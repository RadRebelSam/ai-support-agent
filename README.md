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

1. Navigate to Azure
2. Create a new **Speech Service** resource
3. Choose your region and pricing tier
4. After deployment, go to **Keys and Endpoint**
5. Copy the **Key** and **Region** to your `.env` file

### 2. Azure OpenAI Service

1. Navigate to Azure
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

## 📁 Project Structure

```
ai-support-agent/
├── app.py                   # Main Streamlit application
├── support_agent.py         # Core AI agent with speech capabilities
├── config.py                # Azure configuration management
├── simple_rag.py            # Simple RAG system (currently used)
├── rag_system.py            # Advanced RAG with ChromaDB (available but unused)
├── test_rag.py              # RAG system testing utilities
├── requirements.txt         # Python dependencies
├── sample_knowledge.txt     # Example knowledge base file
└── README.md                # This documentation
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

### Code Structure

- **`app.py`**: Streamlit UI and user interaction logic
- **`support_agent.py`**: Core AI agent with speech and conversation management
- **`simple_rag.py`**: Lightweight RAG system using text matching with URL support
- **`rag_system.py`**: Advanced RAG system with vector embeddings
- **`config.py`**: Centralized configuration management

## 🔮 Future Enhancements

### Planned Features
Comprehensive Backend Dashboard
#### Analytics & Monitoring:
- Real-time Metrics: Live conversation tracking, response times, and system health
- User Analytics: Session duration, conversation patterns, and user engagement metrics
- Performance Monitoring: API usage, error rates, and resource utilization
- Knowledge Base Analytics: Document usage statistics, retrieval effectiveness, and content gaps
#### Content Management:
- Advanced RAG: Switch to ChromaDB-based vector embeddings for semantic search
- Document Library: Centralized repository for all knowledge base documents
- Version Control: Track document updates and maintain revision history
- Content Validation: Automated quality checks and content optimization suggestions
- Bulk Operations: Mass upload, processing, and organization of documents
#### User Management:
- Role-based Access Control: Admin, moderator, and user permission levels
- User Activity Logs: Detailed audit trails of user interactions and system usage
- Session Management: Active session monitoring and remote session termination
- Custom User Profiles: Personalized settings and preferences management
#### System Configuration:
- Model Settings: Fine-tune AI parameters, temperature, and response length
- Voice Configuration: Manage speech recognition languages and TTS voices
- Multi-language Support: Automatic language detection and switching
- Integration Settings: Configure external API connections and webhooks
- Security Settings: Authentication methods, rate limiting, and access controls
#### Reporting & Insights:
- Custom Reports: Generate detailed analytics reports with filtering and export options
- Trend Analysis: Identify patterns in user queries and system performance
- ROI Tracking: Measure support efficiency improvements and cost savings
- Predictive Analytics: Forecast usage patterns and system requirements

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

## 🙏 Acknowledgments

- **Azure Services for speech and language capabilities**: [Azure Documentation](https://learn.microsoft.com/en-us/azure/)
- **Streamlit for the excellent web framework**: [Streamlit Documentation](https://docs.streamlit.io/)
- **LangChain for RAG system components and document processing**: [LangChain Documentation](https://python.langchain.com/docs/)
- **BeautifulSoup for HTML parsing and web content extraction**: [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- **Selenium for JavaScript rendering and dynamic content scraping**: [Selenium Documentation](https://selenium-python.readthedocs.io/)


---

**Built with ❤️ using Azure AI Services and Streamlit**
**by Dexin Yang**
**for Conclase Academy x SBSC NextGen Scholarship Capstone**

**Special thanks to Charles Owolabi, my instructor at Conclase Academy**
