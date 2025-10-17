# Import required libraries for the Streamlit web application
import streamlit as st
from support_agent import SupportAgent
import io
import time
from audio_recorder_streamlit import audio_recorder

# Configure the Streamlit page settings
st.set_page_config(
    page_title="Support Agent",  # Browser tab title
    layout="wide"  # Use full width layout for better UI
)

# Initialize session state variables to maintain state across app reruns
if 'agent' not in st.session_state:
    try:
        # Create the main SupportAgent instance with Azure AI services
        st.session_state.agent = SupportAgent()
        st.session_state.initialized = True
    except Exception as e:
        # Handle initialization errors (e.g., missing API keys)
        st.session_state.initialized = False
        st.session_state.error = str(e)

# Initialize conversation history to store chat messages
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Initialize voice recording state variables
if 'is_recording' not in st.session_state:
    st.session_state.is_recording = False  # Track if currently recording audio

if 'recognizer' not in st.session_state:
    st.session_state.recognizer = None  # Store speech recognizer instance

# Initialize additional session state variables for voice recording
if 'recording_start_time' not in st.session_state:
    st.session_state.recording_start_time = None  # Track when recording started

if 'user_has_interacted' not in st.session_state:
    st.session_state.user_has_interacted = False  # Track if user has interacted with the app

# Main UI Layout - Create the primary interface
st.title("Support Agent")  # Main page title
st.markdown("---")  # Horizontal divider for visual separation

# Sidebar Configuration Panel - Contains all settings and controls
with st.sidebar:
    st.header("Configuration")  # Sidebar header

    # RAG (Retrieval-Augmented Generation) System Configuration Section
    st.subheader("🧠 Knowledge Base (RAG)")
    
    # RAG System Toggle - Enable/disable document-based responses
    rag_enabled = st.checkbox(
        "Enable RAG System", 
        value=st.session_state.agent.use_rag if st.session_state.initialized else False,
        help="Enable retrieval-augmented generation for better responses"
    )
    
    # Apply RAG setting to the agent if initialized
    if st.session_state.initialized:
        st.session_state.agent.enable_rag(rag_enabled)
    
    # Document Upload Section - Allow users to add knowledge sources
    st.markdown("**📚 Add Documents to Knowledge Base**")
    
    # Create two equal-width columns for file upload and URL input
    col1, col2 = st.columns([1, 1])
    
    # Left Column: File Upload Interface
    with col1:
        uploaded_files = st.file_uploader(
            "📄 Upload Files",
            type=['txt', 'pdf', 'docx'],  # Supported file formats
            accept_multiple_files=True,  # Allow multiple file selection
            help="Upload text files, PDFs, or Word documents"
        )
    
    # Right Column: URL Input Interface
    with col2:
        url_input = st.text_area(
            "🌐 Add URLs",
            placeholder="https://example.com/article\nhttps://docs.example.com/guide",
            height=100,  # Fixed height for text area
            help="Enter URLs (one per line) to scrape content from web pages"
        )
        
        # JavaScript Rendering Option - For dynamic websites
        use_js_rendering = st.checkbox(
            "🚀 Use JavaScript Rendering",
            value=False,  # Default to disabled (faster)
            help="Enable for JavaScript-heavy sites (slower but more complete content). Note: May not work in cloud environments - will fallback to standard method."
        )
        
        urls = []
        if url_input:
            urls = [url.strip() for url in url_input.split('\n') if url.strip() and url.strip().startswith(('http://', 'https://'))]
    
    # Show build button if there are files or URLs
    has_files = uploaded_files is not None and len(uploaded_files) > 0
    has_urls = len(urls) > 0
    
    if (has_files or has_urls) and st.button("📚 Build Knowledge Base"):
        if st.session_state.initialized:
            # Combine files and URLs
            all_inputs = []
            
            # Handle uploaded files
            if has_files:
                file_paths = []
                for uploaded_file in uploaded_files:
                    # Create a temporary file
                    with open(f"temp_{uploaded_file.name}", "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    file_paths.append(f"temp_{uploaded_file.name}")
                all_inputs.extend(file_paths)
            
            # Handle URLs
            if has_urls:
                all_inputs.extend(urls)
                st.info(f"🌐 Processing {len(urls)} URL(s)...")
            
            # Setup knowledge base
            with st.spinner("Building knowledge base..."):
                success, message = st.session_state.agent.setup_rag_knowledge_base(all_inputs, use_js_rendering=use_js_rendering)
                if success:
                    st.success(message)
                    st.session_state.agent.enable_rag(True)
                else:
                    st.error(message)
            
            # Clean up temporary files
            import os
            if has_files:
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
            # Display audio player for assistant messages with audio
            if msg["role"] == "assistant" and msg.get("audio_data"):
                # Create a unique key for each audio player
                audio_key = f"audio_{hash(msg['content'])}"
                
                # For the most recent message, add auto-play functionality
                if msg == st.session_state.messages[-1]:
                    # Create a data URL for the audio
                    import base64
                    audio_b64 = base64.b64encode(msg["audio_data"]).decode()
                    audio_data_url = f"data:audio/wav;base64,{audio_b64}"
                    
                    st.markdown("🔊 **Auto-playing response...** (Click to replay if needed)")
                    
                    # Add auto-play HTML5 audio element
                    st.markdown(f"""
                    <audio controls autoplay style="width: 100%; margin: 5px 0;">
                        <source src="{audio_data_url}" type="audio/wav">
                        Your browser does not support the audio element.
                    </audio>
                    """, unsafe_allow_html=True)
                else:
                    st.audio(msg["audio_data"], format="audio/wav")

    # Chat input
    user_input = st.chat_input("Type your message here...")

    if user_input:
        # Mark that user has interacted (helps with auto-play)
        st.session_state.user_has_interacted = True
        
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

                # Text-to-speech
                with st.spinner("Generating speech..."):
                    audio_data = st.session_state.agent.text_to_speech(response)

                # Add assistant message with audio data
                response_timestamp = time.strftime("%H:%M:%S")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "timestamp": response_timestamp,
                    "audio_data": audio_data
                })

                # Display assistant message
                with st.chat_message("assistant"):
                    st.write(response)
                    st.caption(response_timestamp)
                    # Audio will be displayed by the conversation history loop with auto-play

                # Rerun to trigger conversation history loop and show audio
                st.rerun()

            except Exception as e:
                st.error(f"Error: {str(e)}")

