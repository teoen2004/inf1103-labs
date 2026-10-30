FROM python:3.14-slim
WORKDIR /app

# Copy required files into the container
COPY product.py .
COPY inventory.py .
COPY inventory_manager.py .

#Set the default script to run for the container
CMD ["python", "inventory_manager.py"]