#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from pathlib import Path

from sentence_transformers import SentenceTransformer

from faq_search.db import create_faq_database, get_faq_results
from faq_search.faiss_index import (
    compute_faq_embeddings,
    create_faiss_index,
    search_faq,
)


def cli_run(args: argparse.Namespace) -> None:
    """
    run in CLI mode
    """
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

    return
