FROM python:3
WORKDIR /
ENV DEBIAN_FRONTEND=noninteractive
COPY . ./

RUN pip install --default-timeout=100 -r ./requirements.txt
EXPOSE 8080
RUN chmod 777 lauching.sh

CMD ./lauching.sh
