FROM python:3.13.7-slim as builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --user --no-cache-dir -r requirements.txt


FROM python:3.13.7-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local

COPY . .

EXPOSE 8000

ENV PATH=/root/.local/bin:$PATH

ENV PYTHONPATH=/app

CMD ["python", "src/main.py"]