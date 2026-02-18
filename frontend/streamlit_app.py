"""
Streamlit Frontend
Simple dashboard for the Neuro-Cognitive Adaptive Learning System
"""

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from typing import Dict

# Configuration
API_BASE_URL = "http://localhost:8000/api/v1"

st.set_page_config(
    page_title="Adaptive Learning Dashboard",
    page_icon="🧠",
    layout="wide"
)

# Title
st.title("🧠 AI-Enabled Neuro-Cognitive Adaptive Learning")
st.markdown("---")

# Sidebar - User Profile
st.sidebar.header("User Profile")
user_id = st.sidebar.text_input("User ID", value="demo_user_123")

# Tab Navigation
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Dashboard", 
    "🎯 Assessment", 
    "📚 Recommendations", 
    "⚙️ Adaptation"
])

# Tab 1: Dashboard
with tab1:
    st.header("Learning Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Learning Sessions", "24", "+3")
    with col2:
        st.metric("Average Score", "78.5%", "+5.2%")
    with col3:
        st.metric("Engagement Level", "82%", "+7%")
    with col4:
        st.metric("Streak Days", "7", "+1")
    
    st.markdown("### Learning Progress")
    
    # Mock progress data
    progress_data = {
        "Module": ["Python Basics", "Data Structures", "OOP", "Algorithms"],
        "Progress": [100, 75, 45, 10]
    }
    df = pd.DataFrame(progress_data)
    
    fig = go.Figure(data=[
        go.Bar(x=df["Module"], y=df["Progress"], marker_color='lightblue')
    ])
    fig.update_layout(
        title="Module Completion Progress",
        xaxis_title="Module",
        yaxis_title="Completion %",
        yaxis=dict(range=[0, 100])
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Learning Style
    st.markdown("### Your Learning Profile")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("**Dominant Learning Style:** Visual")
        st.info("**Cognitive Load Capacity:** 7.5/10")
        st.info("**Processing Speed:** Fast")
    
    with col2:
        st.success("**Strengths:**")
        st.write("• High cognitive load capacity")
        st.write("• Fast information processing")
        st.write("• Strong visual learning")

# Tab 2: Assessment
with tab2:
    st.header("Cognitive Assessment")
    
    st.markdown("### VARK Learning Style Assessment")
    
    with st.form("vark_form"):
        st.write("Answer the following questions to determine your learning style:")
        
        q1 = st.radio(
            "1. How do you prefer to learn new concepts?",
            ["Visual diagrams and charts", "Audio lectures", "Reading text", "Hands-on practice"]
        )
        
        q2 = st.radio(
            "2. When studying, you prefer to:",
            ["Watch videos", "Listen to explanations", "Read detailed notes", "Do exercises"]
        )
        
        q3 = st.radio(
            "3. You remember things best by:",
            ["Seeing images", "Hearing information", "Reading about them", "Doing activities"]
        )
        
        submitted = st.form_submit_button("Submit Assessment")
        
        if submitted:
            # Map responses to VARK categories
            responses = []
            for answer in [q1, q2, q3]:
                if "Visual" in answer or "Watch" in answer or "Seeing" in answer:
                    responses.append({"preferred_modality": "visual"})
                elif "Audio" in answer or "Listen" in answer or "Hearing" in answer:
                    responses.append({"preferred_modality": "auditory"})
                elif "Reading" in answer or "Read" in answer:
                    responses.append({"preferred_modality": "reading_writing"})
                else:
                    responses.append({"preferred_modality": "kinesthetic"})
            
            # Call API (mock for demo)
            st.success("✅ Assessment completed!")
            
            # Display results
            vark_scores = {
                "Visual": 0.6,
                "Auditory": 0.2,
                "Reading/Writing": 0.1,
                "Kinesthetic": 0.1
            }
            
            fig = go.Figure(data=[
                go.Bar(x=list(vark_scores.keys()), y=list(vark_scores.values()))
            ])
            fig.update_layout(
                title="Your VARK Learning Style Profile",
                xaxis_title="Learning Style",
                yaxis_title="Score",
                yaxis=dict(range=[0, 1])
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.info("**Result:** You are primarily a **Visual** learner!")

# Tab 3: Recommendations
with tab3:
    st.header("Personalized Recommendations")
    
    if st.button("Get Recommendations"):
        st.markdown("### 📚 Recommended Content")
        
        recommendations = [
            {
                "title": "Python Data Visualization",
                "type": "Interactive Tutorial",
                "difficulty": "Intermediate",
                "duration": "45 min",
                "relevance": 0.92
            },
            {
                "title": "Algorithmic Thinking",
                "type": "Video Course",
                "difficulty": "Intermediate",
                "duration": "60 min",
                "relevance": 0.88
            },
            {
                "title": "Object-Oriented Design Patterns",
                "type": "Text + Exercises",
                "difficulty": "Advanced",
                "duration": "90 min",
                "relevance": 0.85
            }
        ]
        
        for rec in recommendations:
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.subheader(rec["title"])
                    st.write(f"**Type:** {rec['type']}")
                    st.write(f"**Difficulty:** {rec['difficulty']} | **Duration:** {rec['duration']}")
                    st.progress(rec["relevance"])
                    st.caption(f"Relevance: {rec['relevance']*100:.0f}%")
                
                with col2:
                    st.button("Start Learning", key=rec["title"])
                
                st.markdown("---")

# Tab 4: Adaptation
with tab4:
    st.header("Adaptive Learning Controls")
    
    st.markdown("### Performance Metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        performance = st.slider("Recent Performance Score", 0.0, 1.0, 0.75, 0.05)
        engagement = st.slider("Engagement Level", 0.0, 1.0, 0.80, 0.05)
        error_rate = st.slider("Error Rate", 0.0, 1.0, 0.20, 0.05)
    
    with col2:
        current_difficulty = st.selectbox(
            "Current Difficulty Level",
            ["beginner", "intermediate", "advanced", "expert"]
        )
    
    if st.button("Adjust Difficulty"):
        st.markdown("### 🎯 Adaptation Results")
        
        # Mock adaptation response
        if performance > 0.7 and engagement > 0.7:
            st.success("✅ **Recommended Action:** Increase difficulty to Advanced")
            st.write("Your strong performance indicates you're ready for more challenging content!")
        elif performance < 0.5 or engagement < 0.4:
            st.warning("⚠️ **Recommended Action:** Decrease difficulty to Beginner")
            st.write("Let's focus on building stronger foundations with easier content.")
        else:
            st.info("ℹ️ **Recommended Action:** Maintain current difficulty")
            st.write("You're at the right level. Keep up the good work!")
        
        st.markdown("### 📝 Personalized Recommendations")
        st.write("• Incorporate more visual diagrams and charts")
        st.write("• Add progress checkpoints and breaks")
        st.write("• Include hands-on practice exercises")
    
    # Cognitive Load Calculator
    st.markdown("---")
    st.markdown("### 🧠 Cognitive Load Calculator")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        task_complexity = st.slider("Task Complexity", 1, 10, 5)
    with col2:
        user_capacity = st.slider("Your Capacity", 0.0, 10.0, 6.5, 0.5)
    with col3:
        time_pressure = st.slider("Time Pressure", 0.0, 1.0, 0.5, 0.1)
    
    if st.button("Calculate Load"):
        # Simple calculation
        load = (task_complexity / max(user_capacity, 1)) * (1 + time_pressure)
        load = min(load, 10)
        
        st.metric("Estimated Cognitive Load", f"{load:.1f}/10")
        
        if load > 7:
            st.error("⚠️ High cognitive load - consider reducing complexity")
        elif load > 4:
            st.success("✅ Moderate load - appropriate challenge level")
        else:
            st.info("💡 Low load - you can handle more complexity")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center'>Made by KRISH JOSHI with 🧠 and ❤️ | "
    "AI-Enabled Neuro-Cognitive Adaptive Learning Framework</div>",
    unsafe_allow_html=True
)
