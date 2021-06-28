FROM amazonlinux:latest

ENV DATABASE_HOST="xyz.com"
ENV DATABASE_USER="xyzuser"
ENV DATABASE_PASSWORD="xyz"
ENV DATABASE_DB_NAME="xyz"
ENV DATABASE_PORT=5432

RUN yum -y update && \
    amazon-linux-extras enable postgresql11 && \
    yum install -y postgresql postgresql-contrib postgresql-devel && \
    yum -y install gcc gcc-devel && \
    yum -y install python3 python3-devel initscripts && \
    mkdir -p /octank/app

WORKDIR /octank

COPY app.py .
COPY requirements.txt .
COPY app/ ./app/

RUN pip3 install -r requirements.txt

CMD ["python3", "app.py"]
