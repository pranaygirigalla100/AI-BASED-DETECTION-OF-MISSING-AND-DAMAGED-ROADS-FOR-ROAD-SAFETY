##  V1
# FROM python:3.12-slim

# WORKDIR /app

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# EXPOSE 8501

# CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]




##  V2
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .

# Add these lines to fix the missing graphics libraries
RUN apt-get update && apt-get install -y \
    libgl1 libglib2.0-0 libxcb1

RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]