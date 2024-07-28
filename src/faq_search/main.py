#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
main.py: faq search system
"""

__author__ = "moz-sec"
__version__ = "0.1.0"
__date__ = "2024/07/25 (Created: 2024/07/19)"

import argparse
import io
import os
import sqlite3
import sys
import urllib.request
import zipfile
from pathlib import Path

import faiss
import numpy as np
import pandas
from sentence_transformers import SentenceTransformer


def create_faq_database(project_dir: Path) -> str:
    """
    create SQLite database and add excel data
    """
    db_path = os.path.join(project_dir, "data/faq.db")
    excel_path = os.path.join(project_dir, "data/dataset_.xlsx")

    if not os.path.exists(excel_path):
        URL = "https://d.line-scdn.net/stf/linecorp/ja/csr/dataset_.zip"
        extract_dir = os.path.join(project_dir, "data")
        with (
            urllib.request.urlopen(url=URL) as res,
            io.BytesIO(res.read()) as bytes_io,
            zipfile.ZipFile(bytes_io) as zip,
        ):
            zip.extractall(extract_dir)

    excel_data = analyze_excel_file(excel_file_path=excel_path)

    conn = sqlite3.connect(database=db_path)
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS faq (id INTEGER PRIMARY KEY, question TEXT, answer TEXT, category1 TEXT, category2 TEXT, source TEXT, type TEXT, service TEXT)"
    )
    cursor.execute("DELETE FROM faq")

    cursor.executemany(
        "INSERT INTO faq VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        excel_data,
    )
    conn.commit()

    return db_path


def analyze_excel_file(excel_file_path: str) -> tuple:
    """
    Read an Excel file to get FAQ data
    """
    excel_data = pandas.read_excel(
        excel_file_path,
        header=0,
        index_col="ID",
        sheet_name="汎用FAQ",
    )
    excel_data = tuple(excel_data.to_numpy().tolist())

    return excel_data


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


def get_faq_results(
    faq_ids: list,
    faq_db: str,
) -> list:
    """
    Get FAQ results.
    """
    conn = sqlite3.connect(database=faq_db)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM faq WHERE id IN ({})".format(",".join("?" * len(faq_ids))),
        faq_ids,
    )
    return cursor.fetchall()


def main():
    parser = argparse.ArgumentParser(description="faq search system")
    parser.add_argument("-v", "--version", action="version", version=__version__)
    parser.add_argument(
        "query",
        help="search faq",
    )
    parser.add_argument(
        "-n",
        "--num",
        type=int,
        default=3,
        help="number of search results",
    )
    args = parser.parse_args()

    faq_db = create_faq_database(Path.cwd())

    # model = SentenceTransformer("sentence-transformers/paraphrase-xlm-r-multilingual-v1")
    model = SentenceTransformer(
        model_name_or_path="sentence-transformers/paraphrase-distilroberta-base-v1"
    )

    faq_ids, faq_embeddings = compute_faq_embeddings(faq_db, model)

    index_flat_l2 = create_faiss_index(model, faq_embeddings, faq_ids)

    faq_indices = search_faq(
        query=args.query, model=model, index=index_flat_l2, k=args.num
    )
    # print(faq_indices)

    results = get_faq_results(
        [faq_ids[i] for i in faq_indices],
        faq_db=faq_db,
    )
    for result in results:
        print("=====")
        print(f"ID: {result[0]}")
        print(f"Question: {result[1]}")
        print(f"Answer: {result[2]}")
        print("=====")


if __name__ == "__main__":
    sys.exit(main())
