FROM python:3.13-slim

ARG PROJECT_PATH

WORKDIR /app

COPY shared/ /shared/
COPY ${PROJECT_PATH}/ /app/

RUN pip install --no-cache-dir -e /shared \
    && pip install --no-cache-dir -e .

CMD ["python", "main.py"]
