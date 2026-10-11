"""FastAPI stub: POST /predict for sentiment model saved by notebook 02."""

from __future__ import annotations

from pathlib import Path

import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = ROOT / "data" / "sentiment_model.joblib"

app = FastAPI(title="AIOT Sentiment API", version="0.1.0")


class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Comment text to classify")


class PredictResponse(BaseModel):
    text: str
    label: str


def _load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. "
            "Run notebook 02_text_classify.ipynb first to save sentiment_model.joblib."
        )
    return joblib.load(MODEL_PATH)


@app.get("/health")
def health():
    return {"ok": True, "model_exists": MODEL_PATH.exists()}


@app.post("/predict", response_model=PredictResponse)
def predict(body: PredictRequest):
    try:
        model = _load_model()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    label = str(model.predict([body.text])[0])
    return PredictResponse(text=body.text, label=label)
