#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sqlite3
import urllib.request
import zipfile
from pathlib import Path

import pandas


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

    conn.close()

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


def get_all_faqs(
    faq_db: str,
) -> list:
    """
    Get all FAQ data.
    """
    conn = sqlite3.connect(database=faq_db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM faq")

    return cursor.fetchall()


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
