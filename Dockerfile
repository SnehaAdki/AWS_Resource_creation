FROM python:3.12-slim

RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app
COPY Pipfile Pipfile.lock ./
RUN pip install --no-cache-dir pipenv \
    && pipenv install --deploy --ignore-pipfile --system

COPY . .
USER appuser

HEALTHCHECK --interval=1m --timeout=10s --start-period=30s --retries=3 \
  CMD pgrep -f run_lambda_launcher/sum.py > /dev/null || exit 1

CMD ["python", "run_lambda_launcher/sum.py"]