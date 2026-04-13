import streamlit as st
import plotly.graph_objects as go

def render_gauge_chart(score: float):
    """Renders a visually appealing gauge chart for the ATS score."""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Overall ATS Score", 'font': {'size': 24, 'color': '#ffffff' if st.get_option('theme.base') == 'dark' else '#000000'}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#4CAF50" if score >= 75 else ("#FFC107" if score >= 50 else "#F44336")},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': 'rgba(255, 0, 0, 0.1)'},
                {'range': [50, 75], 'color': 'rgba(255, 165, 0, 0.1)'},
                {'range': [75, 100], 'color': 'rgba(0, 128, 0, 0.1)'}],
        }
    ))
    
    fig.update_layout(height=350, margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor="rgba(0,0,0,0)", font={'color': 'gray'})
    st.plotly_chart(fig, use_container_width=True)

def render_score_breakdown(breakdown: dict, semantic_sim: float):
    """Renders score breakdown with progress bars."""
    st.subheader("📊 Score Breakdown")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Keyword Match (40%)**")
        st.progress(breakdown.get("keyword_match", 0) / 40.0)
        st.caption(f"{breakdown.get('keyword_match', 0)} / 40 pts")

        st.markdown("**Experience Relevance (20%)**")
        st.progress(breakdown.get("experience_relevance", 0) / 20.0)
        st.caption(f"{breakdown.get('experience_relevance', 0)} / 20 pts")
        
    with col2:
        st.markdown("**Semantic Fit (30%)**")
        st.progress(breakdown.get("semantic_match", 0) / 30.0)
        st.caption(f"{breakdown.get('semantic_match', 0)} / 30 pts (Raw similarity: {semantic_sim:.2f})")
        
        st.markdown("**Formatting (10%)**")
        st.progress(breakdown.get("formatting", 0) / 10.0)
        st.caption(f"{breakdown.get('formatting', 0)} / 10 pts")

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
        st.subheader("💡 General Suggestions")
        for suggestion in suggestions:
            st.info(suggestion)

def render_llm_improvements(improvements: dict):
    if "error" in improvements:
        st.warning("AI Improvement unavailable: " + improvements["error"])
        return
        
    st.subheader("✨ AI-Powered Resume Improvements")
    
    # Render Action Verbs
    if "action_verbs" in improvements:
        st.markdown("**Recommended Strong Action Verbs:**")
        verbs_html = " ".join([f"<span style='background-color:#007BFF; color:white; padding:4px 8px; border-radius:12px; margin:2px; display:inline-block; font-size:12px;'>{verb}</span>" for verb in improvements["action_verbs"]])
        st.markdown(verbs_html, unsafe_allow_html=True)
        st.write("")
        
    if "improvements" in improvements:
        for idx, imp in enumerate(improvements["improvements"]):
            with st.expander(f"Improvement {idx+1} - {imp.get('section', 'General')}"):
                st.write(imp.get('suggestion', ''))

def render_skill_roadmap(roadmap_data: dict):
    if "error" in roadmap_data:+
        st.warning("Roadmap unavailable: " + roadmap_data["error"])
        return
        
    if "roadmap" not in roadmap_data or not roadmap_data["roadmap"]:
        st.info("No roadmap generated. You are well equipped for this role!")
        return

    st.subheader("🗺️ Skill Gap Learning Roadmap")
    
    tabs = st.tabs([step.get("level", "Step") for step in roadmap_data["roadmap"]])
    
    for i, step in enumerate(roadmap_data["roadmap"]):
        with tabs[i]:
            st.markdown(f"### {step.get('level')} Level")
            st.markdown("**Topics:** " + ", ".join(step.get('topics', [])))
            st.markdown("**Tools:** " + ", ".join(step.get('tools', [])))
            st.markdown("**Suggested Project:**")
            st.info(step.get('suggested_project', 'No project suggested.'))
