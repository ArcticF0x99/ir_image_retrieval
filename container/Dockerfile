# syntax=docker/dockerfile:1
FROM webis/tira-touche23-task-3-pyterrier-baseline:0.0.1

COPY workspace/requirements.txt /requirements.txt
WORKDIR /

RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_lg
COPY workspace/stable-diffusion-v1-4 /workspace/stable-diffusion-v1-4
COPY workspace/bart-large-mnli /workspace/bart-large-mnli

COPY workspace/*.py /workspace
COPY workspace/*.ipynb /workspace

ENV MAX_QUERIES 3