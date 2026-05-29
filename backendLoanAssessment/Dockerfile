# ── Stage 1: install dependencies into a venv ────────────────────────────────
FROM public.ecr.aws/docker/library/python:3.12-slim AS builder

WORKDIR /build

COPY backendLoanAssessment/requirements.txt .

RUN python -m venv /build/venv \
    && /build/venv/bin/pip install --no-cache-dir --upgrade pip \
    && /build/venv/bin/pip install --no-cache-dir -r requirements.txt


# ── Stage 2: lean runtime image ───────────────────────────────────────────────
FROM public.ecr.aws/docker/library/python:3.12-slim

# curl is needed for the HEALTHCHECK command
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* \
    && adduser --disabled-password --gecos "" appuser

WORKDIR /app

COPY --from=builder /build/venv /venv

COPY backendLoanAssessment/ backendLoanAssessment/

ENV PATH="/venv/bin:$PATH"

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/openapi.json || exit 1

CMD ["uvicorn", "backendLoanAssessment.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "2"]