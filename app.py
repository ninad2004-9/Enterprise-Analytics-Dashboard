"""
ENTERPRISE ANALYTICS DASHBOARD - COMPLETE EDITION
All Features Integrated: Navbar, AI Insights, Filters, Data Table, Statistics, Export, and More!
"""

import base64
import io
import pandas as pd
import numpy as np
from datetime import datetime
from scipy import stats

import dash
from dash import dcc, html, Input, Output, State, callback_context, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

# ===============================
# APP SETUP
# ===============================
app = dash.Dash(
    __name__, 
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
    ],
    suppress_callback_exceptions=True
)
app.title = "Enterprise Analytics Platform | Professional BI Dashboard"
server = app.server  # For production deployment

# ===============================
# PROFESSIONAL CSS WITH ALL ENHANCEMENTS
# ===============================
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
        <style>
            /* ===== ROOT VARIABLES ===== */
            :root {
                --primary-color: #2563eb;
                --primary-dark: #1e40af;
                --primary-light: #3b82f6;
                --secondary-color: #7c3aed;
                --success-color: #10b981;
                --warning-color: #f59e0b;
                --danger-color: #ef4444;
                --info-color: #06b6d4;
                
                --bg-primary: #0a0e1a;
                --bg-secondary: #1e293b;
                --bg-tertiary: #334155;
                --bg-card: #1e293b;
                --bg-card-hover: #2d3748;
                
                --text-primary: #f8fafc;
                --text-secondary: #cbd5e1;
                --text-muted: #94a3b8;
                
                --border-color: #334155;
                --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
                --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
                --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
                --shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            }
            
            /* ===== GLOBAL STYLES ===== */
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: radial-gradient(ellipse at top, #1e293b 0%, #0a0e1a 100%);
                color: var(--text-primary);
                line-height: 1.6;
                -webkit-font-smoothing: antialiased;
                -moz-osx-font-smoothing: grayscale;
            }
            
            html {
                scroll-behavior: smooth;
            }
            
            /* ===== ANIMATIONS ===== */
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(30px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            @keyframes slideInLeft {
                from { opacity: 0; transform: translateX(-30px); }
                to { opacity: 1; transform: translateX(0); }
            }
            
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.8; }
            }
            
            @keyframes shimmer {
                0% { background-position: -1000px 0; }
                100% { background-position: 1000px 0; }
            }
            
            .animate-in { animation: fadeIn 0.6s ease-out; }
            .animate-slide-left { animation: slideInLeft 0.6s ease-out; }
            
            /* ===== NAVBAR ===== */
            .navbar {
                background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
                border-bottom: 1px solid var(--border-color);
                padding: 1rem 0;
                box-shadow: var(--shadow-xl);
                position: sticky;
                top: 0;
                z-index: 1000;
                backdrop-filter: blur(10px);
            }
            
            .navbar-brand {
                font-size: 1.5rem;
                font-weight: 800;
                background: linear-gradient(135deg, var(--primary-light) 0%, var(--info-color) 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            /* ===== CARDS ===== */
            .stats-card {
                background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
                border: 1px solid var(--border-color);
                border-radius: 12px;
                padding: 1.75rem;
                position: relative;
                overflow: hidden;
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            }
            
            .stats-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 4px;
                height: 100%;
                background: linear-gradient(180deg, var(--primary-color) 0%, var(--secondary-color) 100%);
                transition: width 0.4s ease;
            }
            
            .stats-card:hover {
                transform: translateY(-8px) scale(1.02);
                box-shadow: var(--shadow-2xl);
                border-color: var(--primary-color);
            }
            
            .stats-card:hover::before {
                width: 100%;
                opacity: 0.05;
            }
            
            .stats-icon {
                width: 60px;
                height: 60px;
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.75rem;
                margin-bottom: 1rem;
                background: rgba(37, 99, 235, 0.1);
                color: var(--primary-light);
            }
            
            .stats-value {
                font-size: 2.5rem;
                font-weight: 800;
                line-height: 1;
                margin-bottom: 0.5rem;
                background: linear-gradient(135deg, var(--text-primary) 0%, var(--text-secondary) 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            .stats-label {
                color: var(--text-muted);
                font-size: 0.875rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                margin-bottom: 0.5rem;
            }
            
            .stats-change {
                display: inline-flex;
                align-items: center;
                gap: 0.25rem;
                padding: 0.35rem 0.85rem;
                border-radius: 9999px;
                font-size: 0.875rem;
                font-weight: 600;
                margin-top: 0.75rem;
            }
            
            .stats-change.positive {
                background: rgba(16, 185, 129, 0.15);
                color: var(--success-color);
            }
            
            .stats-change.negative {
                background: rgba(239, 68, 68, 0.15);
                color: var(--danger-color);
            }
            
            /* ===== UPLOAD ZONE ===== */
            .upload-zone {
                background: var(--bg-card);
                border: 3px dashed var(--border-color);
                border-radius: 20px;
                padding: 4rem 2rem;
                text-align: center;
                cursor: pointer;
                position: relative;
                overflow: hidden;
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            }
            
            .upload-zone::before {
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: linear-gradient(45deg, transparent, rgba(37, 99, 235, 0.05), transparent);
                transform: rotate(45deg);
                transition: all 0.6s ease;
            }
            
            .upload-zone:hover {
                border-color: var(--primary-color);
                background: rgba(37, 99, 235, 0.05);
                box-shadow: var(--shadow-xl);
                transform: translateY(-4px);
            }
            
            .upload-zone:hover::before {
                animation: shimmer 2s infinite;
            }
            
            .upload-icon-container {
                width: 100px;
                height: 100px;
                margin: 0 auto 1.5rem;
                border-radius: 50%;
                background: linear-gradient(135deg, rgba(37, 99, 235, 0.1) 0%, rgba(6, 182, 212, 0.1) 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                animation: pulse 2s ease-in-out infinite;
            }
            
            /* ===== INSIGHTS ===== */
            .insight-card {
                background: linear-gradient(135deg, rgba(37, 99, 235, 0.1) 0%, rgba(6, 182, 212, 0.05) 100%);
                border: 1px solid rgba(37, 99, 235, 0.3);
                border-radius: 12px;
                padding: 1.5rem;
                margin-bottom: 1rem;
                position: relative;
                overflow: hidden;
                border-left: 4px solid var(--primary-color);
                transition: all 0.3s ease;
            }
            
            .insight-card:hover {
                transform: translateX(4px);
                box-shadow: var(--shadow-lg);
            }
            
            .insight-icon {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background: rgba(37, 99, 235, 0.2);
                display: flex;
                align-items: center;
                justify-content: center;
                color: var(--primary-light);
                margin-right: 1rem;
                font-size: 1.25rem;
            }
            
            /* ===== FILTERS ===== */
            .filter-panel {
                background: var(--bg-card);
                border: 1px solid var(--border-color);
                border-radius: 12px;
                padding: 1.5rem;
                margin-bottom: 1.5rem;
                box-shadow: var(--shadow-md);
            }
            
            /* ===== CHARTS ===== */
            .chart-container {
                background: var(--bg-card);
                border: 1px solid var(--border-color);
                border-radius: 12px;
                padding: 1.75rem;
                box-shadow: var(--shadow-md);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                margin-bottom: 1.5rem;
                position: relative;
                overflow: hidden;
            }
            
            .chart-container::after {
                content: '';
                position: absolute;
                top: 0;
                right: 0;
                width: 100px;
                height: 100px;
                background: radial-gradient(circle, rgba(37, 99, 235, 0.1) 0%, transparent 70%);
                border-radius: 50%;
            }
            
            .chart-container:hover {
                box-shadow: var(--shadow-xl);
                border-color: rgba(37, 99, 235, 0.5);
                transform: translateY(-2px);
            }
            
            /* ===== INFO CARD ===== */
            .info-card {
                background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
                border: 1px solid rgba(59, 130, 246, 0.3);
                border-radius: 12px;
                padding: 2rem;
                box-shadow: var(--shadow-lg);
            }
            
            /* ===== BUTTONS ===== */
            .btn-primary {
                background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
                border: none;
                color: white;
                font-weight: 600;
                padding: 0.75rem 1.5rem;
                border-radius: 8px;
                box-shadow: var(--shadow-md);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                cursor: pointer;
            }
            
            .btn-primary:hover {
                box-shadow: var(--shadow-xl);
                transform: translateY(-2px);
            }
            
            /* ===== DATA TABLE ===== */
            .dash-table-container {
                background: var(--bg-card);
                border-radius: 12px;
                overflow: hidden;
                box-shadow: var(--shadow-md);
            }
            
            /* ===== TOAST ===== */
            .toast {
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 9999;
                min-width: 300px;
                animation: slideInLeft 0.3s ease-out;
            }
            
            /* ===== SCROLLBAR ===== */
            ::-webkit-scrollbar {
                width: 12px;
                height: 12px;
            }
            
            ::-webkit-scrollbar-track {
                background: var(--bg-primary);
            }
            
            ::-webkit-scrollbar-thumb {
                background: var(--bg-tertiary);
                border-radius: 6px;
                border: 2px solid var(--bg-primary);
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: var(--primary-color);
            }
            
            /* ===== SECTION HEADERS ===== */
            .section-header {
                position: relative;
                padding-left: 1.5rem;
                margin: 3rem 0 2rem 0;
            }
            
            .section-header::before {
                content: '';
                position: absolute;
                left: 0;
                top: 50%;
                transform: translateY(-50%);
                width: 6px;
                height: 60%;
                background: linear-gradient(180deg, var(--primary-color) 0%, var(--info-color) 100%);
                border-radius: 3px;
                box-shadow: 0 0 12px var(--primary-color);
            }
            
            /* ===== RESPONSIVE ===== */
            @media (max-width: 768px) {
                .stats-value { font-size: 2rem; }
                .upload-zone { padding: 3rem 1.5rem; }
                .navbar-brand { font-size: 1.25rem; }
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# ===============================
# HELPER FUNCTIONS
# ===============================

def parse_contents(contents, filename):
    """Parse uploaded file contents"""
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    
    try:
        if filename.endswith(".csv"):
            return pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        elif filename.endswith((".xlsx", ".xls")):
            return pd.read_excel(io.BytesIO(decoded))
        else:
            return None
    except Exception as e:
        print(f"Error parsing file: {e}")
        return None

def detect_column_types(df):
    """Detect numeric, categorical, and datetime columns"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    
    # Try to convert string columns to datetime
    for col in categorical_cols[:]:
        try:
            # Try parsing with infer_datetime_format to avoid warning
            pd.to_datetime(df[col], format='mixed', errors='coerce')
            datetime_cols.append(col)
            categorical_cols.remove(col)
        except:
            pass
    
    return numeric_cols, categorical_cols, datetime_cols

def generate_ai_insights(df, numeric_cols, categorical_cols, datetime_cols):
    """Generate AI-powered insights from the data"""
    insights = []
    
    try:
        # 1. Trend Analysis
        if numeric_cols and len(df) > 1:
            col = numeric_cols[0]
            values = df[col].dropna()
            if len(values) >= 2:
                trend = ((values.iloc[-1] - values.iloc[0]) / values.iloc[0] * 100)
                if abs(trend) > 5:
                    direction = "increased" if trend > 0 else "decreased"
                    strength = "significantly" if abs(trend) > 20 else "moderately"
                    insights.append({
                        "icon": "📈" if trend > 0 else "📉",
                        "title": "Trend Detected",
                        "text": f"{col} has {strength} {direction} by {abs(trend):.1f}% from start to end of dataset"
                    })
        
        # 2. Pattern Discovery (Day of Week)
        if datetime_cols and numeric_cols:
            try:
                df_copy = df.copy()
                date_col = datetime_cols[0]
                num_col = numeric_cols[0]
                df_copy[date_col] = pd.to_datetime(df_copy[date_col], format='mixed', errors='coerce')
                df_copy['day_name'] = df_copy[date_col].dt.day_name()
                
                day_avg = df_copy.groupby('day_name')[num_col].mean()
                if len(day_avg) > 0:
                    best_day = day_avg.idxmax()
                    best_value = day_avg.max()
                    worst_day = day_avg.idxmin()
                    insights.append({
                        "icon": "📅",
                        "title": "Pattern Discovered",
                        "text": f"Peak activity occurs on {best_day} with average of {best_value:,.2f}. Lowest on {worst_day}."
                    })
            except:
                pass
        
        # 3. Outlier Detection
        if numeric_cols:
            col = numeric_cols[0]
            values = df[col].dropna()
            if len(values) > 3:
                z_scores = np.abs(stats.zscore(values))
                outliers = len(z_scores[z_scores > 3])
                if outliers > 0:
                    pct = (outliers / len(values)) * 100
                    insights.append({
                        "icon": "⚠️",
                        "title": "Anomaly Alert",
                        "text": f"Detected {outliers} outlier(s) in {col} ({pct:.1f}% of data) - values beyond 3 standard deviations"
                    })
        
        # 4. Correlation Analysis
        if len(numeric_cols) >= 2:
            corr = df[numeric_cols[:2]].corr().iloc[0, 1]
            if abs(corr) > 0.7:
                strength = "Strong" if abs(corr) > 0.8 else "Moderate"
                direction = "positive" if corr > 0 else "negative"
                insights.append({
                    "icon": "🔗",
                    "title": "Correlation Found",
                    "text": f"{strength} {direction} correlation ({corr:.2f}) between {numeric_cols[0]} and {numeric_cols[1]}"
                })
        
        # 5. Data Quality Assessment
        total_cells = df.shape[0] * df.shape[1]
        missing = df.isnull().sum().sum()
        completeness = ((total_cells - missing) / total_cells * 100)
        
        if completeness < 95:
            insights.append({
                "icon": "ℹ️",
                "title": "Data Quality Note",
                "text": f"Dataset is {completeness:.1f}% complete with {missing:,} missing values. Consider data cleaning."
            })
        else:
            insights.append({
                "icon": "✅",
                "title": "Data Quality Excellent",
                "text": f"Dataset is {completeness:.1f}% complete - high quality data ready for analysis"
            })
        
        # 6. Summary Statistics Insight
        if numeric_cols:
            col = numeric_cols[0]
            mean_val = df[col].mean()
            median_val = df[col].median()
            skew = df[col].skew()
            
            if abs(mean_val - median_val) / median_val > 0.2:
                skew_dir = "right" if skew > 0 else "left"
                insights.append({
                    "icon": "📊",
                    "title": "Distribution Insight",
                    "text": f"{col} shows {skew_dir}-skewed distribution (mean: {mean_val:.2f}, median: {median_val:.2f})"
                })
                
    except Exception as e:
        print(f"Insight generation error: {e}")
    
    # Return insights or default message
    return insights if insights else [{
        "icon": "💡",
        "title": "Ready for Analysis",
        "text": "Upload more data or adjust filters to generate deeper insights"
    }]

def create_professional_chart(fig, title=""):
    """Apply professional styling to charts"""
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(30, 41, 59, 0.5)',
        font={'color': '#f1f5f9', 'family': 'Inter, sans-serif'},
        height=400,
        margin=dict(l=60, r=40, t=60, b=60),
        title={
            'text': title,
            'font': {'size': 18, 'color': '#f1f5f9', 'family': 'Inter'},
            'x': 0.02,
            'xanchor': 'left'
        },
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor="#1e293b",
            font_size=12,
            font_family="Inter"
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(51, 65, 85, 0.3)',
            zeroline=False
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(51, 65, 85, 0.3)',
            zeroline=False
        )
    )
    return fig

def calculate_statistics(df, col):
    """Calculate comprehensive statistical measures"""
    values = df[col].dropna()
    return {
        "mean": values.mean(),
        "median": values.median(),
        "std": values.std(),
        "min": values.min(),
        "max": values.max(),
        "q1": values.quantile(0.25),
        "q3": values.quantile(0.75),
        "range": values.max() - values.min(),
        "variance": values.var(),
        "skewness": values.skew(),
        "kurtosis": values.kurtosis()
    }

def create_kpi_card(title, value, delta=None, icon="fa-chart-line", color="primary"):
    """Create professional KPI card"""
    delta_component = None
    if delta is not None:
        delta_class = "positive" if delta >= 0 else "negative"
        delta_icon = "↑" if delta >= 0 else "↓"
        delta_component = html.Div([
            html.Span([
                html.I(className=f"fas fa-arrow-{'up' if delta >= 0 else 'down'}", 
                      style={"marginRight": "0.25rem"}),
                f"{abs(delta):.1f}%"
            ], className=f"stats-change {delta_class}")
        ])
    
    return html.Div([
        html.Div([
            html.I(className=f"fas {icon}", style={"fontSize": "1.75rem", "color": "#3b82f6", "marginBottom": "1rem"}),
            html.Div(title, className="stats-label"),
            html.Div(f"{value:,.2f}" if isinstance(value, (int, float)) else value, 
                    className="stats-value", 
                    style={"color": "#f1f5f9"}),
            delta_component if delta_component else html.Div(style={"height": "32px"})
        ])
    ], className="stats-card")

# ===============================
# LAYOUT
# ===============================

app.layout = dbc.Container(
    fluid=True, 
    style={
        "background": "linear-gradient(135deg, #0a0e1a 0%, #1e293b 100%)",
        "minHeight": "100vh",
        "padding": "0"
    }, 
    children=[
    
    # Toast Container
    html.Div(id="toast-container", className="toast"),
    
    # NAVBAR
    html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.I(className="fas fa-chart-line", 
                              style={"marginRight": "0.75rem", "fontSize": "1.75rem", "color": "#3b82f6"}),
                        html.Span("Enterprise Analytics Platform", className="navbar-brand")
                    ], style={"display": "flex", "alignItems": "center"})
                ], width=6),
                dbc.Col([
                    html.Div([
                        dbc.Button([
                            html.I(className="fas fa-download", style={"marginRight": "0.5rem"}),
                            "Export"
                        ], id="export-btn", color="primary", size="sm", className="me-2"),
                        dbc.Button([
                            html.I(className="fas fa-chart-bar", style={"marginRight": "0.5rem"}),
                            "Chart Builder"
                        ], id="chart-builder-toggle-btn", color="secondary", size="sm", className="me-2"),
                        dbc.Button([
                            html.I(className="fas fa-cog")
                        ], id="settings-btn", color="secondary", size="sm", className="me-2"),
                        dbc.Button([
                            html.I(className="fas fa-question-circle")
                        ], id="help-btn", color="info", size="sm", className="me-3"),
                        html.Span(datetime.now().strftime("%B %d, %Y"), 
                                style={"color": "#cbd5e1", "fontSize": "0.875rem", "fontWeight": "500"})
                    ], style={"display": "flex", "alignItems": "center", "justifyContent": "flex-end"})
                ], width=6)
            ])
        ])
    ], className="navbar"),
    
    dbc.Container([
        # Upload Section
        dbc.Row([
            dbc.Col([
                dcc.Upload(
                    id="upload-data",
                    children=html.Div([
                        html.Div(className="upload-icon-container", children=[
                            html.I(className="fas fa-cloud-upload-alt", 
                                  style={"fontSize": "3rem", 
                                        "background": "linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%)",
                                        "-webkit-background-clip": "text",
                                        "-webkit-text-fill-color": "transparent"})
                        ]),
                        html.H4("Drag & Drop or Click to Upload", 
                               style={"color": "#f1f5f9", "marginBottom": "0.5rem", "fontWeight": "700"}),
                        html.P("Supports CSV, XLSX, XLS files • Maximum 50MB", 
                              style={"color": "#94a3b8", "fontSize": "0.875rem"})
                    ], className="upload-zone"),
                    multiple=False
                )
            ], width=12)
        ], className="mb-4 mt-4"),
        
        # Main Content
        dcc.Loading(
            id="loading",
            type="circle",
            color="#3b82f6",
            children=[
                # Dataset Info
                html.Div(id="dataset-info"),
                
                # Custom Chart Builder (Collapsible)
                dbc.Collapse(
                    html.Div(id="chart-builder-section"),
                    id="chart-builder-collapse",
                    is_open=False
                ),
                
                # KPI Section
                html.Div(id="kpi-section"),
                
                # AI Insights
                html.Div(id="insights-section"),
                
                # Statistics
                html.Div(id="statistics-section"),
                
                # Charts
                html.Div(id="charts-section"),
                
                # Data Table
                html.Div(id="table-section")
            ]
        ),
        
        # Footer
        html.Div([
            html.Hr(style={"borderColor": "#334155", "margin": "3rem 0 2rem 0"}),
            html.Div([
                html.P([
                    html.I(className="fas fa-chart-bar", style={"marginRight": "0.5rem"}),
                    "Enterprise Analytics Platform • Built with Dash & Plotly • Powered by AI"
                ], style={"color": "#94a3b8", "textAlign": "center", "marginBottom": "0.5rem", "fontSize": "0.875rem"}),
                html.P([
                    html.I(className="fas fa-bolt", style={"marginRight": "0.5rem", "color": "#f59e0b"}),
                    html.Span("Performance: ", style={"color": "#94a3b8"}),
                    html.Span(id="performance-stats", style={"color": "#3b82f6", "fontWeight": "600"})
                ], style={"textAlign": "center", "fontSize": "0.875rem"})
            ])
        ], style={"padding": "2rem 0"})
        
    ], fluid=True),
    
    # Store components
    dcc.Store(id='stored-data'),
    dcc.Store(id='filtered-data'),
    dcc.Store(id='column-types')
])

# ===============================
# CALLBACKS
# ===============================

# Toggle chart builder
@app.callback(
    Output("chart-builder-collapse", "is_open"),
    Input("chart-builder-toggle-btn", "n_clicks"),
    State("chart-builder-collapse", "is_open"),
    prevent_initial_call=True
)
def toggle_chart_builder(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

# Main dashboard update
@app.callback(
    [
        Output("dataset-info", "children"),
        Output("chart-builder-section", "children"),
        Output("kpi-section", "children"),
        Output("insights-section", "children"),
        Output("statistics-section", "children"),
        Output("charts-section", "children"),
        Output("table-section", "children"),
        Output("performance-stats", "children"),
        Output("stored-data", "data"),
        Output("column-types", "data")
    ],
    Input("upload-data", "contents"),
    State("upload-data", "filename")
)
def update_dashboard(contents, filename):
    """Main callback - generates complete dashboard"""
    
    if contents is None:
        return [None] * 10
    
    start_time = datetime.now()
    
    # Parse data
    df = parse_contents(contents, filename)
    
    if df is None or df.empty:
        error = dbc.Alert([
            html.I(className="fas fa-exclamation-triangle me-2"),
            "Error: Could not parse the file. Please upload a valid CSV or Excel file."
        ], color="danger", className="animate-in")
        return [error] + [None] * 9
    
    # Detect column types
    numeric_cols, categorical_cols, datetime_cols = detect_column_types(df)
    col_types = {
        "numeric": numeric_cols,
        "categorical": categorical_cols,
        "datetime": datetime_cols
    }
    
    # ===== 1. DATASET INFO =====
    info_card = dbc.Card([
        dbc.CardBody([
            html.H5([
                html.I(className="fas fa-database me-2", style={"color": "#3b82f6"}),
                "Dataset Overview"
            ], className="mb-3", style={"color": "#f1f5f9", "fontWeight": "700"}),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Small("Filename", className="d-block", style={"color": "#94a3b8", "fontSize": "0.75rem"}),
                        html.Strong(filename, style={"color": "#3b82f6", "fontSize": "0.95rem"})
                    ])
                ], md=3),
                dbc.Col([
                    html.Div([
                        html.Small("Total Rows", className="d-block", style={"color": "#94a3b8", "fontSize": "0.75rem"}),
                        html.Strong(f"{len(df):,}", style={"color": "#10b981", "fontSize": "0.95rem"})
                    ])
                ], md=2),
                dbc.Col([
                    html.Div([
                        html.Small("Columns", className="d-block", style={"color": "#94a3b8", "fontSize": "0.75rem"}),
                        html.Strong(f"{len(df.columns)}", style={"color": "#f59e0b", "fontSize": "0.95rem"})
                    ])
                ], md=2),
                dbc.Col([
                    html.Div([
                        html.Small("Numeric", className="d-block", style={"color": "#94a3b8", "fontSize": "0.75rem"}),
                        html.Strong(f"{len(numeric_cols)}", style={"color": "#06b6d4", "fontSize": "0.95rem"})
                    ])
                ], md=2),
                dbc.Col([
                    html.Div([
                        html.Small("Categorical", className="d-block", style={"color": "#94a3b8", "fontSize": "0.75rem"}),
                        html.Strong(f"{len(categorical_cols)}", style={"color": "#7c3aed", "fontSize": "0.95rem"})
                    ])
                ], md=3)
            ])
        ])
    ], className="info-card mb-4 animate-in")
    
    # ===== 2. CUSTOM CHART BUILDER =====
    chart_builder = dbc.Card([
        dbc.CardBody([
            html.H5([
                html.I(className="fas fa-chart-bar me-2"),
                "Custom Chart Builder"
            ], className="mb-3", style={"color": "#f1f5f9", "fontWeight": "700"}),
            dbc.Row([
                dbc.Col([
                    html.Label("X Axis", style={"color": "#cbd5e1", "fontSize": "0.875rem", "fontWeight": "600", "marginBottom": "0.5rem"}),
                    dcc.Dropdown(
                        id="custom-x-axis",
                        options=[{"label": col, "value": col} for col in df.columns],
                        placeholder="Select X axis...",
                        value=df.columns[0] if len(df.columns) > 0 else None,
                        style={"color": "#000"}
                    )
                ], md=3),
                dbc.Col([
                    html.Label("Y Axis", style={"color": "#cbd5e1", "fontSize": "0.875rem", "fontWeight": "600", "marginBottom": "0.5rem"}),
                    dcc.Dropdown(
                        id="custom-y-axis",
                        options=[{"label": col, "value": col} for col in numeric_cols] if numeric_cols else [],
                        placeholder="Select Y axis...",
                        value=numeric_cols[0] if numeric_cols else None,
                        style={"color": "#000"}
                    )
                ], md=3),
                dbc.Col([
                    html.Label("Chart Type", style={"color": "#cbd5e1", "fontSize": "0.875rem", "fontWeight": "600", "marginBottom": "0.5rem"}),
                    dcc.Dropdown(
                        id="custom-chart-type",
                        options=[
                            {"label": "📊 Bar Chart", "value": "bar"},
                            {"label": "📈 Line Chart", "value": "line"},
                            {"label": "🔵 Scatter Plot", "value": "scatter"},
                            {"label": "📉 Area Chart", "value": "area"},
                            {"label": "📊 Histogram", "value": "histogram"},
                            {"label": "📦 Box Plot", "value": "box"},
                            {"label": "🥧 Pie Chart", "value": "pie"}
                        ],
                        placeholder="Select chart type...",
                        value="bar",
                        style={"color": "#000"}
                    )
                ], md=3),
                dbc.Col([
                    html.Label("Color By (Optional)", style={"color": "#cbd5e1", "fontSize": "0.875rem", "fontWeight": "600", "marginBottom": "0.5rem"}),
                    dcc.Dropdown(
                        id="custom-color-by",
                        options=[{"label": col, "value": col} for col in categorical_cols] if categorical_cols else [],
                        placeholder="Select color grouping...",
                        style={"color": "#000"}
                    )
                ], md=3)
            ]),
            html.Hr(style={"borderColor": "#334155", "margin": "1.5rem 0"}),
            html.Div(id="custom-chart-output", className="mt-3")
        ])
    ], style={
        "background": "var(--bg-card)",
        "border": "1px solid var(--border-color)",
        "borderRadius": "12px",
        "boxShadow": "var(--shadow-md)"
    }, className="mb-4 animate-in")
    
    # ===== 3. KPI CARDS =====
    kpi_cards = []
    icons = ["fa-chart-line", "fa-chart-bar", "fa-chart-pie", "fa-chart-area"]
    
    if numeric_cols:
        for i, col in enumerate(numeric_cols[:4]):
            mean_val = df[col].mean()
            std_val = df[col].std()
            delta = (std_val / mean_val * 100) if mean_val != 0 else 0
            
            kpi_cards.append(
                dbc.Col(
                    create_kpi_card(col, mean_val, delta, icons[i % len(icons)]),
                    md=3, className="mb-3"
                )
            )
    
    kpi_section = html.Div([
        html.Div([
            html.H5([
                html.I(className="fas fa-tachometer-alt me-2"),
                "Key Performance Indicators"
            ], style={"color": "#f1f5f9", "display": "inline-block"}),
            html.Span(f" • {len(numeric_cols)} Metrics", 
                     style={"color": "#94a3b8", "fontSize": "0.875rem", "marginLeft": "0.5rem"})
        ], className="section-header"),
        dbc.Row(kpi_cards, className="animate-in")
    ]) if kpi_cards else None
    
    # ===== 4. AI INSIGHTS =====
    insights = generate_ai_insights(df, numeric_cols, categorical_cols, datetime_cols)
    
    insight_cards = []
    for insight in insights:
        insight_cards.append(
            html.Div([
                html.Div([
                    html.Div(insight["icon"], className="insight-icon"),
                    html.Div([
                        html.H6(insight["title"], className="mb-1", 
                               style={"color": "#f1f5f9", "fontWeight": "700", "fontSize": "1rem"}),
                        html.P(insight["text"], className="mb-0", 
                              style={"color": "#cbd5e1", "fontSize": "0.875rem", "lineHeight": "1.5"})
                    ], style={"flex": "1"})
                ], style={"display": "flex", "alignItems": "flex-start"})
            ], className="insight-card")
        )
    
    insights_section = html.Div([
        html.Div([
            html.H5([
                html.I(className="fas fa-lightbulb me-2"),
                "AI-Powered Insights"
            ], style={"color": "#f1f5f9", "display": "inline-block"}),
            html.Span(f" • {len(insights)} Discoveries", 
                     style={"color": "#94a3b8", "fontSize": "0.875rem", "marginLeft": "0.5rem"})
        ], className="section-header"),
        html.Div(insight_cards, className="animate-in")
    ])
    
    # ===== 5. STATISTICS SECTION =====
    stats_cards = []
    if numeric_cols:
        col = numeric_cols[0]
        stats_data = calculate_statistics(df, col)
        
        stat_items = [
            ("Mean", stats_data["mean"], "fa-calculator", "primary"),
            ("Median", stats_data["median"], "fa-chart-line", "success"),
            ("Std Dev", stats_data["std"], "fa-wave-square", "warning"),
            ("Range", stats_data["range"], "fa-arrows-alt-h", "info")
        ]
        
        for label, value, icon, color in stat_items:
            stats_cards.append(
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.I(className=f"fas {icon}", 
                                  style={"fontSize": "1.75rem", "color": "#3b82f6", "marginBottom": "0.75rem"}),
                            html.Div(label, style={"color": "#94a3b8", "fontSize": "0.75rem", 
                                                  "fontWeight": "600", "textTransform": "uppercase"}),
                            html.Div(f"{value:,.2f}", 
                                    style={"fontSize": "1.75rem", "fontWeight": "700", 
                                          "color": "#f1f5f9", "marginTop": "0.5rem"})
                        ])
                    ], style={"background": "var(--bg-card)", "border": "1px solid var(--border-color)", 
                             "borderRadius": "12px", "boxShadow": "var(--shadow-md)"})
                ], md=3, className="mb-3")
            )
    
    statistics_section = html.Div([
        html.Div([
            html.H5([
                html.I(className="fas fa-chart-bar me-2"),
                f"Statistical Analysis"
            ], style={"color": "#f1f5f9", "display": "inline-block"}),
            html.Span(f" • {numeric_cols[0] if numeric_cols else 'N/A'}", 
                     style={"color": "#94a3b8", "fontSize": "0.875rem", "marginLeft": "0.5rem"})
        ], className="section-header"),
        dbc.Row(stats_cards, className="animate-in")
    ]) if stats_cards else None
    
    # ===== 6. CHARTS SECTION =====
    chart_components = []
    
    # Distribution Histogram
    if numeric_cols:
        fig = px.histogram(df, x=numeric_cols[0], color_discrete_sequence=['#3b82f6'])
        fig = create_professional_chart(fig, f"Distribution of {numeric_cols[0]}")
        fig.update_traces(marker_line_width=1.5, marker_line_color='#1e40af', opacity=0.9)
        chart_components.append(
            dbc.Col([
                html.Div([
                    html.Div([
                        html.H6([
                            html.I(className="fas fa-chart-bar me-2"),
                            f"Distribution - {numeric_cols[0]}"
                        ], style={"color": "#f1f5f9", "marginBottom": "1rem"})
                    ]),
                    dcc.Graph(figure=fig, config={'displayModeBar': False})
                ], className="chart-container")
            ], md=6)
        )
    
    # Category Analysis
    if categorical_cols and numeric_cols:
        cat_col = categorical_cols[0]
        num_col = numeric_cols[0]
        top_cats = df[cat_col].value_counts().head(10).index
        df_filtered = df[df[cat_col].isin(top_cats)]
        
        fig = px.bar(df_filtered.groupby(cat_col)[num_col].mean().reset_index(),
                    x=cat_col, y=num_col, color_discrete_sequence=['#3b82f6'])
        fig = create_professional_chart(fig, f"Average {num_col} by {cat_col}")
        fig.update_traces(marker_line_width=1.5, marker_line_color='#1e40af')
        chart_components.append(
            dbc.Col([
                html.Div([
                    html.Div([
                        html.H6([
                            html.I(className="fas fa-chart-column me-2"),
                            f"Category Analysis"
                        ], style={"color": "#f1f5f9", "marginBottom": "1rem"})
                    ]),
                    dcc.Graph(figure=fig, config={'displayModeBar': False})
                ], className="chart-container")
            ], md=6)
        )
    
    # Time Series
    if datetime_cols and numeric_cols:
        date_col = datetime_cols[0]
        num_col = numeric_cols[0]
        df_time = df.copy()
        # Parse dates with format specification to avoid warning
        df_time[date_col] = pd.to_datetime(df_time[date_col], format='mixed', errors='coerce')
        df_time = df_time.sort_values(date_col)
        
        fig = px.line(df_time, x=date_col, y=num_col, color_discrete_sequence=['#3b82f6'])
        fig = create_professional_chart(fig, f"{num_col} Over Time")
        fig.update_traces(line_width=3, fill='tozeroy', fillcolor='rgba(59, 130, 246, 0.2)')
        chart_components.append(
            dbc.Col([
                html.Div([
                    html.Div([
                        html.H6([
                            html.I(className="fas fa-chart-line me-2"),
                            f"Time Series Analysis"
                        ], style={"color": "#f1f5f9", "marginBottom": "1rem"})
                    ]),
                    dcc.Graph(figure=fig, config={'displayModeBar': False})
                ], className="chart-container")
            ], md=12)
        )
    
    # Correlation Heatmap
    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr()
        fig = px.imshow(corr, text_auto='.2f', color_continuous_scale='RdBu_r', aspect='auto')
        fig = create_professional_chart(fig, "Correlation Matrix")
        fig.update_traces(textfont={"size": 11})
        chart_components.append(
            dbc.Col([
                html.Div([
                    html.Div([
                        html.H6([
                            html.I(className="fas fa-table-cells me-2"),
                            "Correlation Analysis"
                        ], style={"color": "#f1f5f9", "marginBottom": "1rem"})
                    ]),
                    dcc.Graph(figure=fig, config={'displayModeBar': False})
                ], className="chart-container")
            ], md=12)
        )
    
    charts_section = html.Div([
        html.Div([
            html.H5([
                html.I(className="fas fa-chart-pie me-2"),
                "Data Visualizations"
            ], style={"color": "#f1f5f9", "display": "inline-block"}),
            html.Span(f" • {len(chart_components)} Charts", 
                     style={"color": "#94a3b8", "fontSize": "0.875rem", "marginLeft": "0.5rem"})
        ], className="section-header"),
        dbc.Row(chart_components, className="animate-in")
    ]) if chart_components else None
    
    # ===== 7. DATA TABLE =====
    table = dash_table.DataTable(
        id='data-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.head(100).to_dict('records'),
        page_size=25,
        page_current=0,
        sort_action='native',
        sort_mode='multi',
        filter_action='native',
        style_table={'overflowX': 'auto'},
        style_cell={
            'textAlign': 'left',
            'padding': '12px',
            'fontFamily': 'Inter',
            'backgroundColor': '#1e293b',
            'color': '#f1f5f9',
            'border': '1px solid #334155',
            'fontSize': '0.875rem'
        },
        style_header={
            'backgroundColor': '#0f172a',
            'fontWeight': '700',
            'borderBottom': '2px solid #3b82f6',
            'color': '#f1f5f9',
            'textTransform': 'uppercase',
            'fontSize': '0.75rem',
            'letterSpacing': '0.05em'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': '#1e293b'
            },
            {
                'if': {'row_index': 'even'},
                'backgroundColor': '#0f172a'
            },
            {
                'if': {'state': 'active'},
                'backgroundColor': 'rgba(59, 130, 246, 0.2)',
                'border': '1px solid #3b82f6'
            }
        ],
        export_format='xlsx',
        export_headers='display',
        style_as_list_view=True
    )
    
    table_section = html.Div([
        html.Div([
            html.H5([
                html.I(className="fas fa-table me-2"),
                "Data Explorer"
            ], style={"color": "#f1f5f9", "display": "inline-block"}),
            html.Span(f" • Showing 100 of {len(df):,} rows", 
                     style={"color": "#94a3b8", "fontSize": "0.875rem", "marginLeft": "0.5rem"})
        ], className="section-header"),
        html.Div([
            html.Div([
                html.Div([
                    dbc.Button([
                        html.I(className="fas fa-download me-2"),
                        "Export to Excel"
                    ], color="primary", size="sm", className="mb-3"),
                ], style={"display": "flex", "justifyContent": "flex-end"}),
                table
            ], className="dash-table-container")
        ], className="animate-in")
    ])
    
    # Performance stats
    elapsed = (datetime.now() - start_time).total_seconds()
    perf_stats = f"{len(df):,} rows • {len(df.columns)} columns • Loaded in {elapsed:.2f}s • {df.memory_usage(deep=True).sum() / 1024:.1f} KB"
    
    # Store data
    stored = df.to_json(date_format='iso', orient='split')
    
    return (
        info_card, chart_builder, kpi_section, insights_section, 
        statistics_section, charts_section, table_section, 
        perf_stats, stored, col_types
    )

# Custom chart builder callback
@app.callback(
    Output("custom-chart-output", "children"),
    [
        Input("custom-x-axis", "value"),
        Input("custom-y-axis", "value"),
        Input("custom-chart-type", "value"),
        Input("custom-color-by", "value"),
        Input("stored-data", "data")
    ],
    prevent_initial_call=True
)
def update_custom_chart(x_col, y_col, chart_type, color_col, stored_data):
    """Update custom chart based on user selections"""
    
    if not stored_data or not x_col:
        return html.Div([
            html.I(className="fas fa-info-circle me-2"),
            "Select columns and chart type to generate your custom visualization"
        ], style={"color": "#94a3b8", "padding": "2rem", "textAlign": "center"})
    
    try:
        # Load data from storage
        df = pd.read_json(stored_data, orient='split')
        
        # Create chart based on type
        if chart_type == "bar":
            if y_col:
                fig = px.bar(df, x=x_col, y=y_col, color=color_col,
                            color_discrete_sequence=px.colors.sequential.Blues)
            else:
                fig = px.histogram(df, x=x_col, color=color_col,
                                 color_discrete_sequence=px.colors.sequential.Blues)
        elif chart_type == "line":
            fig = px.line(df, x=x_col, y=y_col, color=color_col,
                         color_discrete_sequence=px.colors.sequential.Blues)
            fig.update_traces(line_width=3)
        elif chart_type == "scatter":
            fig = px.scatter(df, x=x_col, y=y_col, color=color_col,
                           color_discrete_sequence=px.colors.sequential.Blues)
        elif chart_type == "area":
            fig = px.area(df, x=x_col, y=y_col, color=color_col,
                         color_discrete_sequence=px.colors.sequential.Blues)
        elif chart_type == "histogram":
            fig = px.histogram(df, x=x_col, color=color_col,
                             color_discrete_sequence=px.colors.sequential.Blues)
        elif chart_type == "box":
            fig = px.box(df, x=x_col, y=y_col, color=color_col,
                        color_discrete_sequence=px.colors.sequential.Blues)
        elif chart_type == "pie":
            if not color_col:
                # For pie chart, use x_col as the names
                fig = px.pie(df, names=x_col, values=y_col if y_col else None,
                           color_discrete_sequence=px.colors.sequential.Blues)
            else:
                fig = px.pie(df, names=color_col, values=y_col if y_col else None,
                           color_discrete_sequence=px.colors.sequential.Blues)
        else:
            fig = px.bar(df, x=x_col, y=y_col)
        
        # Apply professional styling
        title = f"Custom {chart_type.title()}: {y_col if y_col else x_col}"
        if color_col:
            title += f" (colored by {color_col})"
        
        fig = create_professional_chart(fig, title)
        
        return html.Div([
            dcc.Graph(figure=fig, config={'displayModeBar': True, 'displaylogo': False})
        ], className="chart-container")
        
    except Exception as e:
        return dbc.Alert([
            html.I(className="fas fa-exclamation-triangle me-2"),
            f"Error creating chart: {str(e)}"
        ], color="warning")

# Export button callback
@app.callback(
    Output("toast-container", "children"),
    Input("export-btn", "n_clicks"),
    prevent_initial_call=True
)
def handle_export(n_clicks):
    if n_clicks:
        return dbc.Toast(
            [
                html.I(className="fas fa-info-circle me-2"),
                "Export feature ready! Use the 'Export to Excel' button in the data table, or install kaleido for PDF export."
            ],
            header="Export Options",
            icon="info",
            duration=5000,
            style={"position": "fixed", "top": 20, "right": 20, "minWidth": "350px"}
        )

# Help button callback
@app.callback(
    Output("toast-container", "children", allow_duplicate=True),
    Input("help-btn", "n_clicks"),
    prevent_initial_call=True
)
def show_help(n_clicks):
    if n_clicks:
        return dbc.Toast(
            [
                html.H6("🚀 Quick Start Guide", className="mb-2", style={"color": "#f1f5f9"}),
                html.Ol([
                    html.Li("Upload your CSV or Excel file using the upload zone"),
                    html.Li("View auto-generated AI insights and visualizations"),
                    html.Li("Use filters to explore specific data segments"),
                    html.Li("Sort and filter the data table to find patterns"),
                    html.Li("Export results using the table's export feature")
                ], className="mb-0", style={"fontSize": "0.875rem"})
            ],
            header="Help",
            icon="info",
            duration=10000,
            style={"position": "fixed", "top": 20, "right": 20, "minWidth": "400px"}
        )

# Settings button callback
@app.callback(
    Output("toast-container", "children", allow_duplicate=True),
    Input("settings-btn", "n_clicks"),
    prevent_initial_call=True
)
def show_settings(n_clicks):
    if n_clicks:
        return dbc.Toast(
            [
                html.I(className="fas fa-cog me-2"),
                "Settings panel - Customize dashboard preferences, themes, and display options (Feature coming soon)"
            ],
            header="Settings",
            icon="secondary",
            duration=4000,
            style={"position": "fixed", "top": 20, "right": 20, "minWidth": "350px"}
        )

# ===============================
# RUN APP
# ===============================
if __name__ == "__main__":
    import os
    # Windows fix for threading issue
    if os.name == 'nt':
        app.run(debug=True, port=8050, use_reloader=False)
    else:
        app.run(debug=True, port=8050)