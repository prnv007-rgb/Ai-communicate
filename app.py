import streamlit as st
from scorer import RubricScorer
import json

# Page Configuration
st.set_page_config(
    page_title="AI Communication Coach",
    page_icon="🗣️",
    layout="wide"
)

# Title and Description
st.title("🗣️ AI Communication Coach")
st.markdown("""
This tool analyzes spoken communication transcripts based on a comprehensive rubric covering:
- **Content & Structure**: Salutation, Keywords, Flow
- **Speech Rate**: Words per minute analysis
- **Language Quality**: Grammar and Vocabulary
- **Delivery**: Clarity (filler words) and Engagement (sentiment)
""")

# Sidebar with Instructions
with st.sidebar:
    st.header("📋 Instructions")
    st.markdown("""
    1. Paste your self-introduction transcript
    2. Enter the audio duration in seconds
    3. Click **Analyze Score** to get results
    
    **Sample Duration**: 52 seconds
    """)
    
    st.header("📊 Scoring Breakdown")
    st.markdown("""
    - Salutation: 5 points
    - Keywords: 30 points
    - Flow: 5 points
    - Speech Rate: 10 points
    - Grammar: 10 points
    - Vocabulary: 10 points
    - Clarity: 15 points
    - Engagement: 15 points
    
    **Total**: 100 points
    """)

# Main Input Section
st.header(" Input Transcript")
transcript = st.text_area(
    "Paste the transcript here:",
    height=250,
    placeholder="Hello everyone, myself John. I am studying in class 8th...",
    help="Enter the complete self-introduction transcript"
)

col1, col2 = st.columns([3, 1])
with col1:
    duration = st.number_input(
        "Audio Duration (seconds):",
        min_value=1,
        max_value=300,
        value=52,
        help="Duration of the audio recording in seconds"
    )
with col2:
    st.write("")  
    st.write("")  
    analyze_button = st.button(" Analyze Score", type="primary", use_container_width=True)

# Analysis Section
if analyze_button:
    if transcript.strip():
        with st.spinner("Analyzing transcript..."):
            # Initialize scorer
            scorer = RubricScorer()
            results = scorer.analyze(transcript, duration)
        
        # Success message
        st.success(" Analysis Complete!")
        
        # Overall Score - Big Display
        st.markdown("---")
        col_score = st.columns([1, 2, 1])
        with col_score[1]:
            st.markdown(f"""
            <div style='text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px;'>
                <h1 style='color: #0066cc; margin: 0;'>{results['overall_score']}/100</h1>
                <p style='font-size: 18px; color: #666; margin: 0;'>Overall Score</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Detailed Metrics in Cards
        st.header(" Detailed Breakdown")
        
        # Row 1: Content & Structure
        st.subheader(" Content & Structure (40 points)")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Salutation",
                f"{results['metrics']['Salutation']}/5",
                help=results['feedback']['Salutation']
            )
            st.caption(results['feedback']['Salutation'])
        
        with col2:
            st.metric(
                "Keywords",
                f"{results['metrics']['Keywords']}/30",
                help=results['feedback']['Keywords']
            )
            st.caption(results['feedback']['Keywords'])
        
        with col3:
            st.metric(
                "Flow",
                f"{results['metrics']['Flow']}/5",
                help=results['feedback']['Flow']
            )
            st.caption(results['feedback']['Flow'])
        
        st.markdown("---")
        
        # Row 2: Speech Rate
        st.subheader(" Speech Rate (10 points)")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                "Speech Rate Score",
                f"{results['metrics']['Speech Rate']}/10"
            )
            st.caption(results['feedback']['Speech Rate'])
        
        with col2:
            st.metric(
                "Words Per Minute",
                results['details']['wpm']
            )
            st.caption("Ideal range: 111-140 WPM")
        
        st.markdown("---")
        
        # Row 3: Language & Grammar
        st.subheader(" Language & Grammar (20 points)")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                "Grammar",
                f"{results['metrics']['Grammar']}/10"
            )
            st.caption(results['feedback']['Grammar'])
        
        with col2:
            st.metric(
                "Vocabulary (TTR)",
                f"{results['metrics']['Vocabulary']}/10"
            )
            st.caption(results['feedback']['Vocabulary'])
        
        st.markdown("---")
        
        # Row 4: Clarity & Engagement
        st.subheader(" Clarity & Engagement (30 points)")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                "Clarity",
                f"{results['metrics']['Clarity']}/15"
            )
            st.caption(results['feedback']['Clarity'])
        
        with col2:
            st.metric(
                "Engagement",
                f"{results['metrics']['Engagement']}/15"
            )
            st.caption(results['feedback']['Engagement'])
        
        st.markdown("---")
        
        # Additional Details
        with st.expander(" View Additional Details"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write("**Word Count:**", results['details']['word_count'])
                st.write("**Filler Words:**", results['details']['filler_count'])
            
            with col2:
                st.write("**TTR Score:**", results['details']['ttr'])
                st.write("**Positive Sentiment:**", results['details']['sentiment_positive'])
                st.write("**Compound Sentiment:**", results['details']['sentiment_compound'])
            
            with col3:
                st.write("**Duration:**", f"{duration}s")
                st.write("**WPM:**", results['details']['wpm'])
        
        # Raw JSON Output (for debugging/verification)
        with st.expander(" View Raw JSON Output"):
            st.json(results)
        
        # Download Results
        st.markdown("---")
        st.download_button(
            label="📥 Download Results as JSON",
            data=json.dumps(results, indent=2),
            file_name="communication_analysis.json",
            mime="application/json"
        )
        
    else:
        st.warning("⚠️ Please enter a transcript to analyze.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>Built with Streamlit | Powered by NLP & AI</p>
</div>
""", unsafe_allow_html=True)