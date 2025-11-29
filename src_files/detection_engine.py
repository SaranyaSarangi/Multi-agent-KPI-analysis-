"""
Advanced Anomaly Detection Engine with 7 Algorithms
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.seasonal import seasonal_decompose
import logging

from .data_models import AnomalyResult, AnomalyMethod
from .config import SEVERITY_RULES

logger = logging.getLogger(__name__)


class AdvancedAnomalyDetector:
    """
    Advanced multi-algorithm anomaly detection engine.
    Combines statistical, ML, and time-series methods.
    """
    
    def __init__(self):
        self.scaler = StandardScaler()
    
    def detect_zscore(self, values: np.ndarray, threshold: float = 2.0) -> List[AnomalyResult]:
        """Z-score based detection (parametric, assumes normal distribution)"""
        mean = np.mean(values)
        std = np.std(values)
        
        if std == 0:
            return []
        
        z_scores = np.abs((values - mean) / std)
        anomaly_indices = np.where(z_scores > threshold)[0]
        
        results = []
        for idx in anomaly_indices:
            score = float(z_scores[idx])
            results.append(AnomalyResult(
                index=int(idx),
                value=float(values[idx]),
                score=score,
                method="z_score",
                severity=self._classify_severity(score, threshold),
                deviation_pct=float(((values[idx] - mean) / mean) * 100),
                context={"mean": float(mean), "std": float(std)}
            ))
        
        return results
    
    def detect_iqr(self, values: np.ndarray, multiplier: float = 1.5) -> List[AnomalyResult]:
        """
        IQR (Interquartile Range) based detection.
        More robust to outliers than z-score. Non-parametric.
        """
        q1 = np.percentile(values, 25)
        q3 = np.percentile(values, 75)
        iqr = q3 - q1
        
        lower_bound = q1 - multiplier * iqr
        upper_bound = q3 + multiplier * iqr
        
        anomaly_indices = np.where((values < lower_bound) | (values > upper_bound))[0]
        
        results = []
        median = np.median(values)
        
        for idx in anomaly_indices:
            if values[idx] < lower_bound:
                score = (lower_bound - values[idx]) / iqr
            else:
                score = (values[idx] - upper_bound) / iqr
            
            results.append(AnomalyResult(
                index=int(idx),
                value=float(values[idx]),
                score=float(score),
                method="iqr",
                severity=self._classify_severity(score, multiplier),
                deviation_pct=float(((values[idx] - median) / median) * 100),
                context={"q1": float(q1), "q3": float(q3), "iqr": float(iqr)}
            ))
        
        return results
    
    def detect_isolation_forest(self, values: np.ndarray, contamination: float = 0.1) -> List[AnomalyResult]:
        """
        Isolation Forest (ML-based unsupervised anomaly detection).
        Works well for high-dimensional data and doesn't assume distribution.
        """
        if len(values) < 10:
            logger.warning("Not enough data points for Isolation Forest")
            return []
        
        X = values.reshape(-1, 1)
        
        clf = IsolationForest(contamination=contamination, random_state=42)
        predictions = clf.fit_predict(X)
        scores = clf.score_samples(X)
        
        anomaly_indices = np.where(predictions == -1)[0]
        
        results = []
        mean = np.mean(values)
        
        for idx in anomaly_indices:
            score = float(-scores[idx])
            
            results.append(AnomalyResult(
                index=int(idx),
                value=float(values[idx]),
                score=score,
                method="isolation_forest",
                severity=self._classify_severity(score, 1.0),
                deviation_pct=float(((values[idx] - mean) / mean) * 100),
                context={"isolation_score": float(scores[idx])}
            ))
        
        return results
    
    def detect_moving_average(self, values: np.ndarray, window: int = 3, threshold: float = 2.0) -> List[AnomalyResult]:
        """
        Moving average based detection.
        Good for detecting sudden spikes/drops in time series.
        """
        if len(values) < window:
            return []
        
        ma = np.convolve(values, np.ones(window)/window, mode='valid')
        ma = np.concatenate([np.full(window-1, ma[0]), ma])
        
        deviations = np.abs(values - ma)
        std_dev = np.std(deviations)
        
        if std_dev == 0:
            return []
        
        z_scores = deviations / std_dev
        anomaly_indices = np.where(z_scores > threshold)[0]
        
        results = []
        for idx in anomaly_indices:
            results.append(AnomalyResult(
                index=int(idx),
                value=float(values[idx]),
                score=float(z_scores[idx]),
                method="moving_average",
                severity=self._classify_severity(z_scores[idx], threshold),
                deviation_pct=float(((values[idx] - ma[idx]) / ma[idx]) * 100) if ma[idx] != 0 else 0,
                context={"moving_avg": float(ma[idx]), "window": window}
            ))
        
        return results
    
    def detect_seasonal(self, values: np.ndarray, period: int = 7) -> Tuple[List[AnomalyResult], bool, str]:
        """
        Seasonal decomposition for time series.
        Returns: (anomalies, has_seasonality, trend_direction)
        """
        if len(values) < 2 * period:
            logger.warning(f"Not enough data for seasonal decomposition")
            return [], False, "stable"
        
        try:
            decomposition = seasonal_decompose(values, model='additive', period=period, extrapolate_trend='freq')
            
            residuals = decomposition.resid
            trend = decomposition.trend
            seasonal = decomposition.seasonal
            
            residual_std = np.nanstd(residuals)
            if residual_std == 0:
                return [], False, "stable"
            
            z_scores = np.abs(residuals / residual_std)
            anomaly_indices = np.where(z_scores > 2.5)[0]
            
            # Determine trend
            trend_clean = trend[~np.isnan(trend)]
            if len(trend_clean) > 1:
                trend_slope = np.polyfit(range(len(trend_clean)), trend_clean, 1)[0]
                trend_dir = "increasing" if trend_slope > 0.01 else "decreasing" if trend_slope < -0.01 else "stable"
            else:
                trend_dir = "stable"
            
            # Check seasonality
            seasonal_strength = np.std(seasonal) / np.std(values)
            has_seasonality = seasonal_strength > 0.1
            
            results = []
            for idx in anomaly_indices:
                if not np.isnan(residuals[idx]):
                    results.append(AnomalyResult(
                        index=int(idx),
                        value=float(values[idx]),
                        score=float(z_scores[idx]),
                        method="seasonal",
                        severity=self._classify_severity(z_scores[idx], 2.5),
                        deviation_pct=float((residuals[idx] / values[idx]) * 100) if values[idx] != 0 else 0,
                        context={
                            "residual": float(residuals[idx]),
                            "trend": float(trend[idx]) if not np.isnan(trend[idx]) else None,
                            "seasonal": float(seasonal[idx])
                        }
                    ))
            
            return results, has_seasonality, trend_dir
        
        except Exception as e:
            logger.error(f"Seasonal decomposition failed: {e}")
            return [], False, "stable"
    
    def detect_multivariate(self, df: pd.DataFrame, metric_name: str, threshold: float = 0.7) -> Dict[str, float]:
        """
        Multivariate anomaly detection based on correlations.
        Returns: Dictionary of {metric: correlation_coefficient}
        """
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if metric_name not in numeric_cols or len(numeric_cols) < 2:
            return {}
        
        corr_matrix = df[numeric_cols].corr()
        correlations = corr_matrix[metric_name].to_dict()
        correlations.pop(metric_name, None)
        
        significant_corr = {
            k: v for k, v in correlations.items() 
            if abs(v) > threshold
        }
        
        return significant_corr
    
    def detect_ensemble(self, values: np.ndarray, methods: List[AnomalyMethod] = None) -> List[AnomalyResult]:
        """
        Ensemble method: Combines multiple detection algorithms.
        An anomaly is flagged if detected by multiple methods (voting).
        """
        if methods is None:
            methods = [AnomalyMethod.ZSCORE, AnomalyMethod.IQR, AnomalyMethod.MOVING_AVERAGE]
        
        all_results = []
        
        if AnomalyMethod.ZSCORE in methods:
            all_results.extend(self.detect_zscore(values))
        
        if AnomalyMethod.IQR in methods:
            all_results.extend(self.detect_iqr(values))
        
        if AnomalyMethod.MOVING_AVERAGE in methods:
            all_results.extend(self.detect_moving_average(values))
        
        if AnomalyMethod.ISOLATION_FOREST in methods and len(values) >= 10:
            all_results.extend(self.detect_isolation_forest(values))
        
        # Count votes per index
        vote_counts = {}
        anomaly_details = {}
        
        for result in all_results:
            idx = result.index
            if idx not in vote_counts:
                vote_counts[idx] = 0
                anomaly_details[idx] = []
            vote_counts[idx] += 1
            anomaly_details[idx].append(result)
        
        # Keep anomalies detected by at least 2 methods
        min_votes = max(2, len(methods) // 2)
        ensemble_results = []
        
        for idx, votes in vote_counts.items():
            if votes >= min_votes:
                details = anomaly_details[idx]
                avg_score = np.mean([d.score for d in details])
                methods_used = [d.method for d in details]
                
                ensemble_results.append(AnomalyResult(
                    index=idx,
                    value=float(values[idx]),
                    score=float(avg_score),
                    method="ensemble",
                    severity=self._classify_severity(avg_score, 2.0),
                    deviation_pct=details[0].deviation_pct,
                    context={
                        "votes": votes,
                        "methods": methods_used,
                        "confidence": votes / len(methods)
                    }
                ))
        
        return ensemble_results
    
    def _classify_severity(self, score: float, threshold: float) -> str:
        """Classify anomaly severity based on score"""
        if score > threshold * 3:
            return "critical"
        elif score > threshold * 2:
            return "high"
        elif score > threshold * 1.5:
            return "medium"
        else:
            return "low"
