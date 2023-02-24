#!/bin/bash
docker run --rm -ti --gpus=all \
    -p 8888:8888 \
    -v "${PWD}/touche-code/clef23/image-retrieval-for-arguments/baseline-pyterrier:/workspace/baseline" \
    -v "${PWD}/dataset23:/workspace/dataset23" \
    -v "${PWD}/workspace:/workspace" \
    webis/tira-touche23-task-3-pyterrier-baseline:0.0.1 \
    jupyter-lab --allow-root --ip 0.0.0.0

