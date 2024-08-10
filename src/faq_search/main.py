#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "moz-sec"
__version__ = "0.1.2"
__date__ = "2024/08/10 (Created: 2024/07/19)"

import argparse
import sys
from pathlib import Path

import uvicorn
from sentence_transformers import SentenceTransformer

from faq_search.db import create_faq_database, get_faq_results
from faq_search.faiss_index import (
    compute_faq_embeddings,
    create_faiss_index,
    search_faq,
)


def main():
    parser = argparse.ArgumentParser(description="faq search system")
    parser.add_argument("-v", "--version", action="version", version=__version__)
    parser.add_argument(
        "query",
        nargs="?",
        help="Search FAQ",
    )
    parser.add_argument(
        "-n",
        "--num",
        type=int,
        default=3,
        help="number of search results",
    )
    parser.add_argument(
        "--server",
        action="store_true",
        default=False,
        help="server mode",
    )
    args = parser.parse_args()

    if args.server:
        uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=False)
        return 0

    if args.query:
        parser.error("the following arguments are required: query")

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
