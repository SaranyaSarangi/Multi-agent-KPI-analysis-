"""
Root Agent Implementation
"""

from datetime import datetime
import logging

from google.adk.agents import Agent

from .tools import ingest_tool, analysis_tool, search_tool, report_tool
from .observability import tracer

logger = logging.getLogger(__name__)


class RootAgent(Agent):
    """
    Root Agent: Orchestrates the entire KPI analysis pipeline.
    
    Features:
    - Sequential tool execution (ingest -> analyze -> report)
    - Custom tools (anomaly detection)
    - Built-in tools (Google Search for external context)
    - Long-term memory (Memory Bank for baselines)
    - Context engineering (compacted data for LLM)
    - Observability (logging, tracing, metrics)
    """
    
    def __init__(self, model: str = "gemini-2.0-flash-exp"):
        super().__init__(
            model=model,
            tools=[ingest_tool, analysis_tool, report_tool, search_tool],
            instruction="""You are an advanced KPI Analysis Agent with sophisticated anomaly detection.

WORKFLOW:
1. ingest_kpi_data() - Load CSV data
2. analyze_kpi_deviations_advanced() - Detect anomalies using advanced algorithms
3. (OPTIONAL) search_anomaly_context() - If major anomalies, search for external explanations
4. generate_executive_report() - Create comprehensive report
5. Provide executive summary with insights

ANOMALY DETECTION METHODS:
- ensemble (default): Combines multiple algorithms for robust detection
- z_score: Statistical method, assumes normal distribution
- iqr: Interquartile range, robust to outliers
- isolation_forest: ML-based, no distribution assumptions
- moving_average: Detects sudden changes in trends
- seasonal: For time series with recurring patterns

SENSITIVITY LEVELS:
- low: Fewer false positives, catches only major anomalies
- medium (default): Balanced approach
- high: Catches all potential anomalies, more false positives

EXECUTIVE SUMMARY SHOULD INCLUDE:
1. Total anomalies found (by severity)
2. Trending patterns (increasing/decreasing/stable)
3. Seasonal effects if detected
4. Correlations between metrics
5. Risk assessment with specific recommendations
6. Detection method and confidence levels

Be data-driven and provide actionable insights.""",
            temperature=0.3
        )
    
    def analyze_kpis(
        self,
        csv_content: str,
        session_id: str = None,
        method: str = "ensemble",
        sensitivity: str = "medium"
    ) -> str:
        """
        Main entry point for advanced KPI analysis.
        
        Args:
            csv_content: CSV data
            session_id: Optional session ID
            method: Detection algorithm to use
            sensitivity: Alert sensitivity level
            
        Returns:
            Natural language analysis report
        """
        if session_id is None:
            session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        tracer.log_agent_decision(
            "Starting KPI analysis pipeline", 
            f"session={session_id}, method={method}, sensitivity={sensitivity}"
        )
        
        prompt = f"""Analyze this KPI data using advanced anomaly detection.

Session ID: {session_id}
Detection Method: {method}
Sensitivity: {sensitivity}

CSV Data:
{csv_content}

Execute the pipeline:
1. Ingest the data
2. Analyze using method="{method}", sensitivity="{sensitivity}"
3. If significant anomalies found, search for external context
4. Generate comprehensive report
5. Provide executive summary with:
   - Anomaly counts by severity
   - Trend analysis
   - Correlation insights
   - Risk assessment
   - Actionable recommendations"""

        logger.info(f"ROOT_AGENT: Starting analysis for session {session_id}")
        response = self.generate(prompt)
        logger.info(f"ROOT_AGENT: Completed analysis for session {session_id}")
        
        tracer.log_agent_decision("Analysis pipeline completed", f"session={session_id}")
        
        return response
    
    def get_execution_metrics(self):
        """Get performance metrics for the last execution"""
        return tracer.get_metrics()
    
    def export_traces(self):
        """Export execution traces for debugging"""
        return tracer.export_traces()
