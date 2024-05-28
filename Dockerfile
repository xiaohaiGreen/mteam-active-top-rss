FROM python:3.11.9-bullseye
ENV BASE_DIR="/home/apps"

WORKDIR ${BASE_DIR}
COPY requirements.txt docker_entrypoint.sh src  ./
RUN pip install -r requirements.txt && \
    mkdir log && \
    chmod +x docker_entrypoint.sh
CMD [ "./docker_entrypoint.sh"]