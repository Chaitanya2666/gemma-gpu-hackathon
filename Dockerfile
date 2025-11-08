FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Fix: Streamlit ko port 8080 use karne ko bolo
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
