FROM python:3.14-slim
WORKDIR /app

# Copy required files into the container
COPY auditor.py .
COPY modular_auditor.py .

#Set the default script to run for the container
CMD ["python", "modular_auditor.py"]