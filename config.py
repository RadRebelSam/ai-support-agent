import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try to import streamlit for secrets support
try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False

def get_config_value(key: str, default=None):
    """Get configuration value from Streamlit secrets or environment variables"""
    if HAS_STREAMLIT:
        try:
            # Try to get from Streamlit secrets first (for deployment)
            return st.secrets.get(key, os.getenv(key, default))
        except (AttributeError, FileNotFoundError):
            # Fallback to environment variables
            return os.getenv(key, default)
    return os.getenv(key, default)

class AzureConfig:
    """Configuration for Azure AI Services"""

    # Azure Speech Service
    SPEECH_KEY = get_config_value("AZURE_SPEECH_KEY")
    SPEECH_REGION = get_config_value("AZURE_SPEECH_REGION")

    # Azure OpenAI Service
    OPENAI_API_KEY = get_config_value("AZURE_OPENAI_KEY")
    OPENAI_ENDPOINT = get_config_value("AZURE_OPENAI_ENDPOINT")
    OPENAI_DEPLOYMENT = get_config_value("AZURE_OPENAI_DEPLOYMENT", "gpt-4")
    OPENAI_API_VERSION = get_config_value("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
    OPENAI_EMBEDDING_DEPLOYMENT = get_config_value("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-ada-002")

    # Speech Recognition Settings
    SPEECH_RECOGNITION_LANGUAGE = get_config_value("SPEECH_LANGUAGE", "en-US")

    # Text-to-Speech Settings
    VOICE_NAME = get_config_value("TTS_VOICE_NAME", "en-US-JennyNeural")

    @classmethod
    def validate(cls):
        """Validate that all required configuration is present"""
        required_vars = [
            ("AZURE_SPEECH_KEY", cls.SPEECH_KEY),
            ("AZURE_SPEECH_REGION", cls.SPEECH_REGION),
            ("AZURE_OPENAI_KEY", cls.OPENAI_API_KEY),
            ("AZURE_OPENAI_ENDPOINT", cls.OPENAI_ENDPOINT),
        ]

        missing_vars = [var_name for var_name, var_value in required_vars if not var_value]

        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

        return True
