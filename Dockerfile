FROM python:3.9-slim

WORKDIR /app

# Copy dependency file and install requirements
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port that Vercel will use (typically 3000)
EXPOSE 3000

# Run the FastAPI application using the PORT environment variable (defaulting to 8000 if not set)
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
