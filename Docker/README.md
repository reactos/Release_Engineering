# RosBE-Unix on Ubuntu with Release Engineering scripts

Normally this docker container can be used from ghcr.io

Below steps outline the process of running it locally.

## Building the container

 - Create an image named `reactos-base`:
    - `docker build --pull --rm -f "Dockerfile" -t reactos-base "."`
 - Create a container named `reactos-builder` from the `reactos-base` image
    - `docker run --name reactos-builder -it reactos-base`
    - `exit` to close the container

## Running the container

 - Run the `reactos-builder`:
    - `docker start reactos-builder`
 - Show all docker containers:
    - `docker ps`
 - Attach to the running `reactos-builder`:
    - `docker attach 03e11af06800` (where `03e11af06800` is the `CONTAINER ID` from the running container)

## Building a release

```bash
Release_Configure
# Answer the prompts
Release_ISOs
Release_Source
```
