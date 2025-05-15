FROM python:3.10-slim


# Set working directory
WORKDIR /app
ENV HOME=/app

# Copy files
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.enableCORS=false"]
