#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


def compute_faq_embeddings(
    db_path: str, model: SentenceTransformer
) -> tuple[int, np.array]:
    """
    create an embedded text
    """
    conn = sqlite3.connect(database=db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, question FROM faq")
    faq_data = cursor.fetchall()
    faq_ids, faq_questions = zip(*faq_data)

    return faq_ids, np.array(model.encode(faq_questions))


def create_faiss_index(
    model: SentenceTransformer, embeddings, doc_ids: int
) -> faiss.IndexFlatL2:
    """
    Create a Faiss index.
    """
    dimension = model.get_sentence_embedding_dimension()
    index_flat_l2 = faiss.IndexFlatL2(dimension)
    index = faiss.IndexIDMap(index_flat_l2)
    index.add_with_ids(embeddings, doc_ids)

    return index_flat_l2


def search_faq(
    query: str, model: SentenceTransformer, index: faiss.IndexFlatL2, k: int
) -> list:
    """
    Search FAQ.
    """
    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), k)
    return indices[0]
