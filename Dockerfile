FROM python:3.12-slim

WORKDIR /app

# Install pipenv and project dependencies from Pipfile
COPY Pipfile Pipfile.lock ./
RUN pip install --no-cache-dir pipenv \
    && pipenv install --deploy --ignore-pipfile --system

# Copy the application code
COPY . .

# Default command for running the example lambda launcher script
CMD ["python", "run_lambda_launcher/sum.py"]


