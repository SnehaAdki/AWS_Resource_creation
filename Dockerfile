FROM python:3.12-slim

RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app
COPY Pipfile Pipfile.lock ./
RUN pip install --no-cache-dir pipenv \
    && pipenv install --deploy --ignore-pipfile --system

COPY . .
USER appuser

CMD ["python", "run_lambda_launcher/sum.py"]