with col2:
    st.subheader("Voice Input")
    
    # Check if running on cloud
    from config import is_cloud_deployment
    is_cloud = is_cloud_deployment()

    # Voice input method selection
    if is_cloud:
        st.warning("⚠️ **Microphone recording is not available on Streamlit Cloud**")
        st.info("""
        **Why?** Cloud servers don't have physical microphones or audio hardware.
        
        **Alternatives:**
        - Use text input (type your messages)
        - Run the app locally for microphone support
        - Upload audio files (coming soon)
        """)
        voice_method = "Text Only"
    else:
        voice_method = st.radio(
            "Select input method:",
            ["Text Only", "Microphone (Click to Record)"],
            key="voice_method"
        )

    if voice_method == "Microphone (Click to Record)" and not is_cloud:
        st.info("🎤 Click **Start Recording** to begin. Click **Stop Recording** when done, or wait for auto-stop after 10 seconds.")
        
        # Create two columns for Start and Stop buttons
        btn_col1, btn_col2 = st.columns(2)
        
        with btn_col1:
            start_button = st.button("🎤 Start Recording", type="primary", disabled=st.session_state.is_recording)
        
        with btn_col2:
            stop_button = st.button("⏹️ Stop Recording", type="secondary", disabled=not st.session_state.is_recording)
        
        # Show recording status with timer and real-time transcription
        if st.session_state.is_recording and st.session_state.recording_start_time:
            elapsed = int(time.time() - st.session_state.recording_start_time)
            st.warning(f"🔴 Recording in progress... ({elapsed}s) - Speak now or click Stop!")
            
            # Show real-time transcription
            current_text = st.session_state.agent.get_current_transcription()
            if current_text:
                st.info(f"🎤 **Live transcription:** {current_text}")
            else:
                st.info("🎤 **Listening...** (speech will appear here as you talk)")
        
        # Handle Start Recording
        if start_button and not st.session_state.is_recording:
            try:
                # Mark that user has interacted (helps with auto-play)
                st.session_state.user_has_interacted = True
                
                # Start continuous recognition
                st.session_state.recognizer = st.session_state.agent.start_continuous_recognition()
                st.session_state.is_recording = True
                st.session_state.recording_start_time = time.time()
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error starting recording: {str(e)}")
        
        # Handle Stop Recording button
        if stop_button and st.session_state.is_recording:
            try:
                # Stop continuous recognition
                recognized_text = st.session_state.agent.stop_continuous_recognition(st.session_state.recognizer)
                
                # Reset recording state
                st.session_state.is_recording = False
                st.session_state.recognizer = None
                st.session_state.recording_start_time = None

                if recognized_text:
                    st.success(f"✅ Recognized: {recognized_text}")

                    # Process the recognized text
                    timestamp = time.strftime("%H:%M:%S")
                    st.session_state.messages.append({
                        "role": "user",
                        "content": recognized_text,
                        "timestamp": timestamp
                    })

                    # Generate response
                    with st.spinner("🤔 Generating response..."):
                        response = st.session_state.agent.generate_response(recognized_text)

                    # Generate speech
                    with st.spinner("🔊 Generating speech..."):
                        audio_data = st.session_state.agent.text_to_speech(response)

                    response_timestamp = time.strftime("%H:%M:%S")
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response,
                        "timestamp": response_timestamp,
                        "audio_data": audio_data  # Store audio data with the message
                    })

                    st.rerun()
                else:
                    st.warning("⚠️ No speech detected. Please try again.")
                    st.rerun()

            except Exception as e:
                st.session_state.is_recording = False
                st.session_state.recognizer = None
                st.session_state.recording_start_time = None
                st.error(f"❌ Error stopping recording: {str(e)}")
                st.rerun()
        
        # Auto-stop after 10 seconds
        if st.session_state.is_recording and st.session_state.recording_start_time:
            elapsed = time.time() - st.session_state.recording_start_time
            if elapsed > 10:
                try:
                    # Auto-stop
                    recognized_text = st.session_state.agent.stop_continuous_recognition(st.session_state.recognizer)
                    
                    # Reset recording state
                    st.session_state.is_recording = False
                    st.session_state.recognizer = None
                    st.session_state.recording_start_time = None

                    if recognized_text:
                        st.success(f"✅ Auto-stopped. Recognized: {recognized_text}")

                        # Process the recognized text
                        timestamp = time.strftime("%H:%M:%S")
                        st.session_state.messages.append({
                            "role": "user",
                            "content": recognized_text,
                            "timestamp": timestamp
                        })

                        # Generate response
                        with st.spinner("🤔 Generating response..."):
                            response = st.session_state.agent.generate_response(recognized_text)

                        # Generate speech
                        with st.spinner("🔊 Generating speech..."):
                            audio_data = st.session_state.agent.text_to_speech(response)

                        response_timestamp = time.strftime("%H:%M:%S")
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response,
                            "timestamp": response_timestamp,
                            "audio_data": audio_data  # Store audio data with the message
                        })

                        st.rerun()
                    else:
                        st.warning("⚠️ Auto-stopped after 10s. No speech detected.")
                        st.rerun()
                except Exception as e:
                    st.session_state.is_recording = False
                    st.session_state.recognizer = None
                    st.session_state.recording_start_time = None
                    st.error(f"❌ Error: {str(e)}")
                    st.rerun()
            else:
                # Keep updating to show timer and real-time transcription
                time.sleep(0.3)  # Faster updates for real-time feel
                st.rerun()

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
