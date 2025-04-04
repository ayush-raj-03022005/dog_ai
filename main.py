import streamlit as st
import requests
import json
import time
import logging

# Set page config FIRST - must be the first Streamlit command
st.set_page_config(
    page_title="🐾 Professional Dog Training Assistant",
    page_icon="🐕",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme using Streamlit's native color variables
st.markdown("""
<style>
    /* Base dark theme */
    .stApp {
        background-color: var(--default-backgroundColor);
        color: var(--default-textColor);
    }
    
    /* Chat messages */
    .stChatMessage {
        border-radius: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    
    [data-testid="stChatMessage"][aria-label="user"] {
        background-color: var(--default-secondaryBackgroundColor);
        border: 1px solid var(--default-borderColor);
    }
    
    [data-testid="stChatMessage"][aria-label="assistant"] {
        background-color: var(--default-primaryColor);
        border: 1px solid var(--default-borderColor);
        color: var(--default-textColor);
    }
    
    /* Sidebar */
    .st-emotion-cache-6qob1r {
        background: var(--default-secondaryBackgroundColor) !important;
        border-right: 1px solid var(--default-borderColor);
    }
    
    /* Badges */
    .badge {
        padding: 4px 12px;
        border-radius: 20px;
        background: var(--default-primaryColor);
        color: var(--default-textColor) !important;
        border: 1px solid var(--default-borderColor);
        margin: 4px;
        display: inline-block;
        font-size: 0.85em;
    }
    
    /* Feature cards */
    .feature-card {
        background: var(--default-secondaryBackgroundColor) !important;
        border: 1px solid var(--default-borderColor);
        border-radius: 12px;
        padding: 16px;
        margin: 8px;
        text-align: center;
        transition: transform 0.2s;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
    }
    
    /* Input fields */
    .stTextInput input, .stSelectbox select {
        background: var(--default-secondaryBackgroundColor) !important;
        color: var(--default-textColor) !important;
        border: 1px solid var(--default-borderColor) !important;
    }
    
    /* Slider */
    .stSlider .st-ae {
        background: var(--default-borderColor);
    }
    
    /* Progress spinner */
    .stSpinner > div {
        border-color: var(--default-primaryColor) transparent transparent transparent !important;
    }
    
    /* Error messages */
    .stAlert {
        background: var(--default-secondaryBackgroundColor) !important;
        border: 1px solid var(--default-borderColor) !important;
    }
    
    /* Links */
    a {
        color: var(--default-linkColor) !important;
    }
</style>
""", unsafe_allow_html=True)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Hello! 🐶 I'm your Dog Training Expert. Ask me about obedience training, behavior issues, or puppy care!"
    }]

