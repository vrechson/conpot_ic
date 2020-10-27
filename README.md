# APRIMORAMENTO DE HONEYNETS INDUSTRIAIS: DA IMPLEMENTAÇÃO DE NOVOS PROTOCOLOS À EVASÃO DE SERVIÇOS DE DETECÇÃO DE HONEYPOTS
Este repositório abriga o material estudado e desenvolvido durante a iniciação cientifica realizada na Universidade Federal de São Carlos. 

## Detalhes do Projeto
Para executar o container basta utilizar as linhas a seguir:

```
# Para baixar o repositório:
$ git clone git@github.com:vrechson/conpot_ic.git
$ cd conpot_ic

# Para buildar a imagem do container
$ cd conpot
$ docker build . -t conpot

# Para executar o template padrão
$ docker run -it -p 80:8800 -p 102:10201 -p 502:5020 -p 2323:2323 -p 161:16100/udp -p 47808:47808/udp -p 623:6230/udp -p 21:2121 -p 69:6969/udp -p 44818:44818 --network=bridge conpot

# Para executar o template do PLC SIMATIC 300(1)
$ docker run -it -p 80:8800 -p 102:10201 -p 502:5020 -p 2323:2323 -p 161:16100/udp -p 47808:47808/udp -p 623:6230/udp -p 21:2121 -p 69:6969/udp -p 44818:44818 --network=bridge conpot -f -t simatic_3000

# Para executar o template do PLC Sri Lanka Telecom PLC
$ docker run -it -p 80:8800 -p 102:10201 -p 502:5020 -p 2323:2323 -p 161:16100/udp -p 47808:47808/udp -p 623:6230/udp -p 21:2121 -p 69:6969/udp -p 44818:44818 --network=bridge conpot -f -t SriLankaTelecom
```

## O que foi feito
- [X] Tarefa 1: Implementação do protocolo TELNET no projeto Conpot
- [X] Tarefa 2: Criação de novos templates para o Conpot
- [X] Tarefa 3: Pesquisa operacional sobre o funcionamento do projeto Honeypot Or Not do Shodan
- [X] Tarefa 4: Planejamento de possíveis evasões para os métodos de detecção do Honeypot Or Not

Os resultados para cada um desses tópicos estão apresentados no documento da pesquisa.
