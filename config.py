# Configuration management for Azure AI services
import os  # Environment variable access
import platform  # Platform detection for OS-specific configurations
from dotenv import load_dotenv  # Load environment variables from .env file

# Load environment variables from .env file (for local development)
load_dotenv()

# Try to import streamlit for secrets support (for cloud deployment)
try:
    import streamlit as st  # Streamlit framework for web app
    HAS_STREAMLIT = True  # Flag indicating Streamlit is available
except ImportError:
    HAS_STREAMLIT = False  # Streamlit not available (command-line usage)

def get_config_value(key: str, default=None):
    """Get configuration value from Streamlit secrets or environment variables
    
    This function provides a unified way to access configuration values,
    trying Streamlit secrets first (for cloud deployment) and falling back
    to environment variables (for local development).
    """
    if HAS_STREAMLIT:
        try:
            # Try to get from Streamlit secrets first (for cloud deployment)
            return st.secrets.get(key, os.getenv(key, default))
        except (AttributeError, FileNotFoundError):
            # Fallback to environment variables if secrets are not available
            return os.getenv(key, default)
    return os.getenv(key, default)  # Direct environment variable access

def is_cloud_deployment():
    """Detect if running on Streamlit Cloud or other cloud platforms
    
    This function checks for environment indicators that suggest
    the application is running in a cloud environment rather than locally.
    """
    # Check for Streamlit Cloud environment indicators
    if os.getenv("STREAMLIT_SHARING_MODE"):
        return True
    # Check if running on Linux without audio system (typical for cloud)
    if platform.system() == "Linux":
        # Check if ALSA/audio libraries are available
        try:
            import subprocess
            result = subprocess.run(['which', 'aplay'], capture_output=True)
            return result.returncode != 0  # No audio system found
        except:
            return True  # Assume cloud if we can't check
    return False

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
