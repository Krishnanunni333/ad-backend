# pull official base image
FROM tiangolo/uvicorn-gunicorn:python3.10-slim

# set working directory
WORKDIR /app


# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# add app
COPY . .
