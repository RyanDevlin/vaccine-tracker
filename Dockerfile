FROM python:latest

WORKDIR /root/
COPY setup.py requirements.txt ./
COPY ./src/ ./src/

# Since we issue http(s) requests, we need to install
# certificate authority certificates from the
# ca-certificates package inside the container
RUN apt-get update
RUN apt install -y firefox-esr
RUN pip install -r requirements.txt
RUN python setup.py build
RUN python setup.py install

# Expose metadata to explain that these ports are used by the application
EXPOSE 80 443

ENTRYPOINT [ "python", "src/track_vaccine.py" ]