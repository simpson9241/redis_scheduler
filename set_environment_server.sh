# this is for ubuntu 20.04

cd ~/;
sudo apt-get update;
sudo apt-get upgrade;
sudo apt-get install python3-pip;
sudo apt-get update;
sudo apt-get upgrade;
sudo apt-get install redis-server;
sudo pip3 install rq;
redis-server --version;