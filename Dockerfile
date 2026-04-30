FROM python:3.11-slim

WORKDIR /app

RUN useradd -m -u 1000 appuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install -e . --no-deps

RUN chown -R appuser:appuser /app

USER appuser

ENV PYTHONPATH=/app

EXPOSE 5000

CMD ["python", "noshow_iq/api.py"]
