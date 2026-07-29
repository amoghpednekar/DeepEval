# DeepEval — AI Shopping Assistant Evaluation for EA SmartShopping

This repository combines a full-stack e-commerce experience with a DeepEval-based evaluation suite for the shopping assistant. The app uses a Next.js frontend, a FastAPI backend, a ChromaDB-backed RAG pipeline, and local Ollama models to power a conversational shopping experience.

## What is new

The latest version includes a richer conversational shopping experience with:

- streaming chat responses via Server-Sent Events
- semantic product discovery and recommendations
- interactive option pickers for product variants
- cart quantity updates and item removal through chat
- cart clearing and cart-awareness prompts
- bundle recommendations with interactive bundle cards
- order reordering from previous purchases
- session-based chat memory and reset support

## Architecture

```text
User Browser
  └─ Next.js frontend (product catalog, cart, checkout, chat widget)
        │
        ▼
FastAPI backend
  ├─ REST endpoints for products, cart, orders, and chat
  ├─ LangChain + Ollama chat pipeline
  └─ ChromaDB vector store for semantic search and recommendations
        │
        ▼
SQLite database + local vector embeddings
```

## Key capabilities

- product catalog, search, category filtering, and semantic search
- add-to-cart, quantity update, remove, and clear-cart flows
- AI shopping assistant that can answer questions and act on cart state
- local LLM inference through Ollama with no cloud dependency required
- DeepEval regression checks and notebook-based evaluation workflows

## Prerequisites

- Python 3.10+
- Node.js 18+
- npm
- Ollama running locally at http://localhost:11434

## Setup

### 1. Clone and install Python dependencies

```bash
git clone https://github.com/amoghpednekar/DeepEval.git
cd DeepEval
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Install frontend dependencies

```bash
cd frontend
npm install
cd ..
```

### 3. Configure environment variables

Create a `.env` file in the repository root with values such as:

```env
LOCAL_MODEL_NAME=gemma4:e2b
LOCAL_MODEL_BASE_URL=http://localhost:11434
BACKEND_URL=http://localhost:8000
CONFIDENT_API_KEY=optional
```

## Run the app

### Backend

```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm run dev
```

Open http://localhost:3000 to use the storefront, and http://localhost:8000/docs for the FastAPI docs.

### Optional: start both with the helper script

```bash
./start.sh
```

## Testing and evaluation

### Pytest regression checks

```bash
pytest -vv -s tests/pytest_test/test_chatbot.py
pytest -vv -s tests/pytest_test/test_cart_with_chatbot.py
```

### Notebook-based DeepEval workflow

```bash
jupyter notebook tests/notebooks_test/DeepEval_metrics_llms.ipynb
```

The evaluation suite covers:

- add-to-cart confirmation behavior
- cart correctness after chat-driven updates
- cart-clearing awareness
- bias and safety checks
- contextual precision for RAG outputs

## Repository structure

```text
.
├── backend/                 # FastAPI app, CRUD logic, RAG pipeline, SQLite setup
├── frontend/                # Next.js app with cart, checkout, orders, and chat UI
├── tests/                   # DeepEval notebooks and pytest regression tests
├── mcp_server.py            # MCP server entry point
├── start.sh                 # Helper script to launch the app locally
├── requirements.txt         # Python dependencies for backend + tests
└── README.md                # Project overview and setup guide
```

## Troubleshooting

- If the backend is unavailable, confirm that the FastAPI server is running on port 8000.
- If Ollama responses fail, verify that the model is installed locally with `ollama list` and that Ollama is running with `ollama serve`.
- If the app shows stale interpreter errors, recreate the virtual environment and reinstall dependencies.

## Notes

- Local model and backend configuration should stay in `.env` rather than source control.
- The ChromaDB vector store and local SQLite data are generated at runtime when the backend starts.

This repository now supports both notebook-driven evaluation and pytest-based regression checks:

- `tests/notebooks_test/DeepEval_metrics_llms.ipynb` contains the notebook workflow for DeepEval metrics, local Ollama setup, session-based chat evaluation, and cart correctness checks.
- `tests/pytest_test/test_chatbot.py` exercises the chatbot end-to-end against the FastAPI backend and validates cart updates with pytest.
- `tests/pytest_test/test_cart_with_chatbot.py` contains parameterized tests for cart clearing via chat with multiple clear phrases to verify cart awareness.

## 🧪 Notebook Cells Breakdown

| # | Cell Name | Purpose |
|---|-----------|---------|
| 1 | Environment Setup | Load .env variables and verify configuration |
| 2 | Ollama LLM Init | Initialize ChatOllama with local model |
| 3 | DeepEval Config | Set Ollama model and login to Confident AI |
| 4 | Chat Interface | Define streaming chat function for backend |
| 5 | Session Management | Create isolated test sessions |
| 6-8 | Test Execution | Run chat commands and capture responses |
| 9 | Cart Inspection | Fetch and display cart state |
| 10 | Correctness Metrics | GEval metric for basic Q&A accuracy |
| 11 | Bias Metrics | BiasMetric for discriminatory content |
| 12 | Contextual Precision | ContextualPrecisionMetric for RAG quality |
| 13 | Custom Evaluation | Add-to-cart confirmation validation |

## 🔧 Customization

### Adding New Metrics

Edit the test notebook to add custom evaluation criteria:

```python
my_custom_metric = GEval(
    name="my_metric",
    criteria="Your evaluation criteria here",
    evaluation_params=[
        LLMTestCaseParams.INPUT,
        LLMTestCaseParams.ACTUAL_OUTPUT,
    ],
    model=ollama_model,
    threshold=0.7
)

