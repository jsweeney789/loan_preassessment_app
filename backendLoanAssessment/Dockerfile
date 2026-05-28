# ── Stage 1: install dependencies into a venv ────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /build

COPY backendLoanAssessment/requirements.txt .

RUN python -m venv /build/venv \
    && /build/venv/bin/pip install --no-cache-dir --upgrade pip \
    && /build/venv/bin/pip install --no-cache-dir -r requirements.txt


# ── Stage 2: lean runtime image ───────────────────────────────────────────────
FROM python:3.12-slim

# curl is needed for the HEALTHCHECK command
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* \
    && adduser --disabled-password --gecos "" appuser

WORKDIR /app

# Copy the venv from the builder — no build tools in the final image
COPY --from=builder /build/venv /venv

# Copy only the application package
# Build context must be the repo root: docker build -f backendLoanAssessment/Dockerfile .
COPY backendLoanAssessment/ backendLoanAssessment/

ENV PATH="/venv/bin:$PATH"

USER appuser

EXPOSE 8000

# FastAPI exposes /openapi.json automatically — used as the liveness probe
# NOTE: ask the backend team to add a dedicated GET /health → 200 route
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/openapi.json || exit 1

CMD ["uvicorn", "backendLoanAssessment.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "2"]
