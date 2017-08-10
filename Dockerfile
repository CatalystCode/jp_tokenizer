FROM alpine:3.6

ENV MECAB_VERSION 0.996
ENV IPADIC_VERSION 2.7.0-20070801
ENV BUILD_DEPENDENCIES "build-base curl git bash file sudo openssh python3-dev"

# Install MeCab with Neologd
RUN apk add --update --no-cache ${BUILD_DEPENDENCIES} \
  && apk add --update --no-cache openssl \
  && curl -SLO "https://mecab.blob.core.windows.net/files/mecab-${MECAB_VERSION}.tar.gz" \
  && tar zxf mecab-${MECAB_VERSION}.tar.gz \
  && cd mecab-${MECAB_VERSION} \
  && ./configure --enable-utf8-only --with-charset=utf8 \
  && make \
  && make install \
  && cd \
  && curl -SLO "https://mecab.blob.core.windows.net/files/mecab-ipadic-${IPADIC_VERSION}.tar.gz" \
  && tar zxf mecab-ipadic-${IPADIC_VERSION}.tar.gz \
  && cd mecab-ipadic-${IPADIC_VERSION} \
  && ./configure --with-charset=utf8 \
  && make \
  && make install \
  && cd \
  && git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git \
  && mecab-ipadic-neologd/bin/install-mecab-ipadic-neologd -n -y
ENV MECAB_OPTS "-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/"

# Install Python 3.6
RUN apk add --no-cache python3 libstdc++ \
  && python3 -m ensurepip \
  && rm -r /usr/lib/python*/ensurepip \
  && pip3 install --upgrade pip setuptools \
  && if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip; fi

# Set up tokenizer server
ADD requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt
ADD run_server.py /server.py

# Cleanup
RUN apk del ${BUILD_DEPENDENCIES} \
  && rm -rf mecab-${MECAB_VERSION}* mecab-ipadic-${IPADIC_VERSION}* mecab-ipadic-neologd \
  && rm -r /root/.cache \
  && rm /app/requirements.txt

EXPOSE 80
CMD ["python3.6", "/server.py", "--port", "80"]