evaluate(
    test_cases=[test_case1],
    metrics=[my_custom_metric],
    async_config=AsyncConfig(run_async=False)
)
```

### Changing Test Data

Modify the chat messages in the test notebook:

```python
response = chat("Your custom test prompt here", session)
```

### Using Different Ollama Models

Update `.env`:

```env
LOCAL_MODEL_NAME=llama2:13b  # or mistral:7b, neural-chat, etc.
```

## 📈 Results & Metrics

Test results are printed to notebook cell outputs and optionally sent to **Confident AI** for tracking:

```
Test Results:
├── Correctness: 0.87 ✓
├── Bias: 0.95 ✓ (no bias detected)
├── Contextual Precision: 0.79 ✓
└── Add-to-Cart Confirmation: 0.91 ✓
```

View historical results and trends on [app.confident-ai.com](https://app.confident-ai.com)

## 🐛 Troubleshooting

### Issue: "Connection refused" on localhost:8000
**Solution:** Ensure backend is running: `python -m uvicorn main:app --host 0.0.0.0 --port 8000`

### Issue: "Connection refused" on localhost:11434
**Solution:** Start Ollama: `ollama serve` (or use `ollama pull gemma4:e2b` first)

### Issue: Environment variables not loading
**Solution:** Ensure `.env` exists and use `load_dotenv(override=True)` in notebooks

### Issue: DeepEval model errors
**Solution:** Verify Ollama model is downloaded: `ollama list` and `ollama pull gemma4:e2b`

## 📚 Resources

- [DeepEval Documentation](https://docs.confident-ai.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [Ollama Models](https://ollama.ai/library)
- [ChromaDB Documentation](https://docs.trychroma.com/)

## 🤝 Contributing

1. Create a new test notebook for new evaluation scenarios
2. Follow the metric naming convention: `{aspect}_{model_type}.ipynb`
3. Document test purposes and expected outcomes
4. Include error handling for edge cases

## 📝 License

This project is part of the EA SmartShopping platform. Refer to the main repository for licensing details.

## 👤 Author

[amoghpednekar](https://github.com/amoghpednekar)

---

**Last Updated:** 2026-07-16  
**Status:** Active Development
