FROM python:3.11-slim

WORKDIR /app

# Install OS dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    python3-dev \
    libssl-dev \
    libffi-dev \
    pkg-config \
    netcat-openbsd \
    && apt-get clean


# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app files
COPY . .

# Ensure the wait script is executable

CMD ["./wait-for-db.sh", "python", "manage.py", "runserver", "0.0.0.0:8000"]

