FROM python:3.13-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1


RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libssl-dev libffi-dev \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY . .


RUN mkdir -p /app/data

ENV DATABASE_URL=sqlite:///./data/dados.db
ENV PYTHONPATH=/app

VOLUME ["/app/data"]

# comando padrão
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]