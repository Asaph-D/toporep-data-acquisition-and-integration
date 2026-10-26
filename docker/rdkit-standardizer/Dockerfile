FROM python:3.12-slim
ARG RDKIT_VERSION=2026.9.1
RUN pip install --no-cache-dir "rdkit==${RDKIT_VERSION}"
WORKDIR /work
ENTRYPOINT ["python", "/pipeline/standardize_structures_rdkit.py"]
