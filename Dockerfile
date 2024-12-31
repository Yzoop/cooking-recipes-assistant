# Use the official Python 3.12 image as a base
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy the project files to the container
COPY poetry.lock pyproject.toml app/
COPY . /app

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Command to run the app
CMD ["uvicorn", "cooking_assistant.app.main:app", "--host", "0.0.0.0", "--port", "$PORT"]