# Configure sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    with st.container():
        api_key = "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"
        st.markdown("[Get API Key](https://openrouter.ai/keys)")
        
        with st.expander("📘 Quick Start Guide"):
            st.markdown("""
            1. Get API key from OpenRouter
            2. Enter key in the field above
            3. Choose your preferred AI model
            4. Start asking training questions!
            """)
        
        model_name = st.selectbox(
            "🤖 Choose Model",
            ("google/palm-2-chat-bison"),
            index=0
        )
        
        with st.expander("⚡ Advanced Settings"):
            temperature = st.slider("🎨 Response Creativity", 0.0, 1.0, 0.5,
                                   help="Lower = More Factual, Higher = More Creative")
            max_retries = st.number_input("🔄 Max Retries", 1, 5, 2)
        
        st.markdown("### 🚀 Quick Actions")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🧹 Clear Chat", use_container_width=True):
                st.session_state.messages = [{
                    "role": "assistant",
                    "content": "Chat cleared! Ask me about dog training!"
                }]
        with col2:
            if st.button("📋 Example Questions", use_container_width=True):
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": """Try these examples:
                    <span class='badge'>🐾 How to stop leash pulling?</span>
                    <span class='badge'>🏡 Create a potty training schedule</span>
                    <span class='badge'>😟 Help with separation anxiety</span>
                    <span class='badge'>🐕 Teach basic commands</span>""",
                })

# Main interface
st.title("🐕 AI Dog Training Expert")
st.caption("Get professional training advice, behavior solutions, and puppy care tips 24/7")

# Feature cards
with st.container():
    cols = st.columns(4)
    features = [
        ("💡 Expert Tips", "Proven training techniques"),
        ("⚠️ Safety First", "Critical warnings highlighted"),
        ("📅 Progress Tracking", "Follow structured plans"),
        ("🐶 Breed Specific", "Tailored advice when possible")
    ]
    for col, (emoji, text) in zip(cols, features):
        col.markdown(
            f"""<div class="feature-card">
                <h3 style='color: var(--default-primaryColor)'>{emoji}</h3>
                <p style='color: var(--default-textColor)'>{text}</p>
            </div>""", 
            unsafe_allow_html=True
        )

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "badge" in message["content"]:
            st.markdown(message["content"], unsafe_allow_html=True)
        else:
            st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Ask about dog training..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    if not api_key:
        with st.chat_message("assistant"):
            st.error("🔐 API key required! Please check sidebar settings.")
            st.markdown("""
            <div style='background: var(--default-secondaryBackgroundColor); padding: 15px; border-radius: 10px; margin-top: 10px; border: 1px solid var(--default-borderColor);'>
                <h4 style='color: var(--default-primaryColor)'>🚀 Getting Started Guide</h4>
                <ol style='color: var(--default-textColor)'>
                    <li>Visit <a href="https://openrouter.ai/keys" target="_blank">OpenRouter Keys</a></li>
                    <li>Create free account & get API key</li>
                    <li>Paste key in the sidebar</li>
                    <li>Start training! 🎉</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)
        st.stop()

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        attempts = 0
        
        with st.spinner("🧠 Analyzing your query..."):
            time.sleep(0.5)
        
        while attempts < max_retries:
            try:
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://dog-training-assistant.streamlit.app",
                        "X-Title": "AI Dog Trainer"
                    },
                    json={
                        "model": model_name,
                        "messages": [
                            {
                                "role": "system",
                                "content": f"""You are a certified dog trainer with 20+ years experience. STRICT RULES:
1. Respond in clear, structured plain text
2. Format all training plans as:
🌟 Goal: [Training objective]

📘 Method:
Step 1: [Action title]
- Action 1
- Action 2
💡 Pro Tip: [Helpful advice]

⚠️ Safety Notice: [Important warning]

3. Use emojis: 🐾 🐶 💡 ⚠️ 🎯
4. Never use markdown
5. Current date: {time.strftime("%B %d, %Y")}
6. Maintain supportive, professional tone"""
                            },
                            *st.session_state.messages
                        ],
                        "temperature": temperature,
                        "response_format": {"type": "text"}
                    },
                    timeout=15
                )

                response.raise_for_status()
                data = response.json()
                raw_response = data['choices'][0]['message']['content']
                
                processed_response = raw_response
                formatting_cleaners = [
                    ("```", ""), ("**", ""), ("###", ""), 
                    ("\\n", "\n"), ('"', "'"), ("{", ""), ("}", "")
                ]
                
                for pattern, replacement in formatting_cleaners:
                    processed_response = processed_response.replace(pattern, replacement)
                
                lines = processed_response.split('\n')
                for line in lines:
                    words = line.split()
                    for word in words:
                        full_response += word + " "
                        response_placeholder.markdown(full_response + "▌")
                        time.sleep(0.03)
                    full_response += "\n"
                    response_placeholder.markdown(full_response + "▌")
                
                full_response = full_response.replace("Step", "<strong>Step</strong>") \
                                            .replace("Goal:", "<strong>🌟 Goal:</strong>") \
                                            .replace("💡 Pro Tip:", "<span style='color: var(--default-primaryColor)'>💡 Pro Tip:</span>") \
                                            .replace("⚠️ Safety Notice:", "<span style='color: var(--default-errorColor)'>⚠️ Safety Notice:</span>")
                
                response_placeholder.markdown(full_response, unsafe_allow_html=True)
                break
                
            except json.JSONDecodeError as e:
                logging.error(f"JSON Error: {str(e)}")
                attempts += 1
                if attempts == max_retries:
                    response_placeholder.error("⚠️ Failed to process response. Try:")
                    response_placeholder.markdown("""
                    <div style='background: var(--default-secondaryBackgroundColor); padding: 15px; border-radius: 10px; border: 1px solid var(--default-borderColor);'>
                        <h4 style='color: var(--default-primaryColor)'>💡 Try These Fixes:</h4>
                        <ul style='color: var(--default-textColor)'>
                            <li>Rephrase your question</li>
                            <li>Break complex questions into smaller parts</li>
                            <li>Check your internet connection</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    time.sleep(0.5)
                
            except requests.exceptions.RequestException as e:
                response_placeholder.error(f"🌐 Network Error: {str(e)}")
                full_response = "Error: Connection issue - try again later"
                break
                
            except Exception as e:
                logging.error(f"Unexpected Error: {str(e)}")
                response_placeholder.error(f"❌ Unexpected error: {str(e)}")
                full_response = "Error: Please check your input and try again"
                break

    st.session_state.messages.append({"role": "assistant", "content": full_response})
