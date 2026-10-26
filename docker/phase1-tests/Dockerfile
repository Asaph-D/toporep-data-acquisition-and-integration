FROM python:3.12-slim
COPY requirements-phase1.txt /tmp/requirements-phase1.txt
RUN pip install --no-cache-dir -r /tmp/requirements-phase1.txt
WORKDIR /workspace
ENTRYPOINT ["python", "-m", "unittest", "discover", "-s", "tests", "-v"]
