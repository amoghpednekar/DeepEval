import os
from pathlib import Path
from dotenv import load_dotenv
from deepeval.metrics import GEval
from deepeval.evaluate import AsyncConfig
from deepeval.models import OllamaModel
from typing import Optional, Tuple, Union
from pydantic import BaseModel
import requests
import json
import uuid
import pytest
import deepeval

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")


# Load .env from root directory (try parent directory first, then current)
# Use override=True to force reload and overwrite cached values
env_path = Path("../.env") if Path("../.env").exists() else Path(".env")
print(f"Loading from: {env_path.resolve()}")
load_dotenv(env_path, override=True)

## print("MODEL_NAME:", os.getenv("LOCAL_MODEL_NAME"))
## print("BASE_URL:", os.getenv("LOCAL_MODEL_BASE_URL"))

# Load .env from root directory (try parent directory first, then current)
env_path = Path("../.env") if Path("../.env").exists() else Path(".env")
load_dotenv(env_path, override=True)


class OllamaModelNoThink(OllamaModel):
     def generate(self, prompt: str, schema: Optional[BaseModel] = None) -> Tuple[Union[str, BaseModel], float]:
        chat_model = self.load_model()
        messages = [{"role": "user", "content": prompt}]

        response = chat_model.chat(
            model=self.name,
            messages=messages,
            format=schema.model_json_schema() if schema else None,
            options={
                **{"temperature": self.temperature},
                **self.generation_kwargs,
            },
            think=False
        )
        return (
            (
                schema.model_validate_json(response.message.content)
                if schema
                else response.message.content
            ),
            0,
        )

     async def a_generate(self, prompt: str, schema: Optional[BaseModel] = None) -> Tuple[Union[str, BaseModel], float]:
        chat_model = self.load_model(async_mode=True)
        messages = [{"role": "user", "content": prompt}]

        response = await chat_model.chat(
            model=self.name,
            messages=messages,
            format=schema.model_json_schema() if schema else None,
            options={
                **{"temperature": self.temperature},
                **self.generation_kwargs,
            },
            think=False
        )
        return (
            (
                schema.model_validate_json(response.message.content)
                if schema
                else response.message.content
            ),
            0,
        )


## --- Application specific methods---

def chat(message: str, session_id: str) -> str:
    """
    Call the streaming chat endpoint and collect the full assistant response.
    Returns the concatenated text content.
    """
    resp = requests.post(
        f"{BACKEND_URL}/api/chat/stream",
        json={"message": message, "session_id": session_id},
        stream=True,
        timeout=120,
    )
    resp.raise_for_status()

    full_text = ""
    for line in resp.iter_lines():
        if not line:
            continue
        decoded = line.decode("utf-8") if isinstance(line, bytes) else line
        if not decoded.startswith("data: "):
            continue
        payload = decoded[6:].strip()
        if not payload:
            continue
        try:
            data = json.loads(payload)
            if data.get("type") == "chunk":
                full_text += data.get("content", "")
        except json.JSONDecodeError:
            pass
    return full_text.strip()


def get_cart(session_id: str) -> dict:
    resp = requests.get(f"{BACKEND_URL}/api/cart/{session_id}", timeout=10)
    return resp.json()

## ---- fixtures Methods that will be used acrossed the test----

def pytest_configure():
    api_key = os.getenv("CONFIDENT_API_KEY")
    if api_key:
        deepeval.login(api_key=api_key)

@pytest.fixture #reusable methods
def session_id() -> str:
    """
    Generate a new session ID.
    """
    return f"test_{uuid.uuid4().hex[:12]}"

@pytest.fixture(scope="session") #reusable methods
def judge():
    return OllamaModelNoThink(
    model=os.getenv("LOCAL_MODEL_NAME"), 
    base_url=os.getenv("LOCAL_MODEL_BASE_URL")
)