FROM python:3.12.0

# Install system dependencies including the development packages for MySQL or MariaDB
RUN apt-get update && \
    apt-get install -y default-libmysqlclient-dev && \
    rm -rf /var/lib/apt/lists/*

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
ARG DB_APP_NAME
ARG DB_CMS_NAME
ARG ENV
ARG ORIGIN
ARG PROJECT_NAME
ARG VERSION

ENV VERSION=${VERSION}
ENV PROJECT_NAME=${PROJECT_NAME}
ENV DB_USERNAME=${DB_USERNAME}
ENV DB_PASSWORD=${DB_PASSWORD}
ENV DB_APP_NAME=${DB_APP_NAME}
ENV DB_CMS_NAME=${DB_CMS_NAME}
ENV DB_HOST=${DB_HOST}
ENV DB_PORT=${DB_PORT}
ENV ENV=${ENV}
ENV ORIGIN=${ORIGIN}

CMD ["uvicorn", "app.main:app", "--port", "8000"]
