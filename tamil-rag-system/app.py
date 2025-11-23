"""
Tamil Textbook RAG System - Streamlit UI
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Tamil Textbook RAG",
    page_icon="📚",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Tamil:wght@400;700&display=swap');
    
    .blue-header {
        background: linear-gradient(135deg, #1565C0 0%, #1E88E5 100%);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .header-title {
        color: white;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin: 0;
    }
    .header-subtitle {
        color: #E3F2FD;
        font-size: 1rem;
        text-align: center;
        margin-top: 10px;
    }
    .tamil-text {
        font-family: 'Noto Sans Tamil', sans-serif;
        font-size: 1.2rem;
        line-height: 2;
    }
    .source-box {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
    .stTextArea textarea {
        font-family: 'Noto Sans Tamil', sans-serif;
        font-size: 1.1rem;
    }
    .stTextInput input {
        font-family: 'Noto Sans Tamil', sans-serif;
        font-size: 1.1rem;
    }
</style>
<script>
    const doc = window.parent.document;
    doc.addEventListener('keydown', function(e) {
        const activeElement = doc.activeElement;
        if (e.key === 'Enter' && activeElement.tagName === 'INPUT' && !e.shiftKey && !e.ctrlKey) {
            e.preventDefault();
            const buttons = doc.querySelectorAll('button[kind="primary"]');
            if (buttons.length > 0) {
                buttons[0].click();
            }
        }
    });
</script>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="blue-header">
    <p class="header-title">📚 Tamil Textbook RAG System</p>
    <p class="header-subtitle">Zero-Hallucination Q&A for Samacheer Kalvi Tamil Textbooks | Year 6-10</p>
</div>
""", unsafe_allow_html=True)

# Initialize RAG Engine
@st.cache_resource(show_spinner="Loading RAG Engine...")
def get_rag_engine():
    from src.retrieval.rag_engine import RAGEngine
    return RAGEngine()

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    grade_filter = st.selectbox(
        "Filter by Grade",
        options=[None, 6, 7, 8, 9, 10],
        format_func=lambda x: "All Grades" if x is None else f"Year {x}",
        index=0
    )
    
    top_k = st.slider("Number of sources", min_value=1, max_value=10, value=3)
    
    st.divider()
    
    st.header("📊 System Info")
    
    try:
        engine = get_rag_engine()
        stats = engine.mg.get_stats()
        st.metric("Total Nodes", stats.get("nodes", 0))
        st.metric("Total Relationships", stats.get("relationships", 0))
        st.success("✅ Connected to Memgraph")
    except Exception as e:
        st.error(f"❌ Error: {e}")
    
    st.divider()
    
    st.markdown("### 💡 Sample Questions")
    st.markdown("""
    - தமிழ் மொழி பற்றி சொல்லுங்கள்
    - What is this textbook about?
    - Tell me about mathematics
    - Explain photosynthesis
    """)

# Main content
st.markdown("### 🔍 Ask a question (Tamil or English):")

# Initialize session state for question
if 'last_question' not in st.session_state:
    st.session_state.last_question = ""
if 'input_key' not in st.session_state:
    st.session_state.input_key = 0

# Use text_input instead of text_area for Enter key support
question = st.text_input(
    label="Question",
    label_visibility="collapsed",
    placeholder="உங்கள் கேள்வியை இங்கே தட்டச்சு செய்யவும் / Type your question here...",
    key=f"question_input_{st.session_state.input_key}"
)

search_button = st.button("🔎 Search", type="primary", use_container_width=True)

# Process query
if search_button and question:
    st.session_state.last_question = question
    st.session_state.input_key += 1  # Change key to clear input
    st.rerun()

if st.session_state.last_question:
    with st.spinner("🔄 Searching textbooks..."):
        try:
            engine = get_rag_engine()
            result = engine.query(st.session_state.last_question, top_k=top_k, grade=grade_filter)
            
            if result is None:
                st.error("No result returned from query")
            else:
                # Display question
                st.divider()
                st.markdown("### ❓ Question")
                st.markdown(f'<div class="tamil-text"><strong>{st.session_state.last_question}</strong></div>', unsafe_allow_html=True)
                
                # Display answer
                st.markdown("### 📖 Answer")
                
                answer = result.get("answer", "No answer available")
                st.markdown(f'<div class="tamil-text">{answer}</div>', unsafe_allow_html=True)
                
                # Display sources
                st.divider()
                st.subheader("📚 Sources")
                
                sources = result.get("sources", [])
                if sources:
                    for src in sources:
                        if src is None:
                            continue
                        grade = src.get('grade', 'N/A')
                        term = src.get('term', 'N/A')
                        page = src.get('page', 'N/A')
                        subject = src.get('subject', 'N/A')
                        chunk_id = src.get('chunk_id', 'N/A')
                        content_type = src.get('content_type', 'text')
                        
                        # Different icon for images vs text
                        icon = "🖼️" if content_type == 'image' else "📄"
                        type_label = "Image" if content_type == 'image' else "Text"
                        
                        st.markdown(f"""
                        <div class="source-box">
                            <strong>{icon} Source {src.get('source_id', 'N/A')} ({type_label})</strong><br>
                            Grade: {grade} | Term: {term} | Subject: {subject} | Page: {page}<br>
                            <small>Chunk ID: {chunk_id}</small>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("No sources found.")
                
                # Metrics
                st.divider()
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    conf = result.get("confidence", 0) or 0
                    st.metric("Confidence", f"{conf * 100:.1f}%")
                
                with col2:
                    usage = result.get("usage", {}) or {}
                    tokens = usage.get("total_tokens", 0) or 0
                    st.metric("Tokens Used", tokens)
                
                with col3:
                    st.metric("Sources Found", len(sources))
                    
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            import traceback
            st.code(traceback.format_exc())

# Footer
st.divider()
st.markdown("""
<p style="text-align: center; color: #999; font-size: 0.8rem;">
    Built with ❤️ using Memgraph, OpenAI, and Streamlit<br>
    Zero-Hallucination RAG for Tamil Education
</p>
""", unsafe_allow_html=True)