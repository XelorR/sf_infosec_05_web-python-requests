FROM python:3.11

COPY requirements.txt .

RUN apt-get update && apt-get install -y iputils-ping
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD mkdir -p /workspace/log /workspace/app
WORKDIR /workspace
ADD scanner.py .
ADD ./app/__init__.py /workspace/app/
ADD ./app/lib.py /workspace/app/
ADD ./app/server.py /workspace/app/
CMD sed -i 's/127.0.0.1/0.0.0.0/' app/server.py

ENTRYPOINT ["python", "scanner.py"]
