#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

from faq_search.main import create_faq_database

tmp_path = Path.cwd()


def test_create_faq_database(tmp_path):
    db_path = create_faq_database(project_dir=tmp_path)
    assert db_path == str(tmp_path / "data/faq.db")
    assert (tmp_path / "data/faq.db").exists()
    assert (tmp_path / "data/dataset_.xlsx").exists()
    assert (tmp_path / "data/dataset_.xlsx").exists()
    assert (tmp_path / "data/dataset_.xlsx").exists()
