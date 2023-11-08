# Flask Nadalig

This is a dockerized flask app with MySQL

## Prerequisites

To run this youll need [Docker](https://www.docker.com/products/docker-desktop/) and [Docker-compose](https://docs.docker.com/compose/install/) installed

## Clone the Repository

```shell
git clone git@github.com:NadCarlos/flask_app_nadalig.git
```

## .env file

You will find a ".env.example" file in the repository, you use that one as an example, just copy and paste the content to a new ".env" file and replace the variables with your credentials.

## Build Images and Run containers

```shell
docker-compose build && docker-compose up
```

If everything is working and you got no errors you can stop the container with `ctrl + c` and run again `docker-compose up -d` to detach it from the console,
then, to stop the container using `-d` use `docker-compose stop`

## Examples 

In the file "thunder_collection_flask_app.json" you have the examples for you to sart using the app