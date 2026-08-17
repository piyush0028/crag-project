# Corrective Retrieval Augmented Generation (CRAG) System

## Overview
This project implements a Corrective Retrieval Augmented Generation (CRAG) system designed to accurately answer user queries based on a specialized knowledge base. The system utilizes a multi-step pipeline to retrieve documents, evaluate their relevance, and dynamically rewrite search queries if the initial context is deemed insufficient. This self-correcting mechanism ensures high accuracy and reliability in the generated responses.

## Architecture
The application is structured into a robust backend API and a modern frontend interface.

### Backend
The backend is built with Python and FastAPI, orchestrating the core CRAG pipeline.
- **Vector Database**: Utilizes ChromaDB for the persistent storage and semantic search of documents.
- **Language Models**: Integrates with the Google Gemini API (`gemini-embedding-2` for generating embeddings and `gemini-3.5-flash-lite` for evaluation, rewriting, and generation).
- **Pipeline Workflow**:
  1. **Retrieval**: Fetches the most relevant context documents from the vector database based on the user's query.
  2. **Evaluation**: An LLM-driven evaluator assesses whether the retrieved context contains the necessary information to answer the question.
  3. **Rewrite & Re-retrieve**: If the initial context is evaluated as poor, the system rewrites the query using professional terminology and synonyms, then performs a secondary retrieval.
  4. **Generation**: Synthesizes the final answer using the validated context.

### Frontend
The frontend is a React application built with Vite. It provides a responsive, dark-themed interface for users to interact with the CRAG agent. A key feature of the interface is the transparency it offers; it displays the agent's internal reasoning logs (e.g., retrieving, evaluating, rewriting) in real-time alongside the final generated answer.

## Installation and Local Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- Google Gemini API Key

### Backend Setup
1. Navigate to the root directory of the project.
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory and configure your API key:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```
5. Start the FastAPI development server:
   ```bash
   uvicorn main:app --reload
   ```
   The backend API will be available at `http://127.0.0.1:8000`.

### Frontend Setup
1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install the Node.js dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   The frontend application will be accessible at `http://localhost:5173`.

## Deployment Configuration
The project is structured to be easily deployed to modern cloud hosting platforms.

- **Backend (Render)**: The backend can be deployed as a standard web service. Ensure that the `GEMINI_API_KEY` is properly set in the hosting environment variables.
- **Frontend (Vercel)**: The frontend is optimized for deployment on Vercel. During deployment, configure the `VITE_API_URL` environment variable to point to the live backend URL to ensure proper API communication.

## License
This project is provided under the MIT License.
