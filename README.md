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
 1. git clone https://github.com/sunyinqi0508/AQuery2
 2.  cd AQuery2
 3.  git checkout tags/0.4.8a -b adb_hw
 4.  If installing on CIMS (recommended), you also need to download this(https://drive.google.com/file/d/1YkykhM6u0acZ-btQb4EUn4jAEXPT81cN/view) patch and upload it to your server using the below command:
    scp ./centos.zip <netid>@access.cims.nyu.edu:/home/<netid>/
 5. Login to CIMS
 6. Unzip centos.zip
 7. cd centos
 8. chmod u+x cims.sh
 9. nano cims.sh (change export CXX=g++-11.2 to export CXX=g++) and save it
 10. .  ./cims.sh (to run the script)
 11. python3 pip install -r requirements.txt
 12. python3 ./prompt.py
    
