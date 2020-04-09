FROM edxops/xenial-common:latest
RUN apt-get update && apt-get install -y \
    gettext \
    lib32z1-dev \
    libjpeg62-dev \
    libxslt-dev \
    libz-dev \
    python3 \
		python3-pip \
&& rm -rf /var/lib/apt/lists/*

RUN virtualenv venv
RUN chmod u+x venv/bin/activate
RUN venv/bin/activate

ADD xblock-sdk/requirements/dev.txt /tmp/dev.txt
RUN pip3 install -r /tmp/dev.txt \
&& rm /tmp/dev.txt

RUN curl -sL https://deb.nodesource.com/setup_10.x -o /tmp/nodejs-setup
RUN /bin/bash /tmp/nodejs-setup
RUN rm /tmp/nodejs-setup
RUN apt-get -y install nodejs

RUN mkdir -p /usr/local/src/
WORKDIR /usr/local/src/
ADD . .

RUN bash setup-custom-xblocks.sh

WORKDIR /usr/local/src/xblock-sdk
RUN make install

EXPOSE 8000
ENTRYPOINT ["python3", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
