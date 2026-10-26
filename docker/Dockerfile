# syntax=docker/dockerfile:1

# Use a lightweight official Python image.
FROM python:3.14-slim

# Prevent Python from writing .pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Display Python output immediately in container logs.
ENV PYTHONUNBUFFERED=1

# Set the application working directory.
WORKDIR /app

# Create a non-root user and group.
RUN groupadd --system appgroup \
    && useradd --system --gid appgroup \
       --home-dir /app --no-create-home appuser

# Copy dependency definitions first for build caching.
COPY requirements.txt .

# Install dependencies and remove packaging tools
# that are not required by the running application.
RUN python -m pip install --no-cache-dir \
        -r requirements.txt \
    && python -m pip uninstall -y pip setuptools wheel

# Copy application source code.
COPY --chown=appuser:appgroup app/ ./app/

# Switch to the non-root user.
USER appuser

# Document the application port.
EXPOSE 8000

# Start the FastAPI application.
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
