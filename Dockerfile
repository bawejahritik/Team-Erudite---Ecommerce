# syntax=docker/dockerfile:1
FROM python:3.12-alpine
WORKDIR /app
RUN apk add curl bash git openssh openssh-server
COPY . /app
RUN pip install -r requirements.txt
ENV PYTHONPATH="/app"
CMD ["uvicorn", "main:app"]
EXPOSE 8000