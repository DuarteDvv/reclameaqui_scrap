# instalando env

sudo apt update && sudo apt upgrade -y
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y && sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev -y
python3.12 -m venv venv
source venv/bin/activate

# shellscript

Para utilizar adapte o .sh a sua máquina mudando caminhos 

chmod +X ./scrap.sh
chmod 755 ./scrap.sh

./scrap.sh

# recomendações 

Execute utilizando o scrap.sh pois permite que o script seja resistente a problemas de rede, capchas aleatorios e timeouts


