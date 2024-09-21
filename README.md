# Installation:
## Requirements

## Docker (Recommended): 
   - See installation instructions from [docker.com](https://www.docker.com). Run **docker desktop** to start docker engine.
   - In AQuery root directory, type `make docker` to build the docker image from scratch. 
   - For Arm-based Mac users, you would have to build and run the **x86_64** docker image because MonetDB doesn't offer official binaries for arm64 Linux. (Run `docker buildx build --platform=linux/amd64 -t aquery .` instead of `make docker`)
   - Finally run the image in **interactive** mode (`docker run --name aquery -it aquery`) 
   - When you need to access the container again run `docker start -ai aquery` 
   - If there is a need to access the system shell within AQuery, type `dbg` to activate python interpreter and type `os.system('sh')` to launch a shell.
   - Docker image is available on [Docker Hub](https://hub.docker.com/repository/docker/sunyinqi0508/aquery) but building image yourself is highly recommended (see [#2](../../issues/2)) 
## CIMS Computer Lab (Only for NYU affiliates who have access)
  1. Clone this git repo in CIMS.
  2. Download the [patch](https://drive.google.com/file/d/1YkykhM6u0acZ-btQb4EUn4jAEXPT81cN/view?usp=sharing) 
  3. Decompress the patch to any directory and execute script inside by typing (`source ./cims.sh`). Please use the source command or `. ./cims.sh` (dot space) to execute the script because it contains configurations for environment variables. Also note that this script can only work with bash and compatible shells (e.g. dash, zsh. but not csh)
  4. Execute `python3 ./prompt.py`
