#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from pathlib import Path

from faq_search.db import create_faq_database

tmp_path = Path.cwd()


class DbTest(unittest.TestCase):
    def test_create_faq_database(self):
        db_path = create_faq_database(project_dir=tmp_path)
        self.assertEqual(db_path, str(tmp_path / "data/faq.db"))
        self.assertTrue((tmp_path / "data/faq.db").exists())
        self.assertTrue((tmp_path / "data/dataset_.xlsx").exists())


if __name__ == "__main__":
    unittest.main()
