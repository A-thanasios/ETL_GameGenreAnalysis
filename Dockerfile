FROM python:3.12-slim
LABEL authors="A-thanasios"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY alembic ./alembic
COPY alembic.ini .

COPY src ./src
COPY main.py .
COPY alembic/init.sh ./alembic/init.sh

RUN chmod +x ./alembic/init.sh

ENTRYPOINT ["/app/alembic/init.sh"]
CMD ["python", "main.py"]