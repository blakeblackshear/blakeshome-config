FROM nginx:stable

LABEL maintainer="Blake Blackshear <blakeb@blakeshome.com>"

ENV NAXSI_VERSION 0.56

RUN set -x \
	&& apt-get update \
	&& apt-get install --no-install-recommends --no-install-suggests -y \
		curl \
		apt-transport-https \
		ca-certificates \
		build-essential \
		libpcre3-dev
	
RUN curl -fSL https://github.com/nbs-system/naxsi/archive/$NAXSI_VERSION.tar.gz -o naxsi.tar.gz \
	&& tar -zxC /usr/src -f naxsi.tar.gz \
	&& rm naxsi.tar.gz

RUN export NGINX_SRC_VERSION=${NGINX_VERSION%-*} \
	&& curl -fSL https://nginx.org/download/nginx-$NGINX_SRC_VERSION.tar.gz -o nginx.tar.gz \
	&& tar -zxC /usr/src -f nginx.tar.gz \
	&& rm nginx.tar.gz \
	&& cd /usr/src/nginx-$NGINX_SRC_VERSION \
	&& ./configure --with-compat --add-dynamic-module=/usr/src/naxsi-$NAXSI_VERSION/naxsi_src --without-http_gzip_module \
    && make modules \
    && cp objs/ngx_http_naxsi_module.so /etc/nginx/modules \
	&& apt-get remove --purge --auto-remove -y apt-transport-https ca-certificates \
	&& rm -rf /var/lib/apt/lists/* \
	&& rm -rf /usr/src/naxsi-$NAXSI_VERSION \
    && rm -rf /usr/src/nginx-$NGINX_SRC_VERSION