# 🤖 AI Support Agent with RAG System

A sophisticated voice-enabled AI support agent built with Azure AI Services, Streamlit, and Retrieval-Augmented Generation (RAG) capabilities. This application provides intelligent conversation, speech recognition, text-to-speech, and knowledge base integration for enhanced customer support and assistance.

## ✨ Features

### 🎤 **Speech Capabilities**
- **Real-time Speech Recognition**: Convert voice input to text using Azure Speech Services
- **Natural Text-to-Speech**: High-quality voice output using Azure Neural Voices
- **Multi-language Support**: Configurable language settings for global deployment
- **Microphone Integration**: Click-to-record functionality with visual feedback

### 🧠 **AI Intelligence**
- **Azure OpenAI Integration**: Powered by GPT-4 for intelligent responses
- **Conversation Memory**: Maintains context throughout the conversation
- **Customizable System Prompts**: Tailor agent behavior for specific use cases
- **Contextual Responses**: Adapts responses based on conversation history

### 📚 **RAG (Retrieval-Augmented Generation) System**
- **Knowledge Base Integration**: Upload and process documents (TXT, PDF, DOCX) or scrape content from URLs
- **Web Content Scraping**: Add web pages to your knowledge base by simply entering URLs
- **Intelligent Document Search**: Find relevant information from uploaded documents and web content
- **Enhanced Responses**: Combine general AI knowledge with specific document and web content
- **Document Management**: Easy upload, processing, and management of knowledge sources

### 💬 **User Interface**
- **Modern Streamlit UI**: Clean, responsive web interface
- **Real-time Chat**: Interactive conversation with message history
- **Voice Controls**: Seamless switching between text and voice input
- **Export Functionality**: Download conversation logs as text files
- **Configuration Panel**: Easy access to settings and customization options

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit UI  │    │  Support Agent   │    │  Simple RAG     │
│                 │◄──►│                  │◄──►│                 │
│ • Chat Interface│    │ • Speech Services│    │ • Document Load │
│ • Voice Controls│    │ • OpenAI Client  │    │ • Text Matching │
│ • Configuration │    │ • Conversation   │    │ • In-Memory     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌──────────────────┐
                    │  Azure Services  │
                    │                  │
                    │ • Speech Service │
                    │ • OpenAI Service │
                    └──────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (recommended: Python 3.9 or higher)
- **Azure Subscription** with access to:
  - Azure Speech Services
  - Azure OpenAI Service
- **Microphone** (for voice input functionality)

### Installation

1. **Clone or download the project**
   ```bash
   git clone https://github.com/RadRebelSam/ai-support-agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Azure credentials**
   
   Create a `.env` file in the project root:
   ```bash
   # Azure Speech Service
   AZURE_SPEECH_KEY=your_speech_service_key_here
   AZURE_SPEECH_REGION=your_speech_region_here
   
   # Azure OpenAI Service
   AZURE_OPENAI_KEY=your_openai_key_here
   AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
   AZURE_OPENAI_DEPLOYMENT=gpt-4
   AZURE_OPENAI_API_VERSION=2024-02-15-preview
   
   # Optional: Customize speech settings
   SPEECH_LANGUAGE=en-US
   TTS_VOICE_NAME=en-US-JennyNeural
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the web interface**
   - Open your browser to `http://localhost:8501`
   - The application will automatically load with all features available

## 🔧 Azure Setup Guide

### 1. Azure Speech Service

