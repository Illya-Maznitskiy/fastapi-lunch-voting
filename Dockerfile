FROM ubuntu:latest
LABEL authors="comer"

ENTRYPOINT ["top", "-b"]