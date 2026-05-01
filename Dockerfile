FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install -e . --no-deps

# Train model during build
RUN python -c "from noshow_iq.model import train; train('data/KaggleV2-May-2016 (1).csv')"

ENV PYTHONPATH=/app

EXPOSE 7860

CMD ["python", "noshow_iq/api.py"]
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install -e . --no-deps

ENV PYTHONPATH=/app

EXPOSE 7860

CMD ["python", "noshow_iq/api.py"]