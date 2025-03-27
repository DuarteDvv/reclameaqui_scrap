sudo apt update && sudo apt upgrade -y
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y && sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev -y
python3.12 -m venv venv
source venv/bin/activate

# systemd

sudo cp scrap.service /etc/systemd/system/ 
sudo rm /etc/systemd/system/scrap.service  
sudo systemctl daemon-reload
sudo systemctl enable scrap.service
sudo systemctl start scrap.service
systemctl status scrap.service