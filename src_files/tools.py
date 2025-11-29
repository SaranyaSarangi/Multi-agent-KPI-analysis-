"""
FunctionTool Implementations for KPI Agent System
"""

import pandas as pd
import numpy as np
from typing import Dict, Any
from datetime import datetime
import time
import logging
from io import StringIO

from google.adk.tools import FunctionTool

from .data_models import KPIData, MetricAnalysis
from .detection_engine import AdvancedAnomalyDetector
from .session_manager import session_service, memory_bank
from .observability import tracer
from .config import SENSITIVITY_THRESHOLDS

logger = logging.getLogger(__name__)

# Initialize detector
detector = AdvancedAnomalyDetector()


def ingest_kpi_data(csv_content: str, session_id: str) -> Dict[str, Any]:
    """
    Ingests and cleans KPI data from CSV format.
    
    Args:
        csv_content: The CSV data as a string
        session_id: Unique session identifier
    
    Returns:
        Dictionary with status and ingestion summary
    """
    start_time = time.time()
    
    try:
        df = pd.read_csv(StringIO(csv_content))
        
        state = session_service.get(session_id) or KPIData()
        state.raw_data = df.copy()
        
        # Enhanced cleaning
        cleaned_df = df.copy()
        cleaned_df.columns = cleaned_df.columns.str.strip()
        cleaned_df = cleaned_df.dropna(how='all')
        
        # Convert date columns
        date_cols = [col for col in cleaned_df.columns if 'date' in col.lower()]
        for col in date_cols:
            try:
                cleaned_df[col] = pd.to_datetime(cleaned_df[col])
            except:
                pass
        
        numeric_cols = cleaned_df.select_dtypes(include=[np.number]).columns
        cleaned_df[numeric_cols] = cleaned_df[numeric_cols].fillna(cleaned_df[numeric_cols].median())
        
        state.cleaned_data = cleaned_df
        state.metadata.update({
            'ingestion_time': datetime.now().isoformat(),
            'rows': len(cleaned_df),
            'columns': list(cleaned_df.columns),
            'numeric_columns': list(numeric_cols),
            'has_date_column': len(date_cols) > 0
        })
        
        session_service.set(session_id, state)
        
        duration = time.time() - start_time
        result = {
            "status": "success",
            "message": f"Ingested {len(cleaned_df)} rows with {len(cleaned_df.columns)} columns",
            "rows": len(cleaned_df),
            "columns": list(cleaned_df.columns),
            "numeric_columns": list(numeric_cols),
            "duration": duration
        }
        
        tracer.log_tool_call("ingest_kpi_data", {"session_id": session_id}, duration, result)
        return result
    
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        duration = time.time() - start_time
        result = {"status": "error", "error": str(e)}
        tracer.log_tool_call("ingest_kpi_data", {"session_id": session_id}, duration, result)
        return result


def analyze_kpi_deviations_advanced(
    session_id: str,
    method: str = "ensemble",
    sensitivity: str = "medium",
    enable_seasonality: bool = True,
    enable_multivariate: bool = True
) -> Dict[str, Any]:
    """
    Advanced anomaly detection with multiple algorithms.
    
    Args:
        session_id: Session identifier
        method: Detection method
        sensitivity: Alert threshold level
        enable_seasonality: Detect seasonal patterns
        enable_multivariate: Analyze correlations
    
    Returns:
        Comprehensive anomaly analysis
    """
    start_time = time.time()
    
    try:
        state = session_service.get(session_id)
        if not state or state.cleaned_data is None:
            return {"status": "error", "error": "No data found. Call ingest_kpi_data first."}
        
        df = state.cleaned_data
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        thresholds = SENSITIVITY_THRESHOLDS.get(sensitivity, SENSITIVITY_THRESHOLDS["medium"])
        
        analyses = {}
        
        for col in numeric_cols:
            values = df[col].values
            
            # Select detection method
            if method == "ensemble":
                anomalies = detector.detect_ensemble(values)
            elif method == "z_score":
                anomalies = detector.detect_zscore(values, thresholds["z"])
            elif method == "iqr":
                anomalies = detector.detect_iqr(values, thresholds["iqr"])
            elif method == "isolation_forest":
                anomalies = detector.detect_isolation_forest(values, thresholds["isolation"])
            elif method == "moving_average":
                anomalies = detector.detect_moving_average(values)
            elif method == "seasonal":
                anomalies, seasonality, trend = detector.detect_seasonal(values)
            else:
                anomalies = detector.detect_ensemble(values)
            
            # Additional analyses
            seasonality_detected = False
            trend_direction = "stable"
            if enable_seasonality and len(values) >= 14:
                _, seasonality_detected, trend_direction = detector.detect_seasonal(values, period=7)
            
            correlations = {}
            if enable_multivariate:
                correlations = detector.detect_multivariate(df, col)
            
            # Create metric analysis
            analysis = MetricAnalysis(
                metric_name=col,
                baseline_mean=float(np.mean(values)),
                baseline_std=float(np.std(values)),
                anomalies=anomalies,
                detection_methods_used=[method],
                seasonality_detected=seasonality_detected,
                trend=trend_direction,
                correlation_with=correlations
            )
            
            analyses[col] = analysis
            
            # Store baseline in memory
            memory_bank.store(
                f"baseline_{col}_{datetime.now().strftime('%Y%m')}",
                {"mean": float(np.mean(values)), "std": float(np.std(values))}
            )
        
        # Update state
        state.anomalies = analyses
        state.metadata['analysis_time'] = datetime.now().isoformat()
        state.metadata['detection_method'] = method
        state.metadata['sensitivity'] = sensitivity
        session_service.set(session_id, state)
        
        # Build summary
        total_anomalies = sum(len(a.anomalies) for a in analyses.values())
        critical_count = sum(
            len([ano for ano in a.anomalies if ano.severity == "critical"]) 
            for a in analyses.values()
        )
        
        duration = time.time() - start_time
        result = {
            "status": "success",
            "message": f"Found {total_anomalies} anomalies ({critical_count} critical)",
            "summary": {
                "total_anomalies": total_anomalies,
                "critical_anomalies": critical_count,
                "metrics_analyzed": len(analyses),
                "method_used": method,
                "sensitivity": sensitivity
            },
            "duration": duration
        }
        
        tracer.log_tool_call("analyze_kpi_deviations_advanced", 
                           {"session_id": session_id, "method": method}, 
                           duration, result)
        return result
    
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        duration = time.time() - start_time
        result = {"status": "error", "error": str(e)}
        tracer.log_tool_call("analyze_kpi_deviations_advanced", {"session_id": session_id}, duration, result)
        return result


