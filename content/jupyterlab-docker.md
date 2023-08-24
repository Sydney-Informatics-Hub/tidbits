Title: Set up your Jupyter environment in Docker
Date: 2021-05-03
Author: Sergio Pintaldi
Category: Python
Tags: Python, Jupyter

# The Problem

`Python` lets you have multiple virtual environments and that's cool for running scripts but when you need to install `Jupyter` and run a notebook in `Jupyter Lab` (the old `Jupyter Notebook` or `IPython notebook` will be [deprecated soon](https://github.com/jupyter/docker-stacks#jupyter-notebook-deprecation-notice)), different environment might install different version of Jupyter and Lab with different plugins, ending up in a big mess. In fact there will be conflicting Jupyter configuration located under `$HOME/.ipython`.

# Proposed solution

Using docker to install your containerised Jupyter enviroment seems appealing. It can be integrated in your project folder in this way:

```sh
.
├── ...
├── requirements
│   ├── build.sh
│   ├── Dockerfile
│   ├── pip-requirements.txt
│   ├── run.sh
│   └── start.sh
├── ...
```

In which the `Dockerfile` looks like this:

```Dockerfile
# inherit from Python image
FROM python:3.8

# set your user in the container
ARG NB_USER="myuser"
ARG NB_UID="1000"
ARG NB_GID="1000"

# install OS dependencies and perform OS operations (e.g. set your user with passwordless sudo)
RUN apt-get update && \
  apt-get install -y sudo && \
  apt-get install -y python3-dev && \
  useradd -m -s /bin/bash -N -u $NB_UID $NB_USER && \
  chmod g+w /etc/passwd && \
  # give NB_USER passwordless sudo
  echo "${NB_USER}    ALL=(ALL)    NOPASSWD:    ALL" >> /etc/sudoers && \
  # Prevent apt-get cache from being persisted to this layer.
  rm -rf /var/lib/apt/lists/*


# Copy requirements, install and configure the kernel.
COPY --chown="${NB_UID}:${NB_GID}" "pip-requirements.txt" "/tmp/"
RUN pip install -r "/tmp/pip-requirements.txt"

# set default shell, user, working directory and default command when executing the container
ENV SHELL=/bin/bash

USER $NB_UID

WORKDIR "/home/${NB_USER}"

CMD ["jupyter", "lab", "--no-browser", "--ip=0.0.0.0"]
```

Then you can build this into an image with `build.sh` (remember to assign executable permission to the user aka `chmod u+x build.sh`):

```bash
#!/bin/bash

if [ -z "$IMAGETAG" ]; then
    IMAGETAG="latest"
fi

docker build --force-rm -t my_image:${IMAGETAG} .
```

you can pass different arguments for setting your user (see [build-time variables](https://docs.docker.com/engine/reference/commandline/build/#set-build-time-variables---build-arg))

Then you can create your container for the __first time__ with this script in `run.sh`:

```bash
#!/bin/bash

if [ -z "$IMAGETAG" ]; then
    IMAGETAG="latest"
fi

if [ -z "$DOCKERPORT" ]; then
    DOCKERPORT="8888"
fi

docker run -it -p 127.0.0.1:${DOCKERPORT}:8888 \
  -v `dirname ${PWD}`:/home/${USER}/work \
  --name my_container_name my_image:${IMAGETAG}
```

and subsequently run it interactively the next times using `start.sh`:

```bash
#!/bin/bash

docker start -i my_container_name
```

The output is:

![]({attach}images/jupyterlab-docker/jupyter-docker-start.png)

and you can `CTRL + click` in the link to open your `Jupyter Lab` session in your browser. `CTRL + C` to stop the execution. For MAC user use the `Command` key instead of `CTRL`.

# Discussion Points

## Why we need a specific user in your image

By default, all containers are run as `root` user, so when you mount your working folder, you might modify some files and/or create new ones with different perissions, and will not be able to modify them outside the container, unless you change them with `chown` command.

## How big is my image is going to be?

A basic `python 3.8` image with:

```
pandas
numpy
matplotlib
jupyterlab
```

is about 1.3 GB.

## Jupyter Lab versions

From Jupyter Lab 3.0 the installation of the plugins changed. In summary you can install extension such as [interactive matplotlib](https://github.com/matplotlib/ipympl#with-pip) without executing `jupyter labextension install ...` but like a normal python package `pip install myextension` as documented in the [changelog](https://jupyterlab.readthedocs.io/en/stable/getting_started/changelog.html#user-facing-changes).

## Python vs miniconda vs community stacks

I prefer generally to install packages with pip when are for "production" stacks, or stacks that are sort of compartmentalised, but in general you can use the miniconda image, as a base for your `Dockerfile` or the [community stacks](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#selecting-an-image). Both the latter and miniconda images are a bit bigger than standard python images and you can pull them down and use them without building your own dockerfile.

## Install the plugins

With Jupyter Lab > 3.0 you can install widgets and plugins with `pip`. As example here the instructions to install the [interactive matplotlib widget](https://github.com/matplotlib/ipympl#with-pip).
