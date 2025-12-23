"""
KPI Multi-Agent Anomaly Detection Platform - Streamlit Frontend

"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
import time

# Import your backend (adjust path as needed)
# For demo purposes, we'll create a simplified version
# In production, import from your actual backend:
# from your_backend_module import RootAgent

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="KPI Anomaly Detection",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS
# ============================================================================

st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #1f77b4;
        --secondary-color: #ff7f0e;
        --success-color: #2ca02c;
        --warning-color: #ff7f0e;
        --danger-color: #d62728;
    }
    
    /* Header styling */
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(120deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .metric-card-success {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    
    .metric-card-warning {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    
    .metric-card-info {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    
    /* Anomaly badge */
    .anomaly-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    
    .badge-critical {
        background-color: #d62728;
        color: white;
    }
    
    .badge-high {
        background-color: #ff7f0e;
        color: white;
    }
    
    .badge-medium {
        background-color: #ffbb00;
        color: black;
    }
    
    .badge-low {
        background-color: #2ca02c;
        color: white;
    }
    
    /* Upload section */
    .upload-section {
        border: 2px dashed #1f77b4;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background-color: #f8f9fa;
    }
    
    /* Results section */
    .results-container {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-top: 1rem;
    }
    
    /* Stlying for dataframe */
    .dataframe {
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_sample_data():
    """Generate sample data for demo"""
    return """Date,Sales,Revenue,Customer_Count,Conversion_Rate
2025-01-01,100,5000,50,2.0
2025-01-02,105,5250,52,2.1
2025-01-03,98,4900,49,2.0
2025-01-04,300,15000,150,2.0
2025-01-05,102,5100,51,2.0
2025-01-06,99,4950,50,1.9
2025-01-07,103,5150,52,2.0
2025-01-08,101,5050,50,2.0
2025-01-09,97,4850,49,2.0
2025-01-10,500,25000,250,2.0
2025-01-11,105,5250,52,2.1
2025-01-12,102,5100,51,2.0
2025-01-13,98,4900,49,2.0
2025-01-14,103,5150,52,2.0"""


def simulate_analysis(csv_content, method, sensitivity):
    """Simulate backend analysis (replace with actual RootAgent call)"""
    
    # Simulate processing time
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    status_text.text("🔄 Ingesting data...")
    time.sleep(0.5)
    progress_bar.progress(25)
    
    status_text.text("🔍 Running anomaly detection...")
    time.sleep(1)
    progress_bar.progress(50)
    
    status_text.text("🌐 Searching for context...")
    time.sleep(0.8)
    progress_bar.progress(75)
    
    status_text.text("📊 Generating report...")
    time.sleep(0.5)
    progress_bar.progress(100)
    
    status_text.empty()
    progress_bar.empty()
    
    # Simulated results (replace with actual agent.analyze_kpis() call)
    return {
        "session_id": f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "summary": {
            "total_anomalies": 7,
            "critical_count": 2,
            "high_count": 2,
            "medium_count": 2,
            "low_count": 1,
            "metrics_analyzed": 4
        },
        "anomalies": {
            "Sales": [
                {"index": 3, "value": 300, "deviation_pct": 191.2, "severity": "high"},
                {"index": 9, "value": 500, "deviation_pct": 386.5, "severity": "critical"}
            ],
            "Revenue": [
                {"index": 3, "value": 15000, "deviation_pct": 191.2, "severity": "high"},
                {"index": 9, "value": 25000, "deviation_pct": 386.5, "severity": "critical"}
            ],
            "Customer_Count": [
                {"index": 3, "value": 150, "deviation_pct": 191.2, "severity": "medium"},
                {"index": 9, "value": 250, "deviation_pct": 386.5, "severity": "medium"}
            ]
        },
        "trends": {
            "Sales": "increasing",
            "Revenue": "increasing",
            "Customer_Count": "stable",
            "Conversion_Rate": "stable"
        },
        "correlations": {
            "Sales": {"Revenue": 0.98, "Customer_Count": 0.95},
            "Revenue": {"Sales": 0.98}
        },
        "report": """**EXECUTIVE SUMMARY**

Analysis of 14 days across 4 KPI metrics revealed 7 anomalies, including 2 critical alerts requiring immediate attention.

**KEY FINDINGS**
- **Sales**: Detected spike of 500 (+386% above baseline) on Day 10 - CRITICAL
- **Revenue**: Correlated spike of 25,000 (+386%) detected - CRITICAL  
- **Customer Count**: Proportional increase detected (250 customers)
- **Trend Analysis**: Sales showing strong increasing trend (+15% week-over-week)
- **Correlation**: Sales and Revenue highly correlated (0.98) - validates data integrity

**RISK ASSESSMENT**

🔴 **HIGH RISK**: Sales and Revenue anomalies require immediate investigation
- Spike magnitude: 4x normal baseline
- Sudden onset: No gradual buildup
- Action needed: Verify data accuracy, check for system errors or genuine business event

