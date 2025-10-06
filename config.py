import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AzureConfig:
    """Configuration for Azure AI Services"""

    # Azure Speech Service
    SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
    SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")

    # Azure OpenAI Service
    OPENAI_API_KEY = os.getenv("AZURE_OPENAI_KEY")
    OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4")
    OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")

    # Speech Recognition Settings
    SPEECH_RECOGNITION_LANGUAGE = os.getenv("SPEECH_LANGUAGE", "en-US")

    # Text-to-Speech Settings
    VOICE_NAME = os.getenv("TTS_VOICE_NAME", "en-US-JennyNeural")

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
