# Nexus Intelligence Agent

A Retrieval-Augmented Generation (RAG) system for analyzing technical documentation, built with LlamaIndex, Cohere, Pinecone, and Gradio.

## Overview

This project implements a RAG-based chatbot that retrieves relevant information from a vectorized knowledge base stored in Pinecone and generates responses using Cohere's language models. The system is designed to answer questions about technical documentation in Hebrew.

## Features

- **Document Ingestion**: Automatically processes and indexes documents from the `data/` directory into Pinecone.
- **Interactive Chat Interface**: Web-based UI powered by Gradio for user queries.
- **Asynchronous Workflow**: Uses LlamaIndex's Workflow system for efficient retrieval and synthesis.
- **Hebrew Language Support**: Responses are generated in Hebrew based on the provided context.

## Architecture

- **Embedding Model**: Cohere's `embed-english-v3.0` for vectorizing documents.
- **LLM**: Cohere's `command-r-08-2024` for generating responses.
- **Vector Store**: Pinecone for storing and retrieving document embeddings.
- **Frontend**: Gradio for the chat interface.

## Prerequisites

- Python 3.8+
- API keys for:
  - Cohere (COHERE_API_KEY)
  - Pinecone (PINECONE_API_KEY)
- Pinecone index named "rag-project" (or update `INDEX_NAME` in `app.py`)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd rag
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with your API keys:
   ```
   COHERE_API_KEY=your_cohere_api_key
   PINECONE_API_KEY=your_pinecone_api_key
   PINECONE_INDEX_NAME=rag-project
   ```

## Usage

### Ingest Documents

Before running the app, ingest your documents into the vector store:

```bash
python ingest.py
```

This will process all files in the `data/` directory and store their embeddings in Pinecone.

### Run the Chat Application

Start the Gradio interface:

```bash
python app.py
```

Open the provided URL in your browser to interact with the chatbot.

## Project Structure

```
.
├── app.py              # Main application with Gradio interface and NexusAgent workflow
├── ingest.py           # Document ingestion script
├── requirements.txt    # Python dependencies
├── data/               # Directory for documents to ingest
│   ├── architecture.md
│   └── install.md
└── README.md           # This file
```

## Configuration

- Update `INDEX_NAME` in `app.py` if using a different Pinecone index.
- Modify chunk size and overlap in `ingest.py` for different document processing.
- Adjust the system prompt in `app.py` for different response styles.

## Contributing

Feel free to submit issues and pull requests.

## License

[Add your license here]
