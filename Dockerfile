FROM python:3.11-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Create app directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create a non-root user and group
# The actual values will be overridden at runtime by docker-compose
ARG USER_NAME=botuser
ARG USER_ID=1000
ARG GROUP_ID=1000

RUN addgroup -g $GROUP_ID $USER_NAME && \
    adduser -D -u $USER_ID -G $USER_NAME $USER_NAME && \
    chown -R $USER_NAME:$USER_NAME /app

# Switch to non-root user
USER $USER_NAME

# Command to run the application
CMD ["python", "main.py"] 