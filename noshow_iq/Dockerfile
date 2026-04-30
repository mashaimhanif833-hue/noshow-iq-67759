# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Final
FROM python:3.11-slim

WORKDIR /app

# Non-root user banao
RUN useradd -m -u 1000 appuser

# Copy installed packages
COPY --from=builder /root/.local /home/appuser/.local

# Copy project files
COPY . .

# Package install karo
RUN python -m pip install -e . --no-deps

# Ownership fix karo
RUN chown -R appuser:appuser /app

USER appuser

ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONPATH=/app

EXPOSE 5000

CMD ["python", "noshow_iq/api.py"]