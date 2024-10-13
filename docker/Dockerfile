FROM python:3.13.0rc2-slim AS dev
WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.lock pyproject.toml README.md .python-version LICENSE ./
RUN pip install --no-cache-dir -r requirements.lock

COPY ./ ./
ENV PYTHONPATH /app/src

CMD [ "/bin/bash" ]

FROM python:3.13.0rc2-slim
WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.lock pyproject.toml README.md .python-version LICENSE ./
RUN pip install --no-cache-dir -r requirements.lock

COPY ./ ./
ENV PYTHONPATH /app/src

ENTRYPOINT [ "python", "/app/src/faq_search/main.py" ]
CMD ["--help"]
