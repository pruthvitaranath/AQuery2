# Installation:
## Requirements

## Docker: 
   - See installation instructions from [docker.com](https://www.docker.com). Run **docker desktop** to start docker engine.
   - docker pull sunyinqi0508/aquery
     
## Installing Aquery
   - git clone https://github.com/sunyinqi0508/AQuery2
   - cd AQuery2
   - git checkout tags/0.4.8a -b adb_hw
   - python3 -m venv venc (create a virtual env)
   - source venc/bin/activate (activate the virtual env)
   - export CXX=clang++-14 / export CXX=clang++
   - brew install monetdb
   - python3 pip install -r requirements.txt
   - docker run -d sunyinqi0508/aquery
   - docker ps -a (should see that your container is created)
   - python3 prompt.py


You can try installing it on your CIMS server as well. However, newly created accounts might not have access to older GCC modules (11.2), which could cause an issue while running the CIMS patch (step 2).
## CIMS Computer Lab (Only for NYU affiliates who have access)
  1. Clone this git repo in CIMS.
  2. Download the [patch](https://drive.google.com/file/d/1YkykhM6u0acZ-btQb4EUn4jAEXPT81cN/view?usp=sharing) 
  3. Decompress the patch to any directory and execute script inside by typing (`source ./cims.sh`). Please use the source command or `. ./cims.sh` (dot space) to execute the script because it contains configurations for environment variables. Also note that this script can only work with bash and compatible shells (e.g. dash, zsh. but not csh)
  4. Execute `python3 ./prompt.py`
