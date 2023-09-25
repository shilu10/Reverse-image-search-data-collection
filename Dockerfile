FROM python:3.8.9-alpine3.13 as pythonBuilder
WORKDIR /home/root/server
# any dependencies in python which requires a compiled c/c++ code (if any)
RUN apk update && apk add --update gcc libc-dev linux-headers libusb-dev
COPY . .
RUN pip3 install --target=/home/root/server/dependencies -r requirements.txt

FROM python:3.8.9-alpine3.13
WORKDIR /home/root/server
# include runtime libraries (if any)
RUN apk update && apk add libusb-dev
COPY --from=pythonBuilder	/home/root/server .
ENV PYTHONPATH="${PYTHONPATH}:/home/root/server/dependencies"

EXPOSE 8080

CMD ["python3", "app.py"]



FROM python:3.8.9-alpine3.13 as pythonBuilder
RUN apt-get update && apt-get install -y --no-install-recommends build-essential gcc && apt-get clean
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /app

FROM python:3.8.9-alpine3.13 as runtime-image
COPY --from=compile-image /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY . /app
## Replace my-app.py by yours :)
EXPOSE 8080

CMD ["python3", "app.py"]


