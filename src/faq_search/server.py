#!/usr/bin/env python
# -*- coding: utf-8 -*-

from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from sentence_transformers import SentenceTransformer

from faq_search.db import create_faq_database, get_all_faqs, get_faq_results
from faq_search.faiss_index import (
    compute_faq_embeddings,
    create_faiss_index,
    search_faq,
)


def server_run() -> None:
    """
    Run the API server
    """
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model, index_flat_l2, faq_db, faq_ids

    faq_db = create_faq_database(Path.cwd())
    model = SentenceTransformer(
        model_name_or_path="sentence-transformers/paraphrase-distilroberta-base-v1"
    )

    faq_ids, faq_embeddings = compute_faq_embeddings(faq_db, model)

    index_flat_l2 = create_faiss_index(model, faq_embeddings, faq_ids)

    yield
    del model, index_flat_l2, faq_db, faq_ids


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root() -> dict:
    return {"Message": "FAQ Search API"}


@app.get("/faqs")
async def faqs_list() -> dict:
    results = get_all_faqs(faq_db=faq_db)
    return {
        "results": [
            {
                "id": result[0],
                "question": result[1],
                "answer": result[2],
                "category1": result[3],
                "category2": result[4],
                "source": result[5],
                "type": result[6],
                "service": result[7],
            }
            for result in results
        ]
    }


@app.get("/faqs/search")
async def faqs_search(
    query: str,
    num: int = 3,
) -> dict:
    faq_indices = search_faq(query=query, model=model, index=index_flat_l2, k=num)

    results = get_faq_results(
        [faq_ids[i] for i in faq_indices],
        faq_db=faq_db,
    )

    return {
        "results": [
            {"id": result[0], "question": result[1], "answer": result[2]}
            for result in results
        ]
    }
