import streamlit as st
from support_agent import SupportAgent
import io
import time
from audio_recorder_streamlit import audio_recorder

# Page configuration
st.set_page_config(
    page_title="Support Agent",
    layout="wide"
)

# Initialize session state
if 'agent' not in st.session_state:
    try:
        st.session_state.agent = SupportAgent()
        st.session_state.initialized = True
    except Exception as e:
        st.session_state.initialized = False
        st.session_state.error = str(e)

if 'messages' not in st.session_state:
    st.session_state.messages = []

# Main UI
st.title("Support Agent")
st.markdown("---")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")

    # RAG System Configuration
    st.subheader("🧠 Knowledge Base (RAG)")
    
    # RAG toggle
    rag_enabled = st.checkbox(
        "Enable RAG System", 
        value=st.session_state.agent.use_rag if st.session_state.initialized else False,
        help="Enable retrieval-augmented generation for better responses"
    )
    
    if st.session_state.initialized:
        st.session_state.agent.enable_rag(rag_enabled)
    
    # File upload for knowledge base
    uploaded_files = st.file_uploader(
        "Upload documents for knowledge base",
        type=['txt', 'pdf', 'docx'],
        accept_multiple_files=True,
        help="Upload text files, PDFs, or Word documents to build your knowledge base"
    )
    
    if uploaded_files and st.button("📚 Build Knowledge Base"):
        if st.session_state.initialized:
            # Save uploaded files temporarily
            file_paths = []
            for uploaded_file in uploaded_files:
                # Create a temporary file
                with open(f"temp_{uploaded_file.name}", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                file_paths.append(f"temp_{uploaded_file.name}")
            
            # Setup knowledge base
            with st.spinner("Building knowledge base..."):
                success, message = st.session_state.agent.setup_rag_knowledge_base(file_paths)
                if success:
                    st.success(message)
                    st.session_state.agent.enable_rag(True)
                else:
                    st.error(message)
            
            # Clean up temporary files
            import os
            for file_path in file_paths:
                if os.path.exists(file_path):
                    os.remove(file_path)
    
    # Knowledge base management
    if st.session_state.initialized:
        rag_stats = st.session_state.agent.get_rag_stats()
        st.info(f"📊 Knowledge Base: {rag_stats['total_documents']} documents")
        
        if st.button("🗑️ Clear Knowledge Base"):
            st.session_state.agent.clear_rag_knowledge_base()
            st.success("Knowledge base cleared!")
            st.rerun()

    st.markdown("---")

    # System prompt customization
    st.subheader("System Prompt")
    system_prompt = st.text_area(
        "Customize agent behavior:",
        value=st.session_state.agent.system_prompt if st.session_state.initialized else "",
        height=150,
        key="system_prompt_input"
    )

    if st.button("Update System Prompt"):
        if st.session_state.initialized:
            st.session_state.agent.set_system_prompt(system_prompt)
            st.success("System prompt updated!")

    st.markdown("---")

    # Reset conversation
    if st.button("🔄 Reset Conversation"):
        if st.session_state.initialized:
            st.session_state.agent.reset_conversation()
            st.session_state.messages = []
            st.success("Conversation reset!")
            st.rerun()

    st.markdown("---")

    # Statistics
    st.subheader("Statistics")
    st.metric("Messages", len(st.session_state.messages))

# Check if agent is initialized
if not st.session_state.initialized:
    st.error("❌ Failed to initialize AI Support Agent")
    st.error(f"Error: {st.session_state.error}")
    st.info("Please check your .env file and ensure all Azure credentials are configured correctly.")
    st.stop()

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Conversation")

    # Display conversation history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if msg.get("timestamp"):
                st.caption(msg["timestamp"])

    # Chat input
    user_input = st.chat_input("Type your message here...")

    if user_input:
        # Add user message
        timestamp = time.strftime("%H:%M:%S")
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "timestamp": timestamp
        })

        # Display user message
        with st.chat_message("user"):
            st.write(user_input)
            st.caption(timestamp)

        # Generate and display AI response
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.agent.generate_response(user_input)

                # Add assistant message
                response_timestamp = time.strftime("%H:%M:%S")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "timestamp": response_timestamp
                })

                # Display assistant message
                with st.chat_message("assistant"):
                    st.write(response)
                    st.caption(response_timestamp)

                # Text-to-speech
                with st.spinner("Generating speech..."):
                    audio_data = st.session_state.agent.text_to_speech(response)
                    st.audio(audio_data, format="audio/wav")

            except Exception as e:
                st.error(f"Error: {str(e)}")

with col2:
    st.subheader("Voice Input")

    # Voice input method selection
    voice_method = st.radio(
        "Select input method:",
        ["Text Only", "Microphone (Click to Record)"],
        key="voice_method"
    )

    if voice_method == "Microphone (Click to Record)":
        st.info("Click the button below to start recording. Click again to stop.")

        if st.button("🎤 Start/Stop Recording"):
            with st.spinner("Recording... Speak now!"):
                try:
                    # Record from microphone
                    recognized_text = st.session_state.agent.recognize_speech_from_mic()

                    if recognized_text:
                        st.success(f"Recognized: {recognized_text}")

                        # Process the recognized text
                        timestamp = time.strftime("%H:%M:%S")
                        st.session_state.messages.append({
                            "role": "user",
                            "content": recognized_text,
                            "timestamp": timestamp
                        })

                        # Generate response
                        response = st.session_state.agent.generate_response(recognized_text)

                        response_timestamp = time.strftime("%H:%M:%S")
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response,
                            "timestamp": response_timestamp
                        })

                        # Generate speech
                        audio_data = st.session_state.agent.text_to_speech(response)

                        st.rerun()
                    else:
                        st.warning("No speech detected. Please try again.")

                except Exception as e:
                    st.error(f"Error: {str(e)}")

    st.markdown("---")

    # Export conversation
    st.subheader("Export")
    if st.button("📥 Export Conversation"):
        if st.session_state.messages:
            # Create text export
            export_text = "AI Support Agent Conversation\n"
            export_text += "=" * 50 + "\n\n"

            for msg in st.session_state.messages:
                role = msg['role'].upper()
                content = msg['content']
                timestamp = msg.get('timestamp', 'N/A')
                export_text += f"[{timestamp}] {role}:\n{content}\n\n"

            # Offer download
            st.download_button(
                label="Download as TXT",
                data=export_text,
                file_name=f"conversation_{time.strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
        else:
            st.info("No conversation to export yet.")

# Footer
st.markdown("---")
st.caption("Powered by Azure AI Services and Streamlit")