def search_anomaly_context(query: str, session_id: str) -> Dict[str, Any]:
    """
    Search the web for external context about anomalies.
    
    Args:
        query: Search query
        session_id: Session identifier
    
    Returns:
        Search results with relevant context
    """
    start_time = time.time()
    
    try:
        logger.info(f"SEARCH: Querying Google for: {query}")
        
        # Mock search results (replace with actual Google Search API)
        search_results = {
            "status": "success",
            "query": query,
            "results": [
                {
                    "title": "Market Analysis: Understanding KPI Fluctuations",
                    "snippet": "Recent market trends show increased volatility...",
                    "url": "https://example.com/market-analysis"
                }
            ]
        }
        
        # Store in session
        state = session_service.get(session_id)
        if state:
            state.external_context.append({
                "query": query,
                "results": search_results["results"],
                "timestamp": datetime.now().isoformat()
            })
            session_service.set(session_id, state)
        
        duration = time.time() - start_time
        tracer.log_tool_call("search_anomaly_context", {"query": query}, duration, search_results)
        return search_results
    
    except Exception as e:
        logger.error(f"Search failed: {e}")
        duration = time.time() - start_time
        result = {"status": "error", "error": str(e)}
        tracer.log_tool_call("search_anomaly_context", {"query": query}, duration, result)
        return result


def generate_executive_report(session_id: str) -> Dict[str, Any]:
    """
    Generate executive report with context-engineered data.
    
    Args:
        session_id: Session identifier
    
    Returns:
        Compacted report data
    """
    start_time = time.time()
    
    try:
        state = session_service.get(session_id)
        if not state or not state.anomalies:
            return {"status": "error", "error": "No analysis found."}
        
        # Context engineering: Compact the analysis
        compacted = []
        for metric_name, analysis in state.anomalies.items():
            if not analysis.anomalies:
                continue
            
            sorted_anomalies = sorted(
                analysis.anomalies,
                key=lambda x: {"critical": 4, "high": 3, "medium": 2, "low": 1}.get(x.severity, 0),
                reverse=True
            )
            
            compacted.append({
                "metric": metric_name,
                "baseline_mean": round(analysis.baseline_mean, 2),
                "total_anomalies": len(analysis.anomalies),
                "critical_count": len([a for a in analysis.anomalies if a.severity == "critical"]),
                "trend": analysis.trend,
                "seasonality": analysis.seasonality_detected,
                "correlations": analysis.correlation_with,
                "top_anomalies": [
                    {
                        "value": round(a.value, 2),
                        "deviation": round(a.deviation_pct, 1),
                        "severity": a.severity,
                        "method": a.method,
                        "confidence": a.context.get("confidence", 1.0) if a.method == "ensemble" else 1.0
                    }
                    for a in sorted_anomalies[:3]
                ]
            })
        
        report_data = {
            "metadata": {
                "session_id": session_id,
                "analysis_time": state.metadata.get('analysis_time'),
                "rows_analyzed": state.metadata.get('rows'),
                "method": state.metadata.get('detection_method'),
                "sensitivity": state.metadata.get('sensitivity')
            },
            "metrics": compacted,
            "external_context": state.external_context
        }
        
        state.report = report_data
        session_service.set(session_id, state)
        
        duration = time.time() - start_time
        result = {
            "status": "success",
            "message": f"Report generated for {len(compacted)} metrics",
            "report_data": report_data,
            "duration": duration
        }
        
        tracer.log_tool_call("generate_executive_report", {"session_id": session_id}, duration, result)
        return result
    
    except Exception as e:
        logger.error(f"Report generation failed: {e}")
        duration = time.time() - start_time
        result = {"status": "error", "error": str(e)}
        tracer.log_tool_call("generate_executive_report", {"session_id": session_id}, duration, result)
        return result


# Wrap as FunctionTools
ingest_tool = FunctionTool(func=ingest_kpi_data)
analysis_tool = FunctionTool(func=analyze_kpi_deviations_advanced)
search_tool = FunctionTool(func=search_anomaly_context)
report_tool = FunctionTool(func=generate_executive_report)
