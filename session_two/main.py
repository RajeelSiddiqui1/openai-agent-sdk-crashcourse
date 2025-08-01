import os
import streamlit as st
import asyncio
from concurrent.futures import ThreadPoolExecutor
from agents import Agent, Runner, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel
import time
import re

st.set_page_config(
    page_title="AI Customer Support",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    body {
       
    }
    .stApp {
       
    }
    .main-header {
        text-align: center;
        padding: 1rem 0;
      
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 0 1rem;
    }
    
    .agent-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
       
        border-radius: 15px;
        font-size: 0.8rem;
        margin-bottom: 0.5rem;
    }
    
    .user-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #ffffff;
      
    }
    
    .assistant-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #ffffff;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      ]
    }
    
    .status-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    
    .typing-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        animation: typing 1.4s infinite ease-in-out;
    }
    
    .typing-indicator:nth-child(1) { animation-delay: -0.32s; }
    .typing-indicator:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes typing {
        0%, 80%, 100% { transform: scale(0); }
        40% { transform: scale(1); }
    }
    
    .stChatInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #ffffff;
        padding: 0.75rem 1rem;
        
    }
    
    .stChatInput > div > div > input:focus {
      
        box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.2);
    }

    .stButton>button {
        border-radius: 20px;
       
        border: none;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #000000;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🤖 AI Customer Support Assistant</h1>
    <p>Intelligent multi-agent support system ready to help you</p>
</div>
""", unsafe_allow_html=True)

set_tracing_disabled(disabled=True)

GEMINI_API_KEY = "A5JVxhG5iZLcy9AWaqNFkxxjdN0bbc0XLEPgnBiNwISSu1ik"
if not GEMINI_API_KEY:
    st.error("🔑 GEMINI_API_KEY environment variable is not set. Please configure your API key.")
    st.stop()

MODEL = "gemini/gemini-2.5-flash"

@st.cache_resource
def init_agents():
    web_dev = Agent(
        name="Web Development Specialist",
        model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY),
        instructions="""You are an expert web development specialist. 
        Help users with:
        - Website development and coding issues
        - Frontend and backend technologies
        - Debugging and optimization
        - Best practices and architecture
        Provide clear, actionable solutions with code examples when helpful."""
    )
    
    ai_specialist = Agent(
        name="AI Specialist",
        model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY),
        instructions="""You are an artificial intelligence specialist.
        Assist users with:
        - AI concepts and implementations
        - Machine learning questions
        - AI tool recommendations
        - Technical AI support
        Explain complex concepts in an accessible way."""
    )
    
    tech_support = Agent(
        name="Technical Support Specialist",
        model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY),
        instructions="""You are a technical support specialist.
        Help users with:
        - System troubleshooting
        - Software installation and configuration
        - Performance optimization
        - Error resolution
        Provide step-by-step solutions and follow-up questions."""
    )
    
    account_manager = Agent(
        name="Account Management Specialist",
        model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY),
        instructions="""You are an account management specialist.
        Assist users with:
        - Account setup and configuration
        - Profile and subscription management
        - Billing and payment issues
        - Access and permissions
        Be professional, empathetic, and solution-focused."""
    )
    
    general_agent = Agent(
        name="General Support Coordinator",
        handoffs=[web_dev, ai_specialist, tech_support, account_manager],
        model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY),
        instructions="""You are the main support coordinator. 
        Analyze user queries and either:
        1. Handle general inquiries directly with helpful information
        2. Route to appropriate specialists:
            - Web Development Specialist: coding, websites, development
            - AI Specialist: artificial intelligence, machine learning
            - Technical Support: troubleshooting, system issues
            - Account Management: accounts, billing, subscriptions
        
        Always greet users warmly and ensure they feel heard and supported."""
    )
    
    return general_agent

def run_async_in_thread(agent, prompt):
    async def run_agent():
        return await Runner.run(agent, prompt)
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(run_agent())
    finally:
        loop.close()

def display_typing_indicator():
    return st.markdown("""
    <div class="status-indicator">
        <span>AI is thinking</span>
        <div class="typing-indicator"></div>
        <div class="typing-indicator"></div>
        <div class="typing-indicator"></div>
    </div>
    """, unsafe_allow_html=True)

def delete_all_chats():
    st.session_state.messages = []
    welcome_msg = """👋 **Welcome to AI Customer Support!**

I'm your intelligent assistant powered by multiple specialized agents. I can help you with:

🌐 **Web Development** - Coding, websites, technical implementation
🤖 **Artificial Intelligence** - AI concepts, ML, and AI tools  
🔧 **Technical Support** - Troubleshooting and system issues
👤 **Account Management** - Account setup, billing, subscriptions

How can I assist you today?"""
    st.session_state.messages.append({
        "role": "assistant", 
        "content": welcome_msg,
        "agent": "General Support Coordinator"
    })
    st.rerun()

def stream_response(response_text, response_container):
    in_code_block = False
    full_response = ""
    code_block_content = ""
    for char in response_text:
        full_response += char
        if "```" in full_response and not in_code_block:
            in_code_block = True
            code_block_content = ""
        elif "```" in full_response and in_code_block:
            in_code_block = False
        
        response_container.markdown(f'<div class="assistant-message">{full_response}</div>', unsafe_allow_html=True)
        time.sleep(0.01)

if "messages" not in st.session_state:
    delete_all_chats()

with st.sidebar:
    st.header("Chat Options")
    if st.button("Delete All Chats", key="delete_button"):
        delete_all_chats()

with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(f'<div class="user-message">{message["content"]}</div>', 
                            unsafe_allow_html=True)
        else:
            with st.chat_message("assistant", avatar="🤖"):
                if "agent" in message:
                    st.markdown(f'<div class="agent-badge">{message["agent"]}</div>', 
                                unsafe_allow_html=True)
                st.markdown(f'<div class="assistant-message">{message["content"]}</div>', 
                            unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

if prompt := st.chat_input("Type your message here...", key="chat_input"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user", avatar="👤"):
        st.markdown(f'<div class="user-message">{prompt}</div>', unsafe_allow_html=True)
    
    with st.chat_message("assistant", avatar="🤖"):
        typing_placeholder = st.empty()
        with typing_placeholder:
            display_typing_indicator()
        
        try:
            general_agent = init_agents()
            time.sleep(1)
            
            with ThreadPoolExecutor() as executor:
                result = executor.submit(run_async_in_thread, general_agent, prompt).result()
            
            typing_placeholder.empty()
            
            response = result.final_output
            agent_name = result.agent.name if hasattr(result, 'agent') else "AI Assistant"
            
            st.markdown(f'<div class="agent-badge">{agent_name}</div>', unsafe_allow_html=True)
            
            response_container = st.empty()
            
            stream_response(response, response_container)

            st.session_state.messages.append({
                "role": "assistant", 
                "content": response,
                "agent": agent_name
            })
            
        except Exception as e:
            typing_placeholder.empty()
            error_msg = f"⚠️ I apologize, but I encountered an issue: {str(e)}"
            st.error(error_msg)
            st.session_state.messages.append({
                "role": "assistant", 
                "content": error_msg,
                "agent": "System"
            })

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🔒 Your conversations are secure and not stored permanently</p>
    <p>Powered by Gemini AI • Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)
