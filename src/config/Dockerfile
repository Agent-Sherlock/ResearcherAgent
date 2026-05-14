# Use the official agent-server as base
FROM python:3.11-slim

# Install Qiskit dependencies
RUN apt-get update && apt-get install -y libgomp1 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir numpy==2.4.2
