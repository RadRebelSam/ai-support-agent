# Import required libraries for Azure AI services and RAG system
import azure.cognitiveservices.speech as speechsdk  # Azure Speech Services for voice recognition and synthesis
from openai import AzureOpenAI  # Azure OpenAI client for GPT-4 integration
from config import AzureConfig  # Configuration management for Azure services
import time  # For timing operations and delays
import threading  # For handling concurrent operations
from typing import List, Dict, Any  # Type hints for better code documentation
from simple_rag import SimpleRAGSystem  # Custom RAG system for document-based responses

class SupportAgent:
    """AI Support Agent using Azure Speech and OpenAI services
    
    This class integrates Azure Speech Services for voice input/output and Azure OpenAI
    for conversational AI, with an optional RAG system for document-based knowledge retrieval.
    """

    def __init__(self):
        # Validate that all required Azure configuration is present
        AzureConfig.validate()

        # Initialize Azure Speech Services configuration
        self.speech_config = speechsdk.SpeechConfig(
            subscription=AzureConfig.SPEECH_KEY,  # Azure Speech subscription key
            region=AzureConfig.SPEECH_REGION      # Azure region for speech services
        )
        # Configure speech recognition language (e.g., "en-US")
        self.speech_config.speech_recognition_language = AzureConfig.SPEECH_RECOGNITION_LANGUAGE
        # Configure text-to-speech voice (e.g., "en-US-JennyNeural")
        self.speech_config.speech_synthesis_voice_name = AzureConfig.VOICE_NAME

        # Initialize Azure OpenAI client for GPT-4 integration
        self.openai_client = AzureOpenAI(
            api_key=AzureConfig.OPENAI_API_KEY,        # OpenAI API key
            api_version=AzureConfig.OPENAI_API_VERSION, # API version
            azure_endpoint=AzureConfig.OPENAI_ENDPOINT  # Azure OpenAI endpoint
        )

        # Initialize RAG (Retrieval-Augmented Generation) system for document-based responses
        self.rag_system = SimpleRAGSystem()  # Custom RAG implementation
        self.use_rag = False  # Flag to enable/disable RAG functionality

        # Conversation management - Store chat history for context
        self.conversation_history: List[Dict[str, str]] = []  # List of message dictionaries
        # System prompt that defines the AI's role and behavior
        self.system_prompt = """You are a helpful AI call agent. You assist customers with their inquiries in a professional and friendly manner.
Keep your responses concise and clear, suitable for spoken conversation."""
        
        # Speech recognition state variables for real-time voice processing
        self.recognized_text = ""  # Final recognized text from speech
        self.partial_text = ""     # Real-time partial recognition results
        self.is_recognizing = False  # Flag indicating if recognition is active
        self.recognition_done = threading.Event()  # Threading event for synchronization

    def start_continuous_recognition(self) -> speechsdk.SpeechRecognizer:
        """Start continuous speech recognition with real-time transcription"""
        self.recognized_text = ""
        self.is_recognizing = True
        self.recognition_done.clear()
        
        # Configure for faster, more responsive recognition
        self.speech_config.set_property(
            speechsdk.PropertyId.Speech_SegmentationSilenceTimeoutMs, 
            "500"  # 0.5 seconds of silence before finalizing
        )
        self.speech_config.set_property(
            speechsdk.PropertyId.SpeechServiceConnection_InitialSilenceTimeoutMs,
            "5000"  # 5 seconds max initial silence
        )
        
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config,
            audio_config=audio_config
        )
        
        def recognized_cb(evt):
            """Callback when speech is recognized (final result)"""
            if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                # Only add if it's not already in the recognized text to avoid duplication
                new_text = evt.result.text.strip()
                if new_text and new_text not in self.recognized_text:
                    self.recognized_text += new_text + " "
                    print(f"Final recognized: {new_text}")
        
        def recognizing_cb(evt):
            """Callback for partial recognition results (real-time)"""
            if evt.result.reason == speechsdk.ResultReason.RecognizingSpeech:
                # This gives us real-time partial results
                print(f"Recognizing: {evt.result.text}")
                # Store partial result for real-time display (don't add to final text)
                self.partial_text = evt.result.text
        
        def canceled_cb(evt):
            """Callback when recognition is canceled"""
            print(f"Recognition canceled: {evt}")
            self.is_recognizing = False
            self.recognition_done.set()
        
        def stopped_cb(evt):
            """Callback when recognition is stopped"""
            print(f"Recognition stopped: {evt}")
            self.is_recognizing = False
            self.recognition_done.set()
        
        # Connect callbacks
        recognizer.recognized.connect(recognized_cb)
        recognizer.recognizing.connect(recognizing_cb)  # Real-time partial results
        recognizer.canceled.connect(canceled_cb)
        recognizer.session_stopped.connect(stopped_cb)
        
        # Start continuous recognition
        recognizer.start_continuous_recognition()
        print("Real-time continuous recognition started. Speak now...")
        
        return recognizer
    
    def stop_continuous_recognition(self, recognizer: speechsdk.SpeechRecognizer) -> str:
        """Stop continuous recognition and return recognized text"""
        if recognizer and self.is_recognizing:
            recognizer.stop_continuous_recognition()
            self.recognition_done.wait(timeout=2)  # Wait up to 2 seconds for cleanup
        
        result = self.recognized_text.strip()
        self.recognized_text = ""
        self.partial_text = ""
        return result
    
    def get_current_transcription(self) -> str:
        """Get current transcription (final + partial) for real-time display"""
        final = self.recognized_text.strip()
        partial = self.partial_text.strip()
        
        # Only show partial if it's different from what's already in final
        if final and partial and not partial.lower() in final.lower():
            return f"{final} {partial}"
        elif final:
            return final
        elif partial:
            return partial
        else:
            return ""
    
    def recognize_speech_from_mic(self, timeout_seconds: int = 5) -> str:
        """Recognize speech from microphone input with timeout (legacy method)
        
        Args:
            timeout_seconds: Maximum seconds to wait for speech input (default: 5)
        
        Returns:
            Recognized text or empty string if no speech detected
        """
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config,
            audio_config=audio_config
        )

        print(f"Listening... (will auto-stop after {timeout_seconds} seconds of silence)")
        result = recognizer.recognize_once_async().get()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return result.text
        elif result.reason == speechsdk.ResultReason.NoMatch:
            return ""
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation = result.cancellation_details
            # Don't raise exception for timeout, just return empty string
            if cancellation.reason == speechsdk.CancellationReason.Error:
                raise Exception(f"Speech recognition canceled: {cancellation.error_details}")
            return ""

        return ""

    def recognize_speech_from_audio(self, audio_data: bytes, format: str = "wav") -> str:
        """Recognize speech from audio data"""
        # Create a push stream for the audio data
        stream = speechsdk.audio.PushAudioInputStream()
        stream.write(audio_data)
        stream.close()

        audio_config = speechsdk.audio.AudioConfig(stream=stream)
        recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config,
            audio_config=audio_config
        )

        result = recognizer.recognize_once_async().get()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return result.text
        elif result.reason == speechsdk.ResultReason.NoMatch:
            return ""
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation = result.cancellation_details
            raise Exception(f"Speech recognition canceled: {cancellation.reason}")

        return ""

    def generate_response(self, user_input: str) -> str:
        """Generate AI response using Azure OpenAI with optional RAG"""
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })

        # Check if RAG is enabled and has knowledge base
        if self.use_rag and self.rag_system.documents:
            try:
                # Query RAG system for relevant information
                rag_result = self.rag_system.query(user_input)
                rag_answer = rag_result["answer"]
                source_docs = rag_result["source_documents"]
                
                # Create enhanced system prompt with RAG context
                enhanced_prompt = f"""{self.system_prompt}

Based on the knowledge base, here's relevant information:
{rag_answer}

Use this information to provide a helpful and accurate response. If the information doesn't directly answer the question, use your general knowledge to provide a helpful response."""
                
            except Exception as e:
                # Fallback to regular response if RAG fails
                enhanced_prompt = f"{self.system_prompt}\n\nNote: Knowledge base search failed, using general knowledge."
        else:
            enhanced_prompt = self.system_prompt

        # Prepare messages for API call
        messages = [
            {"role": "system", "content": enhanced_prompt}
        ] + self.conversation_history

        # Call Azure OpenAI
        response = self.openai_client.chat.completions.create(
            model=AzureConfig.OPENAI_DEPLOYMENT,
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )

        assistant_message = response.choices[0].message.content

        # Add assistant response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def text_to_speech(self, text: str) -> bytes:
        """Convert text to speech and return audio data"""
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config,
            audio_config=None  # No audio output config = return audio data
        )

        result = synthesizer.speak_text_async(text).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return result.audio_data
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation = result.cancellation_details
            raise Exception(f"Speech synthesis canceled: {cancellation.reason}")

        return b""

    def speak_text(self, text: str):
        """Speak text through default speaker"""
        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config,
            audio_config=audio_config
        )

        result = synthesizer.speak_text_async(text).get()

        if result.reason == speechsdk.ResultReason.Canceled:
            cancellation = result.cancellation_details
            raise Exception(f"Speech synthesis canceled: {cancellation.reason}")

    def reset_conversation(self):
        """Reset the conversation history"""
        self.conversation_history = []

    def set_system_prompt(self, prompt: str):
        """Update the system prompt"""
        self.system_prompt = prompt

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get the current conversation history"""
        return self.conversation_history.copy()
    
    def enable_rag(self, enabled: bool = True):
        """Enable or disable RAG functionality"""
        self.use_rag = enabled
    
    def setup_rag_knowledge_base(self, file_paths: List[str], force_recreate: bool = False, use_js_rendering: bool = False):
        """Setup RAG knowledge base from files and URLs"""
        try:
            # Load documents
            documents = self.rag_system.load_documents(file_paths, use_js_rendering=use_js_rendering)
            if not documents:
                return False, "No documents loaded"
            
            # Process documents
            processed_docs = self.rag_system.process_documents(documents)
            
            # Create knowledge base
            self.rag_system.create_knowledge_base(processed_docs)
            
            return True, f"Knowledge base created with {len(processed_docs)} document chunks"
            
        except Exception as e:
            return False, f"Error setting up knowledge base: {str(e)}"
    
    def get_rag_stats(self) -> Dict[str, Any]:
        """Get RAG system statistics"""
        return self.rag_system.get_stats()
    
    def clear_rag_knowledge_base(self):
        """Clear the RAG knowledge base"""
        self.rag_system.clear_knowledge_base()
        self.use_rag = False
