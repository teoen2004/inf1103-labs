FROM python:3.14-slim
WORKDIR /app

# Copy the application source files and sample data into the container
COPY product.py supplier.py inventory.py discount.py order.py product_factory.py inventory_manager.py products.csv ./

# Copy the Lab 8 tests, Lab 9 automated tests folder, and test runner
COPY test_*.py run_tests.py ./
COPY tests ./tests

# Set the default script to run for the container
# (run the tests instead with: docker run --rm <image> python run_tests.py)
CMD ["python", "inventory_manager.py"]
