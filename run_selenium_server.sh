docker rm -f selenium-server 
docker run -d -p 4444:4444 --shm-size="2g" --network host -e SE_VNC_NO_PASSWORD='1' --name selenium-server selenium/standalone-chrome:4.4.0-20220812