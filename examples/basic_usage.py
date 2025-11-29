"""
Basic Usage Example for KPI Agent System
"""

from google import genai
from src import RootAgent, load_config, setup_logging

def main():
    # Setup
    config = load_config()
    setup_logging(log_level=config.log_level)
    
    # Configure Google API
    genai.configure(api_key=config.google_api_key)
    
    # Sample KPI data with anomalies
    sample_csv = """Date,Sales,Revenue,Customer_Count,Conversion_Rate
2025-01-01,100,5000,50,2.0
2025-01-02,105,5250,52,2.1
2025-01-03,98,4900,49,2.0
2025-01-04,300,15000,150,2.0
2025-01-05,102,5100,51,2.0
2025-01-06,99,4950,50,1.9
2025-01-07,103,5150,52,2.0
2025-01-08,101,5050,50,2.0
2025-01-09,97,4850,49,2.0
2025-01-10,500,25000,250,2.0"""

    print("="*70)
    print("KPI ANOMALY DETECTION - BASIC USAGE")
    print("="*70)
    
    # Initialize agent
    agent = RootAgent(model=config.default_model)
    
    # Run analysis
    print("\n📊 Running analysis with ensemble method...")
    result = agent.analyze_kpis(
        csv_content=sample_csv,
        method="ensemble",
        sensitivity="medium"
    )
    
    # Print results
    print("\n" + "="*70)
    print("ANALYSIS RESULTS")
    print("="*70)
    print(result)
    
    # Get execution metrics
    print("\n" + "="*70)
    print("EXECUTION METRICS")
    print("="*70)
    metrics = agent.get_execution_metrics()
    for key, value in metrics.items():
        print(f"{key}: {value}")
    
    print("\n✅ Analysis complete!")


if __name__ == "__main__":
    main()
