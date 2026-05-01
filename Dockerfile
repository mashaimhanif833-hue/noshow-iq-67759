FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install -e . --no-deps

ENV PYTHONPATH=/app
ENV MONGO_URI=mongodb://localhost:27017/noshow_iq

EXPOSE 7860

CMD ["python", "noshow_iq/api.py"]