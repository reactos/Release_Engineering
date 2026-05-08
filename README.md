# Release Engineering

This repository contains the scripts used to create ReactOS release images.

## Building a release using Docker
You can build ReactOS releases locally in three easy steps, assuming you have Docker Desktop installed.

#### 1. Building the container
Clone this git repository and `cd` into it. From the root of the repository, run the commands below. This will create a Docker image called `reactos-base` and a Docker container called `reactos-builder`.

```bash
docker build -t reactos-base .
docker run --name reactos-builder -it reactos-base
```
Your container will now be set up and your terminal will be connected to it. To disconnect from the container, run `exit`.

If you disconnect from your container, you can reconnect to it using this command:
```bash
docker start -ai reactos-builder
```

#### 2. Building release deliverables
Once you connect to your container, you will be in the `/reactos` directory. This contains a git clone of the ReactOS repository. To build release deliverables, simply checkout the branch with the release you want to make and run `release`.
```bash
git checkout {release branch}
release
```
The release script will handle fetching the latest commits from origin, downloading optional modules, building ReactOS, and creating the deliverables. When there is no internet connection, the release script is smart enough to continue if optional modules were downloaded previously and warn about not fetching from origin.

#### 3. Copying the deliverables
When complete, the release script will display a message similar to this:

```
*******************************************************************************
Successfully created the following packages:
    /reactos/deliverables/ReactOS-0.4.16-dev-2669-i386.zip
    /reactos/deliverables/ReactOS-0.4.16-dev-2669-src.zip
*******************************************************************************
```

Simply copy the release deliverables from the `/reactos/deliverables` folder to your computer to use them as needed. You can copy them from the container using Docker Desktop's graphical interface, or you can use the Docker command line interface. For example, this will copy the contents of `/reactos/deliverables` to the current working directory if your container name is `reactos-builder`:
```bash
docker cp reactos-builder:/reactos/deliverables/. .
```
