import streamlit as st
import plotly.graph_objects as go

def render_gauge_chart(score: float):
    """Renders a visually appealing gauge chart for the ATS score."""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "ATS Match Score", 'font': {'size': 24}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#4CAF50" if score >= 75 else ("#FFC107" if score >= 50 else "#F44336")},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': '#FFEBEE'},
                {'range': [50, 75], 'color': '#FFF8E1'},
                {'range': [75, 100], 'color': '#E8F5E9'}],
        }
    ))
    
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig, use_container_width=True)

def render_feedback(matched: list, missing: list, suggestions: list):
    """Displays the feedback sections beautifully."""
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("✅ Matched Skills")
        if matched:
            st.success(", ".join(matched))
        else:
            st.warning("No specific skills matched.")
            
    with col2:
        st.subheader("❌ Missing Skills")
        if missing:
            st.error(", ".join(missing[:20]) + ("..." if len(missing) > 20 else ""))
        else:
            st.success("You matched all key skills!")

    if suggestions:
        st.subheader("💡 Improvement Suggestions")
        for suggestion in suggestions:
            st.info(suggestion)