🟡 **MEDIUM RISK**: Customer count deviation within acceptable correlation range
- Proportional to sales increase
- Suggests legitimate business activity rather than data error

**RECOMMENDED ACTIONS**

1. **Immediate (0-24h)**: Investigate Day 10 spike - verify data entry, check for promotional campaigns, review transaction logs
2. **Short-term (1-7d)**: Monitor Days 11-14 for pattern continuation vs. one-time anomaly
3. **Analysis**: Compare against marketing calendar - was there a campaign launch?
4. **System Check**: Review data pipeline for potential double-counting or duplicate entries
5. **Threshold Update**: If spike is legitimate, update baseline expectations for future campaigns

**EXTERNAL CONTEXT**

Search results indicate potential promotional campaign or seasonal event during this period. Spike may be expected business behavior rather than anomaly.

**CONFIDENCE LEVEL**: 95% (Ensemble method with 3/3 algorithm agreement)
"""
    }


def plot_time_series(df, anomalies_dict):
    """Create interactive time series plot with anomalies highlighted"""
    
    fig = go.Figure()
    
    # Get numeric columns
    numeric_cols = df.select_dtypes(include=['number']).columns
    
    for col in numeric_cols:
        # Plot main line
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df[col],
            mode='lines+markers',
            name=col,
            line=dict(width=2),
            marker=dict(size=6)
        ))
        
        # Highlight anomalies if present
        if col in anomalies_dict:
            anomaly_indices = [a['index'] for a in anomalies_dict[col]]
            anomaly_values = [a['value'] for a in anomalies_dict[col]]
            
            fig.add_trace(go.Scatter(
                x=anomaly_indices,
                y=anomaly_values,
                mode='markers',
                name=f'{col} Anomalies',
                marker=dict(
                    size=15,
                    color='red',
                    symbol='circle-open',
                    line=dict(width=3, color='red')
                ),
                showlegend=True
            ))
    
    fig.update_layout(
        title="KPI Time Series with Detected Anomalies",
        xaxis_title="Day",
        yaxis_title="Value",
        hovermode='x unified',
        height=500,
        template="plotly_white"
    )
    
    return fig


def plot_anomaly_distribution(summary):
    """Create pie chart of anomaly severity distribution"""
    
    labels = ['Critical', 'High', 'Medium', 'Low']
    values = [
        summary['critical_count'],
        summary['high_count'],
        summary['medium_count'],
        summary['low_count']
    ]
    colors = ['#d62728', '#ff7f0e', '#ffbb00', '#2ca02c']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        hole=0.4
    )])
    
    fig.update_layout(
        title="Anomaly Severity Distribution",
        height=400
    )
    
    return fig


# ============================================================================
# MAIN APP
# ============================================================================

def main():
    # Header
    st.markdown('<h1 class="main-header">🔍 KPI Anomaly Detection</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-Powered Multi-Agent Analysis Platform | Powered by Google ADK & Gemini 2.0</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d4735304ff6292a690345.svg", width=50)
        st.title("⚙️ Configuration")
        
        st.markdown("### Detection Method")
        method = st.selectbox(
            "Algorithm",
            ["ensemble", "z_score", "iqr", "isolation_forest", "moving_average", "seasonal"],
            help="Ensemble combines multiple methods for highest accuracy"
        )
        
        st.markdown("### Sensitivity")
        sensitivity = st.select_slider(
            "Alert Threshold",
            options=["low", "medium", "high"],
            value="medium",
            help="Low: Fewer alerts, High: Catch everything"
        )
        
        st.markdown("### Advanced Options")
        enable_search = st.checkbox("Enable Web Search", value=True, help="Search for external context")
        enable_seasonality = st.checkbox("Detect Seasonality", value=True, help="Identify recurring patterns")
        enable_multivariate = st.checkbox("Correlation Analysis", value=True, help="Analyze metric relationships")
        
        st.markdown("---")
        st.markdown("### About")
        st.info("""
        **Built with:**
        - Google ADK
        - Gemini 2.0 Flash
        - 7 Detection Algorithms
        - Ensemble Voting
        
        **Features:**
        - Real-time analysis
        - Context-aware detection
        - Executive reports
        """)
        
        # Sample data button
        if st.button("📥 Load Sample Data", use_container_width=True):
            st.session_state.sample_data = create_sample_data()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📂 Upload Your Data")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type=['csv'],
            help="Upload CSV with KPI metrics (Date, Sales, Revenue, etc.)"
        )
        
        # Or use sample data
        if 'sample_data' in st.session_state:
            st.success("✅ Sample data loaded! Click 'Analyze' to proceed.")
            csv_content = st.session_state.sample_data
        elif uploaded_file is not None:
            csv_content = uploaded_file.getvalue().decode('utf-8')
            st.success(f"✅ File uploaded: {uploaded_file.name}")
        else:
            csv_content = None
            st.info("👆 Upload a CSV file or click 'Load Sample Data' in the sidebar to get started")
        
        # Show data preview
        if csv_content:
            with st.expander("📊 Data Preview", expanded=False):
                df_preview = pd.read_csv(pd.io.common.StringIO(csv_content))
                st.dataframe(df_preview, use_container_width=True)
                st.caption(f"📏 Shape: {df_preview.shape[0]} rows × {df_preview.shape[1]} columns")
    
    with col2:
        st.markdown("### 🎯 Quick Stats")
        
        if csv_content:
            df_temp = pd.read_csv(pd.io.common.StringIO(csv_content))
            
            # Display metrics
            st.metric("Total Rows", df_temp.shape[0], delta=None)
            st.metric("Metrics to Analyze", len(df_temp.select_dtypes(include=['number']).columns))
            st.metric("Detection Method", method.upper())
            st.metric("Sensitivity", sensitivity.upper())
        else:
            st.info("Upload data to see statistics")
    
    # Analysis button
    st.markdown("---")
    
    if csv_content:
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        
        with col_btn2:
            analyze_button = st.button("🚀 Analyze KPIs", type="primary", use_container_width=True)
        
        if analyze_button:
            st.markdown("---")
            st.markdown("## 📊 Analysis Results")
            
            # Run analysis
            with st.spinner("🤖 AI agents analyzing your data..."):
                results = simulate_analysis(csv_content, method, sensitivity)
            
            # Success message
            st.success(f"✅ Analysis complete! Session ID: `{results['session_id']}`")
            
            # Summary metrics
            st.markdown("### 📈 Summary")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card metric-card-warning">
                    <h3 style="margin:0; font-size: 2rem;">{results['summary']['total_anomalies']}</h3>
                    <p style="margin:0;">Total Anomalies</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card metric-card-info">
                    <h3 style="margin:0; font-size: 2rem;">{results['summary']['critical_count']}</h3>
                    <p style="margin:0;">Critical</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card metric-card-success">
                    <h3 style="margin:0; font-size: 2rem;">{results['summary']['metrics_analyzed']}</h3>
                    <p style="margin:0;">Metrics Analyzed</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <h3 style="margin:0; font-size: 2rem;">95%</h3>
                    <p style="margin:0;">Confidence</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Visualizations
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Time series plot
                df_plot = pd.read_csv(pd.io.common.StringIO(csv_content))
                fig_ts = plot_time_series(df_plot, results['anomalies'])
                st.plotly_chart(fig_ts, use_container_width=True)
            
            with col2:
                # Severity distribution
                fig_pie = plot_anomaly_distribution(results['summary'])
                st.plotly_chart(fig_pie, use_container_width=True)
            
            # Detailed anomalies
            st.markdown("### 🔍 Detected Anomalies")
            
            for metric, anomalies in results['anomalies'].items():
                with st.expander(f"📊 {metric} ({len(anomalies)} anomalies)", expanded=True):
                    for anom in anomalies:
                        severity_class = f"badge-{anom['severity']}"
                        st.markdown(f"""
                        <div style="padding: 1rem; background: #f8f9fa; border-radius: 8px; margin-bottom: 0.5rem;">
                            <span class="anomaly-badge {severity_class}">{anom['severity'].upper()}</span>
                            <strong>Day {anom['index']}</strong>: Value = {anom['value']} 
                            (<strong>{anom['deviation_pct']:+.1f}%</strong> deviation)
                        </div>
                        """, unsafe_allow_html=True)
            
            # Trends & Correlations
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📈 Trend Analysis")
                for metric, trend in results['trends'].items():
                    icon = "📈" if trend == "increasing" else "📉" if trend == "decreasing" else "➡️"
                    st.markdown(f"{icon} **{metric}**: {trend.capitalize()}")
            
            with col2:
                st.markdown("### 🔗 Correlations")
                if results['correlations']:
                    for metric, corrs in results['correlations'].items():
                        st.markdown(f"**{metric}**:")
                        for related, coef in corrs.items():
                            st.markdown(f"  - {related}: {coef:.2f}")
                else:
                    st.info("No significant correlations detected")
            
            # Executive Report
            st.markdown("### 📄 Executive Report")
            st.markdown(results['report'])
            
            # Download options
            st.markdown("---")
            st.markdown("### 💾 Export Results")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                json_str = json.dumps(results, indent=2)
                st.download_button(
                    label="📥 Download JSON",
                    data=json_str,
                    file_name=f"analysis_{results['session_id']}.json",
                    mime="application/json",
                    use_container_width=True
                )
            
            with col2:
                st.download_button(
                    label="📥 Download Report",
                    data=results['report'],
                    file_name=f"report_{results['session_id']}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            
            with col3:
                df_export = pd.read_csv(pd.io.common.StringIO(csv_content))
                st.download_button(
                    label="📥 Download CSV",
                    data=df_export.to_csv(index=False),
                    file_name=f"data_{results['session_id']}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p>Built with ❤️ using Google ADK & Gemini 2.0 Flash</p>
        <p>🔗 <a href="https://github.com/yourusername/kpi-agent">GitHub</a> | 
        📖 <a href="#">Documentation</a> | 
        🎥 <a href="#">Demo Video</a></p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
