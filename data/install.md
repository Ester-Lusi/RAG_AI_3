# Nexus Installation Guide

## Prerequisites

Before installing Nexus, ensure your system meets the following requirements:

- **Python Version**: Python 3.8 or higher
- **Operating System**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 18.04+)
- **RAM**: Minimum 4GB, recommended 8GB+
- **Storage**: At least 1GB free space for dependencies and data
- **Internet Connection**: Required for downloading dependencies and accessing external APIs

## Environment Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/nexus.git
cd nexus
```

### 2. Create Virtual Environment

Create and activate a Python virtual environment to isolate dependencies:

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Install all required Python packages using pip:

```bash
pip install llama-index llama-index-embeddings-cohere llama-index-vector-stores-pinecone pinecone-client python-dotenv
```

This will install:
- **llama-index**: Core framework for RAG (Retrieval-Augmented Generation) operations
- **llama-index-embeddings-cohere**: Cohere embeddings for text vectorization
- **llama-index-vector-stores-pinecone**: Pinecone vector database integration
- **pinecone-client**: Official Pinecone Python client
- **python-dotenv**: Environment variable management from .env files

### 4. Environment Configuration

Create a `.env` file in the project root with your API keys and configuration:

```env
# Cohere API Configuration
COHERE_API_KEY=your_cohere_api_key_here

# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=your_pinecone_environment
PINECONE_INDEX_NAME=nexus-index

# Application Settings
LOG_LEVEL=INFO
MAX_TOKENS=1000
TEMPERATURE=0.7
```

**Security Note**: Never commit your `.env` file to version control. Add it to `.gitignore`.

### 5. API Key Setup

#### Cohere API Key
1. Visit [Cohere Dashboard](https://dashboard.cohere.ai/)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Generate a new API key
5. Copy the key to your `.env` file

#### Pinecone API Key
1. Visit [Pinecone Console](https://app.pinecone.io/)
2. Create a new account or log in
3. Go to API Keys in the sidebar
4. Create a new API key
5. Note your environment (e.g., `us-west1-gcp`)
6. Add the key and environment to your `.env` file

### 6. Initialize Pinecone Index

Before running the application, you need to create and configure your Pinecone index:

```python
import pinecone
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize Pinecone
pinecone.init(
    api_key=os.getenv('PINECONE_API_KEY'),
    environment=os.getenv('PINECONE_ENVIRONMENT')
)

# Create index if it doesn't exist
index_name = os.getenv('PINECONE_INDEX_NAME')
if index_name not in pinecone.list_indexes():
    pinecone.create_index(
        name=index_name,
        dimension=768,  # Cohere embed-english-v2.0 dimension
        metric='cosine'
    )
```

### 7. Verify Installation

Run the following command to verify all dependencies are installed correctly:

```bash
python -c "import llama_index, pinecone, cohere; print('All dependencies installed successfully')"
```

You should see: `All dependencies installed successfully`

### 8. Run the Application

Start the Nexus application:

```bash
python app.py
```

The application should start and display initialization messages. Check the console output for any errors.

## Troubleshooting

### Common Issues

**ImportError: No module named 'llama_index'**
- Ensure you're running from the activated virtual environment
- Reinstall dependencies: `pip install -r requirements.txt` (if you have a requirements file)

**Pinecone Authentication Error**
- Verify your API key and environment in `.env`
- Check your Pinecone account limits and billing status

**Cohere API Error**
- Confirm your Cohere API key is valid
- Check your Cohere account quota

**Virtual Environment Issues**
- On Windows, ensure you're using PowerShell and the correct activation script
- Try recreating the virtual environment if issues persist

### Performance Optimization

For better performance:
- Use SSD storage for data persistence
- Increase RAM if processing large datasets
- Consider using GPU acceleration for embeddings (if available)

### Support

If you encounter issues not covered here:
1. Check the [GitHub Issues](https://github.com/your-org/nexus/issues) page
2. Review the application logs for detailed error messages
3. Contact the development team with your error logs and system information