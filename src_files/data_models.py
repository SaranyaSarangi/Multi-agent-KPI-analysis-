"""
Data Models for KPI Agent System
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum
import pandas as pd


class AnomalyMethod(Enum):
    """Supported anomaly detection methods"""
    ZSCORE = "z_score"
    IQR = "iqr"
    ISOLATION_FOREST = "isolation_forest"
    MOVING_AVERAGE = "moving_average"
    SEASONAL = "seasonal"
    MULTIVARIATE = "multivariate"
    ENSEMBLE = "ensemble"


@dataclass
class AnomalyResult:
    """Single anomaly detection result"""
    index: int
    value: float
    score: float  # Anomaly score (higher = more anomalous)
    method: str
    severity: str  # "critical", "high", "medium", "low"
    deviation_pct: float
    context: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "index": self.index,
            "value": self.value,
            "score": self.score,
            "method": self.method,
            "severity": self.severity,
            "deviation_pct": self.deviation_pct,
            "context": self.context
        }


@dataclass
class MetricAnalysis:
    """Complete analysis for one metric"""
    metric_name: str
    baseline_mean: float
    baseline_std: float
    anomalies: List[AnomalyResult]
    detection_methods_used: List[str]
    seasonality_detected: bool = False
    trend: str = "stable"  # "increasing", "decreasing", "stable"
    correlation_with: Dict[str, float] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "metric_name": self.metric_name,
            "baseline_mean": self.baseline_mean,
            "baseline_std": self.baseline_std,
            "anomalies": [a.to_dict() for a in self.anomalies],
            "detection_methods_used": self.detection_methods_used,
            "seasonality_detected": self.seasonality_detected,
            "trend": self.trend,
            "correlation_with": self.correlation_with
        }


@dataclass
class KPIData:
    """State container for data flowing through agents"""
    raw_data: Optional[pd.DataFrame] = None
    cleaned_data: Optional[pd.DataFrame] = None
    anomalies: Optional[Dict[str, MetricAnalysis]] = None
    report: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    external_context: List[Dict[str, str]] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary (excluding DataFrames for serialization)"""
        return {
            "metadata": self.metadata,
            "anomalies": {
                k: v.to_dict() for k, v in self.anomalies.items()
            } if self.anomalies else None,
            "report": self.report,
            "external_context": self.external_context,
            "raw_data_shape": self.raw_data.shape if self.raw_data is not None else None,
            "cleaned_data_shape": self.cleaned_data.shape if self.cleaned_data is not None else None
        }