1. Navigate to [Azure Portal](https://portal.azure.com)
2. Create a new **Speech Service** resource
3. Choose your region and pricing tier
4. After deployment, go to **Keys and Endpoint**
5. Copy the **Key** and **Region** to your `.env` file

### 2. Azure OpenAI Service

1. Navigate to [Azure Portal](https://portal.azure.com)
2. Create a new **Azure OpenAI** resource
3. Deploy a GPT-4 model (or GPT-3.5-turbo for cost efficiency)
4. Go to **Keys and Endpoint** section
5. Copy the **API Key**, **Endpoint**, and **Deployment Name** to your `.env` file

### 3. Voice Configuration

The application supports various Azure Neural Voices. Popular options include:

| Language | Voice Name | Description |
|----------|------------|-------------|
| English (US) | `en-US-JennyNeural` | Female, friendly |
| English (US) | `en-US-GuyNeural` | Male, professional |
| English (US) | `en-US-AriaNeural` | Female, conversational |
| English (UK) | `en-GB-LibbyNeural` | Female, British accent |
| Spanish | `es-ES-ElviraNeural` | Female, Spanish |
| French | `fr-FR-DeniseNeural` | Female, French |

## 📖 Usage Guide

### Basic Chat

1. **Text Input**: Type your message in the chat input field
2. **Send**: Press Enter or click send
3. **Voice Response**: The agent will respond with both text and audio

### Voice Input

> **Note:** Voice input (microphone) only works when running locally. Streamlit Cloud servers don't have physical microphones. Text-to-speech output works everywhere!

**Local Development Only:**
1. **Select Voice Method**: Choose "Microphone (Click to Record)" in the sidebar
2. **Start Recording**: Click the microphone button
3. **Speak**: Speak your message clearly
4. **Stop Recording**: Click the button again to process

**On Streamlit Cloud:**
- Use text input to chat with the agent
- Voice output (text-to-speech) works perfectly!

### Knowledge Base (RAG)

1. **Upload Documents**: Use the file uploader in the sidebar
2. **Add URLs**: Enter web page URLs to scrape content (one per line)
3. **Supported Formats**: TXT, PDF, DOCX files and web pages (HTML)
4. **Build Knowledge Base**: Click "Build Knowledge Base" after adding files/URLs
5. **Enable RAG**: Toggle the "Enable RAG System" checkbox
6. **Ask Questions**: The agent will now use your documents and web content to provide more accurate responses

### Configuration

- **System Prompt**: Customize the agent's behavior and personality
- **Reset Conversation**: Clear chat history and start fresh
- **Export Chat**: Download conversation logs as text files

## 📁 Project Structure

```
ai-support-agent/
├── app.py                    # Main Streamlit application
├── support_agent.py         # Core AI agent with speech capabilities
├── config.py                # Azure configuration management
├── simple_rag.py            # Simple RAG system (currently used)
├── rag_system.py            # Advanced RAG with ChromaDB (available but unused)
├── test_rag.py              # RAG system testing utilities
├── requirements.txt         # Python dependencies
├── sample_knowledge.txt     # Example knowledge base file
└── README.md               # This documentation
```

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `AZURE_SPEECH_KEY` | Azure Speech Service API key | - | ✅ |
| `AZURE_SPEECH_REGION` | Azure region for Speech Service | - | ✅ |
| `AZURE_OPENAI_KEY` | Azure OpenAI API key | - | ✅ |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint URL | - | ✅ |
| `AZURE_OPENAI_DEPLOYMENT` | Model deployment name | `gpt-4` | ❌ |
| `AZURE_OPENAI_EMBEDDING_DEPLOYMENT` | Embedding model for RAG | `text-embedding-ada-002` | ❌ |
| `AZURE_OPENAI_API_VERSION` | API version | `2024-02-15-preview` | ❌ |
| `SPEECH_LANGUAGE` | Speech recognition language | `en-US` | ❌ |
| `TTS_VOICE_NAME` | Text-to-speech voice | `en-US-JennyNeural` | ❌ |

> **Note**: For deployment to Streamlit Cloud, use the secrets dashboard instead of `.env` file. See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for details.

### RAG System Configuration

- **Current Implementation**: Simple text matching using keyword overlap
- **Chunk Size**: Variable (paragraph-based splitting)
- **Storage**: In-memory document storage
- **Retrieval Method**: Simple text matching (simple_rag.py) - currently active
- **Advanced Option**: Vector embeddings (rag_system.py) - available but not used
- **Max Documents**: 3 relevant documents per query
- **URL Support**: Web scraping with BeautifulSoup for HTML content extraction
- **Content Sources**: Local files (TXT, PDF, DOCX) and web pages (HTML)

## 🛠️ Development

### Running in Development Mode

```bash
streamlit run app.py --server.runOnSave true
```

### Testing Individual Components

```python
# Test the support agent
from support_agent import SupportAgent

agent = SupportAgent()
response = agent.generate_response("Hello!")
print(response)

# Test RAG system
from simple_rag import SimpleRAGSystem

rag = SimpleRAGSystem()
# Load from files and URLs
documents = rag.load_documents(["sample_knowledge.txt", "https://example.com/article"])
processed = rag.process_documents(documents)
rag.create_knowledge_base(processed)
result = rag.query("What is this about?")
print(result)
```

### Code Structure

- **`app.py`**: Streamlit UI and user interaction logic
- **`support_agent.py`**: Core AI agent with speech and conversation management
- **`simple_rag.py`**: Lightweight RAG system using text matching with URL support
- **`rag_system.py`**: Advanced RAG system with vector embeddings
- **`config.py`**: Centralized configuration management

## 🐛 Troubleshooting

### Common Issues

#### Speech Recognition Problems
- **Issue**: No speech detected
- **Solution**: Check microphone permissions and Azure Speech Service configuration
- **Debug**: Verify `AZURE_SPEECH_KEY` and `AZURE_SPEECH_REGION` are correct

#### OpenAI API Errors
- **Issue**: "Invalid API key" or "Deployment not found"
- **Solution**: Verify all Azure OpenAI credentials in `.env` file
- **Debug**: Check deployment name matches `AZURE_OPENAI_DEPLOYMENT`

#### RAG System Issues
- **Issue**: "No relevant information found"
- **Solution**: Ensure documents are properly uploaded and processed
- **Debug**: Check file formats and content quality

#### URL Scraping Issues
- **Issue**: "Network error loading URL" or "Error loading URL"
- **Solution**: Check URL accessibility and internet connection
- **Debug**: Verify URLs are valid and publicly accessible
- **Note**: Some websites may block automated requests or require authentication

#### Audio Playback Problems
- **Issue**: No audio output
- **Solution**: Check browser audio permissions and try different browser
- **Debug**: Verify TTS voice name is valid

### Performance Optimization

- **Large Documents**: Split large files into smaller chunks for better processing
- **Memory Usage**: Clear knowledge base when switching between different document sets
- **Response Time**: Adjust chunk size and retrieval parameters for your use case

## 🚀 Deployment

### Streamlit Cloud (Recommended)

The easiest way to deploy this application is using Streamlit Cloud:

1. **Quick Deploy**: Push your code to GitHub and connect to [share.streamlit.io](https://share.streamlit.io)
2. **Free Hosting**: Deploy and host your app for free
3. **Auto-scaling**: Automatic scaling based on usage
4. **Easy Configuration**: Add secrets via web dashboard

📖 **See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed step-by-step instructions**

### Local Deployment
The application runs locally using Streamlit's built-in server. For production deployment:

### Azure App Service
1. Create an Azure App Service
2. Configure environment variables
3. Deploy the application
4. Set up custom domain (optional)

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

## 🔮 Future Enhancements

### Planned Features
- **Multi-language Support**: Automatic language detection and switching
- **Real-time Streaming**: Continuous speech recognition
- **Custom Wake Words**: Voice activation without clicking
- **Analytics Dashboard**: Conversation metrics and insights
- **User Authentication**: Multi-user support with profiles
- **API Integration**: REST API for external system integration
- **Mobile App**: Native mobile application
- **Advanced RAG**: Switch to ChromaDB-based vector embeddings for semantic search

### Integration Possibilities
- **CRM Systems**: Salesforce, HubSpot integration
- **Help Desk**: Zendesk, Freshdesk integration
- **Database**: Direct database querying capabilities
- **APIs**: External API integration for real-time data

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License

```
MIT License

Copyright (c) 2024 Dexin Yang

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

**Note**: Please ensure compliance with Azure service terms and OpenAI usage policies when using this software.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

### Development Guidelines
1. Follow Python PEP 8 style guidelines
2. Add comprehensive docstrings to new functions
3. Include error handling for all external API calls
4. Test with various document types and sizes
5. Update documentation for new features

## 📞 Support

For technical support:

- **Azure Services**: [Azure Support](https://azure.microsoft.com/support/)
- **Streamlit**: [Streamlit Documentation](https://docs.streamlit.io/)
- **OpenAI**: [OpenAI Documentation](https://platform.openai.com/docs)

## 🙏 Acknowledgments

- **Azure AI Services** for speech and language capabilities
- **Streamlit** for the excellent web framework
- **LangChain** for RAG system components
- **Simple Text Matching** for document retrieval (currently used)

---

**Built with ❤️ using Azure AI Services and Streamlit**
**by Dexin Yang**
**for Conclase Academy x SBSC NextGen Scholarship Capstone**

**Special thanks to Charles Owolabi, my instructor at Conclase Academy, for his excellent guidance and mentorship throughout this project.**
