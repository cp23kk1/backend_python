FROM python:3.12-slim

# Install required system dependencies
RUN apt-get update \
    && apt-get install -y pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

RUN pip install --upgrade pip

# Install virtualenv, Create a virtual environment and activate it
RUN pip install virtualenv
RUN virtualenv venv
RUN . venv/bin/activate

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ARG DB_USERNAME
ARG DB_PASSWORD
ARG DB_HOST
ARG DB_PORT
ARG DB_NAME
ARG ENV
ARG ORIGIN

ENV DB_USERNAME=${DB_USERNAME}
ENV DB_PASSWORD=${DB_PASSWORD}
ENV DB_NAME=${DB_NAME}
ENV DB_HOST=${DB_HOST}
ENV DB_PORT=${DB_PORT}
ENV ENV=${ENV}
ENV ORIGIN=${ORIGIN}

CMD ["uvicorn", "app.main:app", "--port", "8000"]
