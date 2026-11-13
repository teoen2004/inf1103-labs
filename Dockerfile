FROM python:3.14-slim
WORKDIR /app

# Copy the application source files into the container
COPY product.py supplier.py inventory.py order.py inventory_manager.py ./

# Copy the Lab 8 tests and the test runner
COPY test_*.py run_tests.py ./

# Set the default script to run for the container
# (run the tests instead with: docker run --rm <image> python run_tests.py)
CMD ["python", "inventory_manager.py"]
