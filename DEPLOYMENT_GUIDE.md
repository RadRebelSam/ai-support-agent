# Streamlit Cloud Deployment Guide

This guide will help you deploy your AI Support Agent to Streamlit Cloud.

## Prerequisites

1. **Azure Account** with the following resources:
   - Azure Speech Service
   - Azure OpenAI Service (with GPT-4 deployment)
   - Azure OpenAI Embeddings deployment (text-embedding-ada-002)

## Local Development Setup

### 1. Create `.env` file

Create a `.env` file in the project root with your Azure credentials:

```env
# Azure Speech Service
AZURE_SPEECH_KEY=your_speech_service_key_here
AZURE_SPEECH_REGION=your_region_here  # e.g., eastus, westus2

# Azure OpenAI Service
AZURE_OPENAI_KEY=your_openai_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Azure OpenAI Embeddings (for RAG system)
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-ada-002

# Optional Settings
SPEECH_LANGUAGE=en-US
TTS_VOICE_NAME=en-US-JennyNeural
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Locally

```bash
streamlit run app.py
```

## Streamlit Cloud Deployment

### 1. Push to GitHub

Make sure your code is pushed to a GitHub repository. **Important:** Do NOT commit your `.env` file!

```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### 2. Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository, branch, and `app.py` as the main file
5. Click "Advanced settings" before deploying

### 3. Configure Secrets in Streamlit Cloud

In the "Advanced settings" or after deployment in "App settings" → "Secrets", add your configuration:

```toml
# Azure Speech Service
AZURE_SPEECH_KEY = "your_speech_service_key_here"
AZURE_SPEECH_REGION = "your_region_here"

# Azure OpenAI Service
AZURE_OPENAI_KEY = "your_openai_api_key_here"
AZURE_OPENAI_ENDPOINT = "https://your-resource-name.openai.azure.com/"
AZURE_OPENAI_DEPLOYMENT = "gpt-4"
AZURE_OPENAI_API_VERSION = "2024-02-15-preview"

# Azure OpenAI Embeddings
AZURE_OPENAI_EMBEDDING_DEPLOYMENT = "text-embedding-ada-002"

# Optional Settings
SPEECH_LANGUAGE = "en-US"
TTS_VOICE_NAME = "en-US-JennyNeural"
```

### 4. Deploy

Click "Deploy" and wait for the app to start!

## How to Get Your Azure Credentials

### Azure Speech Service

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to your Speech Service resource
3. Click "Keys and Endpoint" in the left menu
4. Copy:
   - **Key 1** or **Key 2** → `AZURE_SPEECH_KEY`
   - **Location/Region** → `AZURE_SPEECH_REGION`

### Azure OpenAI Service

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to your Azure OpenAI resource
3. Click "Keys and Endpoint" in the left menu
4. Copy:
   - **Key 1** or **Key 2** → `AZURE_OPENAI_KEY`
   - **Endpoint** → `AZURE_OPENAI_ENDPOINT`
5. Go to "Model deployments" → "Manage Deployments"
6. Note your deployment names:
   - GPT-4 deployment name → `AZURE_OPENAI_DEPLOYMENT`
   - Embedding deployment name → `AZURE_OPENAI_EMBEDDING_DEPLOYMENT`

## Troubleshooting

### "Missing required environment variables"

- Make sure all required secrets are added in Streamlit Cloud
- Check that the variable names match exactly (case-sensitive)
- Restart the app after adding secrets

### "Error initializing RAG system"

- Ensure you have created an embedding deployment in Azure OpenAI
- The embedding deployment must be named `text-embedding-ada-002` or update the config

### "Microphone recording not available" or "SPXERR_AUDIO_SYS_LIBRARY_NOT_FOUND"

- **This is expected on Streamlit Cloud!** Cloud servers don't have physical microphones
- **Solution**: The app automatically detects cloud deployment and disables microphone input
- **Alternatives**: 
  - Use text input (fully functional on cloud)
  - Run the app locally for microphone support
  - Text-to-speech output still works on cloud (responses have audio)

### "Speech recognition failed"

- Verify your Azure Speech Service key and region are correct
- Check that your Speech Service resource is active in Azure Portal
- Note: Voice **input** only works locally, but voice **output** (TTS) works everywhere

### Deployment Failed on Streamlit Cloud

Common issues:
1. **Wrong Python version**: Check `runtime.txt` specifies `python-3.11`
2. **Missing dependencies**: Ensure all packages are in `requirements.txt`
3. **Package conflicts**: Try specifying exact versions if there are conflicts

## Configuration File Priority

The app supports both local development and cloud deployment:

1. **Local Development**: Uses `.env` file (via `python-dotenv`)
2. **Streamlit Cloud**: Uses Streamlit secrets (`.streamlit/secrets.toml` or cloud dashboard)
3. **Priority**: Streamlit secrets > Environment variables > Default values

## Security Best Practices

1. ✅ Never commit `.env` files to Git
2. ✅ Add `.env` to `.gitignore`
3. ✅ Use separate Azure resources for dev and production
4. ✅ Rotate your API keys regularly
5. ✅ Use Azure Key Vault for production deployments

## Support

If you encounter issues:
- Check the Streamlit Cloud logs in the app dashboard
- Verify all Azure services are active and properly configured
- Ensure your Azure subscription has sufficient credits/quota

