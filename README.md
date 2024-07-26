<div align="center">

# faq-search

<img src="https://github.com/moz-sec/faq-search/blob/main/img/faq_search_top_icon.png" width="200">

[![Lang](https://img.shields.io/badge/python-3.10.14+-yellow.svg?logo=python)](https://www.python.org/)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Linting: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![codecov](https://codecov.io/github/moz-sec/faq-search/graph/badge.svg?token=EQ7ZLCE2IH)](https://codecov.io/github/moz-sec/faq-search)

`faq-search` is FAQ search system.

</div>

## Description

`faq-search` is a system that searches for FAQs.
This repository uses the [FAQ dataset](https://d.line-scdn.net/stf/linecorp/ja/csr/dataset_.zip) provided by LINE Corporation.
[Faiss (Facebook AI Similarity Search)](https://engineering.fb.com/2017/03/29/data-infrastructure/faiss-a-library-for-efficient-similarity-search/) developed by Facebook, identifies questions that are similar to the query and outputs an Answer.

Click here to read the article on LINE Corporation.
[https://linecorp.com/ja/csr/newslist/ja/2020/260](https://linecorp.com/ja/csr/newslist/ja/2020/260)

## Usage

The following is the `faq-search` help output.

```txt
usage: main.py [-h] [-v] query

faq search system

positional arguments:
  query          search faq

options:
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit
```

## Quick Start

```bash
git clone https://github.com/moz-sec/faq-search.git && cd faq-search
pip install -r requirements.lock
python src/faq-search/main.py -h
python src/faq-search/main.py インフルエンザ
```

## Maintainers

- [@moz-sec](https://github.com/moz-sec)

## License

[MIT](https://github.com/moz-sec/faq-search/blob/main/LICENSE)
