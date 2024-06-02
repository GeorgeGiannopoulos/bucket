# Bucket like Repository

Use [Bucker Client](https://github.com/GeorgeGiannopoulos/clients/tree/master/bucket-client) to connect to it

## How it Works

- An `python` image is used

- The `pip` is updaded to latest version

- Change working directory to where the project's code will be reside

- The project's python dependencies are copied to the project's home directory and are installed

- The project's source code is copied inside the image

- An entrypoint using python command and a cmd command that runs the expected main script of the project are executed

## How to Configure

1. Select a `python` image version that matches the one used to develop the project (replace `latest`)

2. Change the environmental variable named `BUCKET_URL` for CORS support

## How to Use

Build image

```shell
docker build -t bucket:latest .
```

Run container

```shell
docker run -idt -p 8000:8000 --restart=unless-stopped --name bucket bucket:latest
```
