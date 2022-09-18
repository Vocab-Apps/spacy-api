# building for dev:
# docker build -t lucwastiaux/cloud-language-tools:dev -f Dockerfile .
# docker push lucwastiaux/cloud-language-tools:dev
# 
# pushing to digitalocean registry
# docker tag lucwastiaux/cloud-language-tools:dev-3 registry.digitalocean.com/luc/cloud-language-tools:dev-3
# docker push registry.digitalocean.com/luc/cloud-language-tools:dev-3

# running locally:
# docker run --env-file /home/luc/python/cloud-language-tools-secrets/cloud-language-tools-local  -p 0.0.0.0:8042:8042/tcp lucwastiaux/cloud-language-tools:20220902-7
# inspecting space usage
# docker container exec 224e53da8507 du -hc --max-depth=1 /root

FROM ubuntu:20.04

# use ubuntu mirrors
RUN sed -i -e 's|archive\.ubuntu\.com|mirrors\.xtom\.com\.hk|g' /etc/apt/sources.list
# install packages first
RUN apt-get update -y && apt-get install -y python3-pip

# update pip
RUN pip3 install --upgrade pip

# install requirements
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt && pip3 cache purge

# install spacy modules
RUN python3 -m spacy download en_core_web_trf
RUN python3 -m spacy download fr_dep_news_trf
RUN python3 -m spacy download zh_core_web_trf

# copy app files
COPY api.pi start.sh ./

EXPOSE 8042
ENTRYPOINT ["./start.sh"]
