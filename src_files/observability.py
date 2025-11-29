"""
Observability: Logging, Tracing, and Metrics
"""

import logging
import json
from typing import Dict, Any, List
from datetime import datetime


class ExecutionTracer:
    """Tracks agent execution for observability"""
    
    def __init__(self):
        self.traces: List[Dict[str, Any]] = []
        self.logger = logging.getLogger(__name__)
    
    def log_tool_call(self, tool_name: str, args: Dict, duration: float, result: Any):
        """Log a tool execution"""
        trace = {
            "timestamp": datetime.now().isoformat(),
            "type": "tool_call",
            "tool_name": tool_name,
            "arguments": args,
            "duration_seconds": duration,
            "status": result.get("status") if isinstance(result, dict) else "completed",
            "result_summary": str(result)[:200]
        }
        self.traces.append(trace)
        self.logger.info(
            f"TOOL_CALL: {tool_name} | "
            f"Duration: {duration:.2f}s | "
            f"Status: {trace['status']}"
        )
    
    def log_agent_decision(self, decision: str, context: str):
        """Log agent reasoning"""
        trace = {
            "timestamp": datetime.now().isoformat(),
            "type": "agent_decision",
            "decision": decision,
            "context": context
        }
        self.traces.append(trace)
        self.logger.info(f"AGENT_DECISION: {decision}")
    
    def get_metrics(self) -> Dict:
        """Get execution metrics"""
        if not self.traces:
            return {}
        
        tool_calls = [t for t in self.traces if t.get("type") == "tool_call"]
        total_duration = sum(t["duration_seconds"] for t in tool_calls)
        
        return {
            "total_tool_calls": len(tool_calls),
            "total_duration": total_duration,
            "average_duration": total_duration / len(tool_calls) if tool_calls else 0,
            "tools_used": list(set(t["tool_name"] for t in tool_calls)),
            "success_rate": sum(1 for t in tool_calls if t.get("status") == "success") / len(tool_calls) if tool_calls else 0
        }
    
    def export_traces(self) -> str:
        """Export traces as JSON"""
        return json.dumps(self.traces, indent=2)
    
    def clear(self):
        """Clear all traces"""
        self.traces = []


# Global tracer instance
tracer = ExecutionTracer()


def setup_logging(log_level: str = "INFO", log_file: str = None):
    """
    Setup logging configuration.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional log file path
    """
    handlers = [logging.StreamHandler()]
    
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers
    )
