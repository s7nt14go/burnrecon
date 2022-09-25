#!/usr/bin/env bash

printf "Installing tools 🔧\n\n"

go env -w GO111MODULE=auto
# Enum subdomains
echo "Install Amass"
go install github.com/OWASP/Amass/v3/...@latest
echo "Install assetfinder"
go install github.com/tomnomnom/assetfinder@latest
echo "Install subfinder"
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
echo "Install Naabu"
apt install -y libpcap-dev
go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
echo "Install Chaos"
go install -v github.com/projectdiscovery/chaos-client/cmd/chaos@latest
echo "Install Haktrails"
go install -v github.com/hakluke/haktrails@latest
echo "  Criando arquivo de configuração para o Haktrails"
mkdir -p ~/.config/haktools
touch ~/.config/haktools/haktrails-config.yml
echo "Instalando o github-search"
mkdir -p ~/tools
cd ~/tools
git clone https://github.com/gwen001/github-search.git
cd github-search
pip3 install -r requirements3.txt

echo "Instalando findomain"
curl -LO https://github.com/Findomain/Findomain/releases/download/8.2.1/findomain-linux.zip
unzip findomain-linux.zip
chmod +x findomain
mv findomain /usr/bin
rm findomain-linux.zip

# Check if subdomains are alive
echo "Install httpx"
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest


