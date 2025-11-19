from __future__ import annotations

import os
from typing import Any, Dict, Optional, List
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "novascreen")

_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None

async def get_db() -> AsyncIOMotorDatabase:
    global _client, _db
    if _db is None:
        _client = AsyncIOMotorClient(DATABASE_URL)
        _db = _client[DATABASE_NAME]
    return _db

async def create_document(collection_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    db = await get_db()
    data = {**data, "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()}
    result = await db[collection_name].insert_one(data)
    inserted = await db[collection_name].find_one({"_id": result.inserted_id})
    # Convert ObjectId to string for JSON serialization
    if inserted and "_id" in inserted:
        inserted["id"] = str(inserted.pop("_id"))
    return inserted or {}

async def get_documents(
    collection_name: str,
    filter_dict: Optional[Dict[str, Any]] = None,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    db = await get_db()
    cursor = db[collection_name].find(filter_dict or {}).limit(limit)
    docs: List[Dict[str, Any]] = []
    async for d in cursor:
        d["id"] = str(d.pop("_id"))
        docs.append(d)
    return docs
