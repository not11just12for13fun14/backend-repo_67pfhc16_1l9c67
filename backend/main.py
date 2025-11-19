from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import create_document, get_documents
from schemas import Lead, TestMessage

app = FastAPI(title="NovaScreen Africa API", version="1.0.0")

# Allow all origins for dev preview; in production, restrict this
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "ok", "service": "NovaScreen Africa API"}

@app.get("/test")
async def test():
    # Try a simple DB roundtrip to confirm connectivity
    try:
        docs = await get_documents("ping", {}, limit=1)
        return {"ok": True, "db": True, "count": len(docs)}
    except Exception as e:
        return {"ok": True, "db": False, "error": str(e)}

@app.post("/quote")
async def submit_quote(lead: Lead):
    try:
        saved = await create_document("lead", lead.model_dump())
        return {"success": True, "lead": saved}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save lead: {e}")

class FAQItem(BaseModel):
    question: str
    answer: str

@app.get("/faq")
async def faq():
    # Static FAQs for now
    items = [
        FAQItem(question="Do you offer custom sizes?", answer="Yes, panels can be configured to virtually any dimension."),
        FAQItem(question="Indoor vs Outdoor?", answer="Outdoor LEDs have higher brightness, weather resistance, and different pixel pitch options."),
        FAQItem(question="Do you install and support?", answer="We provide full installation, calibration, and ongoing support.")
    ]
    return {"items": [i.model_dump() for i in items]}
