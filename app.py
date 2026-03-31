"""
Water Quality Prediction System - Streamlit Dashboard
Interactive web application with CSV upload, batch prediction, and real-time monitoring
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from predict_pollution import PollutionPredictor
from mitigation_suggestions import MitigationRecommender

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Water Quality Prediction System",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# PREMIUM CSS STYLING
# ============================================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* Global */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #1a1a3e 40%, #24243e 100%);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #12122a 0%, #1e1e48 100%);
    border-right: 1px solid rgba(255,255,255,0.05);
}
section[data-testid="stSidebar"] .stRadio label {
    color: #e0e0ff !important;
    font-weight: 500;
    padding: 6px 0;
}
section[data-testid="stSidebar"] .stRadio label:hover {
    color: #7c83ff !important;
}

/* Header Glass Card */
.glass-header {
    background: linear-gradient(135deg, rgba(100, 108, 255, 0.15), rgba(0, 210, 255, 0.08));
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 30px 36px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.glass-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at 30% 50%, rgba(100,108,255,0.12), transparent 50%);
    pointer-events: none;
}
.glass-header h1 {
    color: #ffffff;
    font-size: 2.4em;
    font-weight: 800;
    margin: 0 0 6px 0;
    letter-spacing: -0.5px;
    position: relative;
    z-index: 1;
}
.glass-header p {
    color: rgba(200, 210, 255, 0.7);
    font-size: 1.05em;
    margin: 0;
    position: relative;
    z-index: 1;
}

/* Metric Cards */
.metric-glass {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px;
    padding: 24px 20px;
    text-align: center;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    position: relative;
    overflow: hidden;
}
.metric-glass:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(100,108,255,0.15);
}
.metric-glass .metric-value {
    font-size: 2.6em;
    font-weight: 800;
    margin: 8px 0 4px;
    background: linear-gradient(135deg, #ffffff, #c0c8ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.metric-glass .metric-label {
    color: rgba(200,210,255,0.6);
    font-size: 0.85em;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}
.metric-glass .metric-icon {
    font-size: 1.8em;
}

/* Risk-colored metric values */
.metric-good .metric-value {
    background: linear-gradient(135deg, #00e676, #69f0ae) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
}
.metric-moderate .metric-value {
    background: linear-gradient(135deg, #ffa726, #ffcc02) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
}
.metric-bad .metric-value {
    background: linear-gradient(135deg, #ef5350, #ff7043) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
}

/* Section headers */
.section-title {
    color: #e0e0ff;
    font-size: 1.4em;
    font-weight: 700;
    margin: 30px 0 16px;
    padding-bottom: 10px;
    border-bottom: 2px solid rgba(100,108,255,0.3);
    letter-spacing: -0.3px;
}

/* Upload zone */
.upload-zone {
    background: rgba(100,108,255,0.06);
    border: 2px dashed rgba(100,108,255,0.3);
    border-radius: 20px;
    padding: 50px 30px;
    text-align: center;
    transition: all 0.3s ease;
    margin: 20px 0;
}
.upload-zone:hover {
    border-color: rgba(100,108,255,0.6);
    background: rgba(100,108,255,0.1);
}
.upload-zone h3 {
    color: #c0c8ff;
    font-size: 1.5em;
    font-weight: 700;
    margin-bottom: 8px;
}
.upload-zone p {
    color: rgba(200,210,255,0.5);
    font-size: 0.95em;
}

/* Prediction result card */
.result-card {
    border-radius: 18px;
    padding: 28px;
    margin: 16px 0;
    border: 1px solid rgba(255,255,255,0.07);
    backdrop-filter: blur(16px);
}
.result-good {
    background: linear-gradient(135deg, rgba(0,230,118,0.12), rgba(105,240,174,0.06));
    border-left: 4px solid #00e676;
}
.result-moderate {
    background: linear-gradient(135deg, rgba(255,167,38,0.12), rgba(255,204,2,0.06));
    border-left: 4px solid #ffa726;
}
.result-bad {
    background: linear-gradient(135deg, rgba(239,83,80,0.12), rgba(255,112,67,0.06));
    border-left: 4px solid #ef5350;
}
.result-card h2 {
    margin: 0 0 6px 0;
    font-weight: 700;
}
.result-card p { color: rgba(200,210,255,0.7); }

/* Recommendation card */
.rec-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-left: 4px solid #646cff;
    border-radius: 14px;
    padding: 20px 24px;
    margin: 12px 0;
    transition: transform 0.2s;
}
.rec-card:hover {
    transform: translateX(4px);
}
.rec-card h4 {
    color: #c0c8ff;
    margin: 0 0 6px 0;
    font-weight: 600;
}
.rec-card p {
    color: rgba(200,210,255,0.6);
    margin: 0;
    font-size: 0.92em;
    line-height: 1.5;
}

/* Data table */
div[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #646cff 0%, #5a54e0 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 30px;
    font-weight: 600;
    font-size: 1em;
    letter-spacing: 0.3px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 20px rgba(100,108,255,0.3);
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(100,108,255,0.45);
}

/* Download button */
.stDownloadButton > button {
    background: linear-gradient(135deg, #00c853, #00e676) !important;
    color: #0a0a1a !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 20px rgba(0,200,83,0.3) !important;
}

/* Slider */
div[data-testid="stSlider"] > div > div > div {
    background: rgba(100,108,255,0.3) !important;
}

/* Selectbox */
div[data-testid="stSelectbox"] label, div[data-testid="stMultiSelect"] label {
    color: #c0c8ff !important;
}

/* Plotly charts dark theme override */
.js-plotly-plot .plotly .modebar { opacity: 0.4; }
.js-plotly-plot .plotly .modebar:hover { opacity: 0.9; }

/* hide default streamlit branding */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# PLOTLY THEME
# ============================================================================

PLOTLY_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter', color='#c0c8ff', size=13),
    title_font=dict(size=18, color='#e0e0ff', family='Inter'),
    legend=dict(font=dict(color='#c0c8ff')),
    xaxis=dict(gridcolor='rgba(100,108,255,0.08)', zerolinecolor='rgba(100,108,255,0.12)'),
    yaxis=dict(gridcolor='rgba(100,108,255,0.08)', zerolinecolor='rgba(100,108,255,0.12)'),
    margin=dict(l=40, r=20, t=50, b=40),
    hoverlabel=dict(bgcolor='#1e1e48', font_size=13, font_family='Inter'),
)

RISK_COLORS = {'Good': '#00e676', 'Moderate': '#ffa726', 'Bad': '#ef5350'}

FEATURE_COLS = ['pH', 'DO', 'turbidity', 'temperature', 'conductivity',
                'nitrate', 'phosphate', 'bod', 'cod']

# ============================================================================
# CACHE AND DATA LOADING
# ============================================================================

@st.cache_resource
def load_predictor():
    """Load ML model"""
    try:
        return PollutionPredictor('model/pollution_model.pkl')
    except FileNotFoundError:
        return None


def run_batch_prediction(predictor, df):
    """Run prediction on every row of the dataframe."""
    results = []
    for _, row in df.iterrows():
        sensor = {col: row[col] for col in FEATURE_COLS}
        pred = predictor.predict(sensor)
        results.append({
            'predicted_risk': pred['pollution_risk'],
            'confidence': pred['confidence'],
            'prob_Good': pred['probabilities'].get('Good', 0),
            'prob_Moderate': pred['probabilities'].get('Moderate', 0),
            'prob_Bad': pred['probabilities'].get('Bad', 0),
        })
    return pd.DataFrame(results)


def detect_columns(df):
    """Try to auto-detect feature columns in an uploaded CSV."""
    mapping = {}
    aliases = {
        'pH': ['ph', 'ph_value', 'ph_level'],
        'DO': ['do', 'dissolved_oxygen', 'dissolved_o2', 'do_mg_l'],
        'turbidity': ['turbidity', 'turb', 'turbidity_ntu'],
        'temperature': ['temperature', 'temp', 'water_temp', 'water_temperature'],
        'conductivity': ['conductivity', 'cond', 'ec', 'electrical_conductivity'],
        'nitrate': ['nitrate', 'no3', 'nitrate_mg_l'],
        'phosphate': ['phosphate', 'po4', 'phosphate_mg_l'],
        'bod': ['bod', 'biochemical_oxygen_demand'],
        'cod': ['cod', 'chemical_oxygen_demand'],
    }
    lower_cols = {c.lower().strip(): c for c in df.columns}
    for feature, alias_list in aliases.items():
        for alias in alias_list:
            if alias in lower_cols:
                mapping[feature] = lower_cols[alias]
                break
    return mapping


def render_header(icon, title, subtitle):
    st.markdown(f"""
    <div class="glass-header">
        <h1>{icon} {title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def render_metric(icon, value, label, css_extra=""):
    st.markdown(f"""
    <div class="metric-glass {css_extra}">
        <div class="metric-icon">{icon}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application"""

    predictor = load_predictor()

    if predictor is None:
        st.error("⚠️ Model not found! Please run `python train_model.py` first.")
        st.stop()

    # Sidebar
    st.sidebar.markdown("""
    <div style="text-align:center; padding:20px 0 10px;">
        <span style="font-size:2.6em;">💧</span>
        <h2 style="color:#e0e0ff; margin:4px 0 0; font-size:1.15em; font-weight:700; letter-spacing:-0.3px;">
            AquaPredict AI
        </h2>
        <p style="color:rgba(200,210,255,0.45); font-size:0.78em; margin:2px 0 0;">
            Water Quality Intelligence
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("---")

    page = st.sidebar.radio(
        "Navigation",
        [
            "📁 Upload & Predict",
            "📊 Dashboard",
            "🔮 Manual Prediction",
            "📈 Data Analysis",
            "🗺️ GIS Map",
            "💡 Recommendations"
        ]
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="background:rgba(100,108,255,0.08); border-radius:14px; padding:16px; border:1px solid rgba(100,108,255,0.15);">
        <p style="color:rgba(200,210,255,0.55); font-size:0.82em; line-height:1.6; margin:0;">
            <b style="color:#c0c8ff;">AI-Powered</b> water quality prediction using
            ensemble ML models. Upload CSV data for instant batch predictions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ====================================================================
    # PAGE ROUTING
    # ====================================================================
    if page == "📁 Upload & Predict":
        show_upload_predict(predictor)
    elif page == "📊 Dashboard":
        show_dashboard(predictor)
    elif page == "🔮 Manual Prediction":
        show_manual_prediction(predictor)
    elif page == "📈 Data Analysis":
        show_data_analysis()
    elif page == "🗺️ GIS Map":
        show_gis_map()
    elif page == "💡 Recommendations":
        show_recommendations()


# ============================================================================
# PAGE 1: UPLOAD & PREDICT
# ============================================================================

def show_upload_predict(predictor):
    render_header("📁", "Upload CSV & Predict", "Upload your water quality sensor data and get instant AI predictions")

    # Upload zone
    st.markdown("""
    <div class="upload-zone">
        <h3>📄 Drop your CSV file here</h3>
        <p>Required columns: pH, DO, turbidity, temperature, conductivity, nitrate, phosphate, bod, cod</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload CSV",
        type=['csv'],
        label_visibility="collapsed",
        key="csv_upload"
    )

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"❌ Failed to read CSV: {e}")
            return

        st.markdown('<div class="section-title">📋 Uploaded Data Preview</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            render_metric("📊", f"{df.shape[0]:,}", "Rows")
        with col2:
            render_metric("📐", f"{df.shape[1]}", "Columns")
        with col3:
            render_metric("📄", uploaded_file.name, "File")

        st.dataframe(df.head(10), use_container_width=True, height=300)

        # Auto-detect columns
        mapping = detect_columns(df)
        missing = [f for f in FEATURE_COLS if f not in mapping]

        if missing:
            st.warning(f"⚠️ Could not auto-detect columns: **{', '.join(missing)}**. Please map them below.")

            st.markdown('<div class="section-title">🔗 Column Mapping</div>', unsafe_allow_html=True)
            cols = st.columns(3)
            for i, feat in enumerate(FEATURE_COLS):
                with cols[i % 3]:
                    default_idx = 0
                    if feat in mapping:
                        try:
                            default_idx = list(df.columns).index(mapping[feat])
                        except ValueError:
                            default_idx = 0
                    selected = st.selectbox(
                        f"{feat}",
                        options=df.columns.tolist(),
                        index=default_idx,
                        key=f"map_{feat}"
                    )
                    mapping[feat] = selected

        # Rename columns to standard names
        reverse_map = {v: k for k, v in mapping.items()}
        df_mapped = df.rename(columns=reverse_map)

        # Check all features exist
        still_missing = [f for f in FEATURE_COLS if f not in df_mapped.columns]
        if still_missing:
            st.error(f"❌ Missing required columns after mapping: {', '.join(still_missing)}")
            return

        st.markdown("---")

        # Run prediction
        if st.button("🚀 Run Batch Prediction", use_container_width=True, key="batch_predict"):
            with st.spinner("🔄 Running predictions on all rows..."):
                pred_df = run_batch_prediction(predictor, df_mapped)

            st.session_state['prediction_results'] = pred_df
            st.session_state['uploaded_data'] = df_mapped
            st.session_state['original_data'] = df
            st.success(f"✅ Predictions complete for **{len(pred_df):,}** samples!")

        # Show results if they exist
        if 'prediction_results' in st.session_state:
            pred_df = st.session_state['prediction_results']
            df_mapped = st.session_state['uploaded_data']

            st.markdown('<div class="section-title">🎯 Prediction Results</div>', unsafe_allow_html=True)

            # Summary metrics
            good = (pred_df['predicted_risk'] == 'Good').sum()
            moderate = (pred_df['predicted_risk'] == 'Moderate').sum()
            bad = (pred_df['predicted_risk'] == 'Bad').sum()
            total = len(pred_df)
            avg_conf = pred_df['confidence'].mean()

            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                render_metric("🟢", f"{good:,}", f"Good ({good/total*100:.1f}%)", "metric-good")
            with col2:
                render_metric("🟡", f"{moderate:,}", f"Moderate ({moderate/total*100:.1f}%)", "metric-moderate")
            with col3:
                render_metric("🔴", f"{bad:,}", f"Bad ({bad/total*100:.1f}%)", "metric-bad")
            with col4:
                render_metric("📊", f"{total:,}", "Total Samples")
            with col5:
                render_metric("🎯", f"{avg_conf:.1f}%", "Avg Confidence")

            st.markdown("---")

            # Charts
            col1, col2 = st.columns(2)

            with col1:
                counts = pred_df['predicted_risk'].value_counts()
                fig = px.pie(
                    values=counts.values,
                    names=counts.index,
                    color=counts.index,
                    color_discrete_map=RISK_COLORS,
                    title='Prediction Distribution',
                    hole=0.55,
                )
                fig.update_layout(**PLOTLY_LAYOUT)
                fig.update_traces(textfont_size=14, textinfo='percent+label',
                                  marker=dict(line=dict(color='#0f0c29', width=2)))
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                fig = px.histogram(
                    pred_df, x='confidence',
                    nbins=30,
                    title='Confidence Distribution',
                    color_discrete_sequence=['#646cff']
                )
                fig.update_layout(**PLOTLY_LAYOUT)
                st.plotly_chart(fig, use_container_width=True)

            # Combined dataframe for download
            result_df = pd.concat([
                st.session_state['original_data'].reset_index(drop=True),
                pred_df.reset_index(drop=True)
            ], axis=1)

            st.markdown('<div class="section-title">📋 Full Results Table</div>', unsafe_allow_html=True)
            st.dataframe(result_df, use_container_width=True, height=400)

            # Download button
            csv_data = result_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="⬇️ Download Results as CSV",
                data=csv_data,
                file_name="water_quality_predictions.csv",
                mime="text/csv",
                use_container_width=True
            )


# ============================================================================
# PAGE 2: DASHBOARD
# ============================================================================

def show_dashboard(predictor):
    render_header("📊", "Monitoring Dashboard", "Real-time water quality statistics and visualizations")

    if 'prediction_results' not in st.session_state:
        st.info("📁 **No data loaded yet.** Go to **Upload & Predict** to upload a CSV file first.")

        st.markdown("---")
        st.markdown("*Or load the built-in sample dataset for a quick demo:*")
        if st.button("📦 Load Sample Dataset", key="load_sample"):
            try:
                df = pd.read_csv('dataset/sensor_data.csv')
                pred_df = run_batch_prediction(predictor, df)
                st.session_state['prediction_results'] = pred_df
                st.session_state['uploaded_data'] = df
                st.session_state['original_data'] = df
                st.rerun()
            except FileNotFoundError:
                st.error("Sample dataset not found. Please run `python generate_dataset.py` first.")
        return

    pred_df = st.session_state['prediction_results']
    df = st.session_state['uploaded_data']

    # Key metrics row
    good = (pred_df['predicted_risk'] == 'Good').sum()
    moderate = (pred_df['predicted_risk'] == 'Moderate').sum()
    bad = (pred_df['predicted_risk'] == 'Bad').sum()
    total = len(pred_df)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_metric("🟢", f"{good:,}", f"Good · {good/total*100:.1f}%", "metric-good")
    with col2:
        render_metric("🟡", f"{moderate:,}", f"Moderate · {moderate/total*100:.1f}%", "metric-moderate")
    with col3:
        render_metric("🔴", f"{bad:,}", f"Bad · {bad/total*100:.1f}%", "metric-bad")
    with col4:
        render_metric("📍", f"{total:,}", "Total Readings")

    st.markdown("---")

    # Charts row
    col1, col2 = st.columns(2)

    with col1:
        counts = pred_df['predicted_risk'].value_counts()
        fig = px.pie(
            values=counts.values, names=counts.index,
            color=counts.index, color_discrete_map=RISK_COLORS,
            title='Risk Level Distribution', hole=0.55
        )
        fig.update_layout(**PLOTLY_LAYOUT)
        fig.update_traces(textfont_size=14, textinfo='percent+label',
                          marker=dict(line=dict(color='#0f0c29', width=2)))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Feature importance radar
        available = [c for c in FEATURE_COLS if c in df.columns]
        if available:
            means = df[available].mean()
            maxes = df[available].max()
            normalized = (means / maxes * 100).fillna(0)

            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=normalized.values.tolist() + [normalized.values[0]],
                theta=available + [available[0]],
                fill='toself',
                fillcolor='rgba(100,108,255,0.15)',
                line=dict(color='#646cff', width=2),
                name='Mean Values'
            ))
            fig.update_layout(
                **PLOTLY_LAYOUT,
                title='Parameter Overview (Normalized)',
                polar=dict(
                    bgcolor='rgba(0,0,0,0)',
                    radialaxis=dict(visible=True, gridcolor='rgba(100,108,255,0.1)',
                                    color='#c0c8ff', tickfont=dict(size=10)),
                    angularaxis=dict(gridcolor='rgba(100,108,255,0.1)', color='#c0c8ff')
                ),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Parameter statistics
    st.markdown('<div class="section-title">📊 Parameter Statistics</div>', unsafe_allow_html=True)
    available_features = [c for c in FEATURE_COLS if c in df.columns]
    if available_features:
        stats = df[available_features].describe().T.round(2)
        st.dataframe(stats, use_container_width=True)

    # Trends
    st.markdown('<div class="section-title">📈 Parameter Trends</div>', unsafe_allow_html=True)
    selected_params = st.multiselect(
        "Select parameters to visualize",
        available_features,
        default=available_features[:3] if len(available_features) >= 3 else available_features
    )

    if selected_params:
        sample = df[selected_params].reset_index(drop=True).head(500)
        fig = px.line(
            sample, title='Parameter Trends (first 500 readings)',
            markers=False,
            color_discrete_sequence=['#646cff', '#00e676', '#ffa726', '#ef5350', '#00bcd4',
                                     '#ab47bc', '#ffee58', '#8d6e63', '#78909c']
        )
        fig.update_layout(**PLOTLY_LAYOUT, hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)


# ============================================================================
# PAGE 3: MANUAL PREDICTION
# ============================================================================

def show_manual_prediction(predictor):
    render_header("🔮", "Manual Prediction", "Enter sensor readings to predict water pollution risk")

    st.markdown('<div class="section-title">🎛️ Sensor Input Parameters</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**pH & Oxygen**")
        pH = st.slider("pH", 4.0, 10.0, 7.0, 0.1, key="m_ph")
        DO = st.slider("Dissolved Oxygen (mg/L)", 0.0, 12.0, 6.5, 0.1, key="m_do")
        turbidity = st.slider("Turbidity (NTU)", 0.0, 50.0, 2.0, 0.5, key="m_turb")

    with col2:
        st.markdown("**Temperature & Conductivity**")
        temperature = st.slider("Temperature (°C)", 2.0, 28.0, 15.0, 0.5, key="m_temp")
        conductivity = st.slider("Conductivity (µS/cm)", 100.0, 1500.0, 500.0, 10.0, key="m_cond")
        nitrate = st.slider("Nitrate (mg/L)", 0.0, 30.0, 3.0, 0.5, key="m_nitrate")

    with col3:
        st.markdown("**Nutrients & Organic**")
        phosphate = st.slider("Phosphate (mg/L)", 0.0, 5.0, 0.2, 0.05, key="m_phos")
        bod = st.slider("BOD (mg/L)", 0.0, 20.0, 2.0, 0.5, key="m_bod")
        cod = st.slider("COD (mg/L)", 0.0, 80.0, 10.0, 1.0, key="m_cod")

    if st.button("🔮 Predict Pollution Risk", use_container_width=True, key="predict_manual"):
        sensor_data = {
            'pH': pH, 'DO': DO, 'turbidity': turbidity,
            'temperature': temperature, 'conductivity': conductivity,
            'nitrate': nitrate, 'phosphate': phosphate,
            'bod': bod, 'cod': cod
        }

        result = predictor.predict(sensor_data)

        st.markdown("---")
        risk = result['pollution_risk']
        css_class = {'Good': 'result-good', 'Moderate': 'result-moderate', 'Bad': 'result-bad'}.get(risk, '')
        emoji = {'Good': '✅', 'Moderate': '⚠️', 'Bad': '🚨'}.get(risk, '')

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown(f"""
            <div class="result-card {css_class}">
                <h2>{emoji} {risk.upper()} RISK</h2>
                <p>Confidence: <b>{result['confidence']}%</b></p>
                <p>Model: {result['model_used']}</p>
            </div>
            """, unsafe_allow_html=True)

            if risk == 'Good':
                st.success("✅ Water quality is GOOD. No action required.")
            elif risk == 'Moderate':
                st.warning("⚠️ Water quality is MODERATE. Increase monitoring frequency.")
            else:
                st.error("🚨 Water quality is BAD. Activate emergency response immediately.")

        with col2:
            probs = result['probabilities']
            fig = go.Figure(go.Bar(
                x=list(probs.keys()),
                y=list(probs.values()),
                marker_color=[RISK_COLORS.get(k, '#646cff') for k in probs.keys()],
                text=[f"{v:.1f}%" for v in probs.values()],
                textposition='auto',
                textfont=dict(color='white', size=14)
            ))
            fig.update_layout(**PLOTLY_LAYOUT, title='Prediction Confidence',
                              xaxis_title='Risk Level', yaxis_title='Probability (%)')
            st.plotly_chart(fig, use_container_width=True)


# ============================================================================
# PAGE 4: DATA ANALYSIS
# ============================================================================

def show_data_analysis():
    render_header("📈", "Data Analysis", "Explore patterns and correlations in your uploaded data")

    if 'uploaded_data' not in st.session_state or 'prediction_results' not in st.session_state:
        st.info("📁 **No data loaded.** Go to **Upload & Predict** to upload a CSV file first.")
        return

    df = st.session_state['uploaded_data']
    pred_df = st.session_state['prediction_results']
    df_with_pred = pd.concat([df.reset_index(drop=True), pred_df.reset_index(drop=True)], axis=1)

    available = [c for c in FEATURE_COLS if c in df.columns]

    # Box plot by risk level
    st.markdown('<div class="section-title">📦 Parameters by Risk Level</div>', unsafe_allow_html=True)
    selected_param = st.selectbox("Select Parameter", available, key="box_param")

    if selected_param:
        fig = px.box(
            df_with_pred, x='predicted_risk', y=selected_param,
            color='predicted_risk', color_discrete_map=RISK_COLORS,
            title=f'{selected_param} Distribution by Predicted Risk'
        )
        fig.update_layout(**PLOTLY_LAYOUT, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Correlation heatmap
    st.markdown('<div class="section-title">🔥 Correlation Heatmap</div>', unsafe_allow_html=True)
    if available:
        corr = df[available].corr()
        fig = px.imshow(
            corr, text_auto='.2f',
            color_continuous_scale=[[0, '#0f0c29'], [0.5, '#646cff'], [1, '#ff6b6b']],
            title='Feature Correlations',
            aspect='auto'
        )
        fig.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Scatter matrix
    st.markdown('<div class="section-title">🔍 Scatter Plot</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        x_feat = st.selectbox("X axis", available, index=0, key="scatter_x")
    with col2:
        y_feat = st.selectbox("Y axis", available, index=min(1, len(available) - 1), key="scatter_y")

    fig = px.scatter(
        df_with_pred, x=x_feat, y=y_feat,
        color='predicted_risk', color_discrete_map=RISK_COLORS,
        title=f'{x_feat} vs {y_feat}',
        opacity=0.6
    )
    fig.update_layout(**PLOTLY_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)


# ============================================================================
# PAGE 5: GIS MAP
# ============================================================================

def show_gis_map():
    render_header("🗺️", "GIS Pollution Map", "Interactive map showing sensor locations and pollution levels")

    if 'uploaded_data' not in st.session_state or 'prediction_results' not in st.session_state:
        st.info("📁 **No data loaded.** Go to **Upload & Predict** to upload a CSV file first.")
        return

    df = st.session_state['uploaded_data']
    pred_df = st.session_state['prediction_results']

    # Check for lat/lon columns
    lat_col = None
    lon_col = None
    for c in df.columns:
        cl = c.lower()
        if cl in ['latitude', 'lat']:
            lat_col = c
        elif cl in ['longitude', 'lon', 'long', 'lng']:
            lon_col = c

    if lat_col is None or lon_col is None:
        st.warning("🗺️ **No geographic coordinates found** in the uploaded data. "
                    "The CSV needs `latitude` and `longitude` columns for map visualization.")
        st.info("💡 Tip: Add columns named `latitude` and `longitude` to your CSV to enable the map.")
        return

    try:
        import folium
        from streamlit_folium import st_folium
    except ImportError:
        st.error("Please install folium and streamlit-folium: `pip install folium streamlit-folium`")
        return

    df_map = pd.concat([df.reset_index(drop=True), pred_df.reset_index(drop=True)], axis=1)

    mean_lat = df_map[lat_col].mean()
    mean_lon = df_map[lon_col].mean()

    map_obj = folium.Map(
        location=[mean_lat, mean_lon],
        zoom_start=12,
        tiles='CartoDB dark_matter'
    )

    sample_size = min(300, len(df_map))
    sample = df_map.sample(sample_size, random_state=42)

    folium_colors = {'Good': 'green', 'Moderate': 'orange', 'Bad': 'red'}

    for _, row in sample.iterrows():
        risk = row.get('predicted_risk', 'Good')
        color = folium_colors.get(risk, 'gray')
        popup_parts = [f"<b>Risk: {risk}</b><br>"]
        for feat in FEATURE_COLS:
            if feat in row.index:
                popup_parts.append(f"{feat}: {row[feat]}<br>")

        folium.CircleMarker(
            location=[row[lat_col], row[lon_col]],
            radius=6,
            popup=folium.Popup("".join(popup_parts), max_width=250),
            color=color, fill=True, fillColor=color,
            fillOpacity=0.7, weight=2
        ).add_to(map_obj)

    st_folium(map_obj, width=1200, height=600)

    st.markdown("""
    <div style="background:rgba(255,255,255,0.04); border-radius:12px; padding:16px; margin-top:12px;
                border:1px solid rgba(255,255,255,0.06); text-align:center;">
        <span style="color:#00e676;">🟢 Good</span> &nbsp;&nbsp;|&nbsp;&nbsp;
        <span style="color:#ffa726;">🟡 Moderate</span> &nbsp;&nbsp;|&nbsp;&nbsp;
        <span style="color:#ef5350;">🔴 Bad</span>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# PAGE 6: RECOMMENDATIONS
# ============================================================================

def show_recommendations():
    render_header("💡", "Mitigation Recommendations", "AI-powered action plans based on water quality data")

    st.markdown('<div class="section-title">🎛️ Custom Scenario Analysis</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        risk = st.selectbox("Pollution Risk Level", ["Good", "Moderate", "Bad"], key="rec_risk")
    with col2:
        turbidity = st.number_input("Turbidity (NTU)", 0.0, 50.0, 5.0, key="rec_turb")
    with col3:
        DO = st.number_input("Dissolved Oxygen (mg/L)", 0.0, 12.0, 6.0, key="rec_do")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        nitrate = st.number_input("Nitrate (mg/L)", 0.0, 30.0, 5.0, key="rec_nitrate")
    with col2:
        phosphate = st.number_input("Phosphate (mg/L)", 0.0, 5.0, 0.5, key="rec_phos")
    with col3:
        bod = st.number_input("BOD (mg/L)", 0.0, 20.0, 3.0, key="rec_bod")
    with col4:
        cod = st.number_input("COD (mg/L)", 0.0, 80.0, 15.0, key="rec_cod")

    if st.button("💡 Generate Recommendations", use_container_width=True, key="gen_rec"):
        sensor_data = {
            'pollution_risk': risk,
            'turbidity': turbidity, 'DO': DO,
            'nitrate': nitrate, 'phosphate': phosphate,
            'bod': bod, 'cod': cod,
            'pH': 7.0, 'temperature': 15.0, 'conductivity': 500.0
        }

        recommendations = MitigationRecommender.recommend(sensor_data)

        st.markdown("---")
        st.markdown('<div class="section-title">🎯 Action Plan</div>', unsafe_allow_html=True)

        for rec in recommendations:
            if 'action' in rec:
                st.markdown(f"""
                <div class="rec-card">
                    <h4>{rec.get('priority', '')} {rec.get('category', '')}</h4>
                    <p><b>{rec.get('action', '')}</b><br>{rec.get('details', '')}</p>
                </div>
                """, unsafe_allow_html=True)
            elif 'issue' in rec:
                st.markdown(f"""
                <div class="rec-card">
                    <h4>{rec.get('priority', '')} {rec.get('parameter', '')} — {rec.get('issue', '')}</h4>
                    <p>Current Value: <b>{rec.get('value', 'N/A')}</b></p>
                </div>
                """, unsafe_allow_html=True)

                if 'recommendations' in rec:
                    for j, r in enumerate(rec['recommendations'], 1):
                        st.markdown(f"""
                        <div style="background:rgba(100,108,255,0.04); border-radius:10px; padding:10px 16px;
                                    margin:4px 0 4px 20px; border:1px solid rgba(100,108,255,0.08);">
                            <span style="color:rgba(200,210,255,0.7); font-size:0.9em;">{j}. {r}</span>
                        </div>
                        """, unsafe_allow_html=True)


# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    main()
