FROM python:3.9-slim

WORKDIR /app

# Copy dependency file and install requirements
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# Run the FastAPI application (production command)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
