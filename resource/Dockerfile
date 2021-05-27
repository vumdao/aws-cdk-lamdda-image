FROM amazon/aws-lambda-python:3.8

RUN yum -y update && \
    yum install -y python3-pip && \
    pip3 install requests

COPY app.py ./

CMD ["app.handler"]
