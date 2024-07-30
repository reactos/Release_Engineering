FROM ubuntu:24.04
LABEL org.opencontainers.image.authors="Mark Jansen <mark.jansen@reactos.org>"
LABEL Description="RosBE-Unix on Ubuntu with Release Engineering scripts"

WORKDIR /work

# The settings `DEBIAN_FRONTEND="noninteractive" TZ="Europe/Amsterdam"` are for `texinfo`
RUN apt-get update -y \
    && apt-get upgrade -y \
    && DEBIAN_FRONTEND="noninteractive" TZ="Europe/Amsterdam" apt-get install -y \
        bison \
        build-essential \
        flex \
        git \
        nano \
        p7zip-full \
        pkg-config \
        python-is-python3 \
        python3 \
        texinfo \
        wget \
        zip \
        zlib1g-dev \
        && rm -rf /var/lib/apt/lists/*

RUN wget https://downloads.sourceforge.net/reactos/RosBE-Unix-2.2.1.tar.bz2 \
    && tar -xjf RosBE-Unix-2.2.1.tar.bz2 \
    && rm RosBE-Unix-2.2.1.tar.bz2 \
    && cd RosBE-Unix-2.2.1 \
    && echo yes | bash RosBE-Builder.sh /usr/local/RosBE \
    && cd .. \
    && rm -rf RosBE-Unix-2.2.1

RUN git clone https://github.com/learn-more/Release_Engineering \
    && mv Release_Engineering/Release_* /usr/local/bin \
    && rm -rf Release_Engineering

CMD ["/usr/local/RosBE/RosBE.sh", "/work"]
