# Use a lightweight Python base image
FROM python:3.11-slim

# Install uv
RUN pip install --no-cache-dir uv

# Set working directory
WORKDIR /app

# Copy dependency definitions first (for build caching)
COPY pyproject.toml uv.lock* ./

# Install dependencies using uv
RUN uv sync --frozen --no-dev

# Copy the rest of the app
COPY .GarminDb /root/.GarminDb
COPY . .

#Declare host and port as environment variables
ENV DB_HOST=host.docker.internal
ENV DB_USER=postgres

# Default command to run your script
CMD ["uv", "run", "main.py"]
