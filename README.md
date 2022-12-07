# Image Retrieval (Touche Task 3)

## Download repository

Clone the Repository. Open git bash in the local folder of the repository. 
Enter the commands `git submodule init` and `git submodule update` to download
also the submodule **touche-code**.

## Start the local docker server

Make sure that Docker Desktop is installed with WSL. Then execute the 
`container/start-jupyter-docker.bat` file.

## Explanation of data structure

Data of datset from last year should be saved in `container/dataset22`.

The `touche-code` submodule is savd in `container/touche-code`.

All self written data for the task should be saved in `container/workspace`. 

In jupyter lab on the docker server only the workspace directory is shown. 
The dataset22 directory and the submodule as the directory `baseline` is 
linked into the workspace directory and shown there.

