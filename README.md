# ht-poker
## Scala bootcamp hometask.

Script supports three game types: texas-holdem, omaha-holdem, five-card-draw.How to run and build:
* Generate personal access token ((account) Settings -> Developer settings)
* Copy following to your Dockerfile:

```
FROM ubuntu:latest
RUN apt-get update
RUN apt-get -q -y install curl zip unzip git
RUN curl -O -J -L -u <your-token>:x-oauth-basic https://github.com/NeoIsALie/ht-poker/archive/main.zip
RUN unzip ht-poker-main.zip
WORKDIR /ht-poker-main
COPY input.txt /ht-poker-main
COPY output.txt /ht-poker-main
RUN chmod +x prepare.sh
RUN chmod +x run.sh
```
* Build image and run using:
```
docker build -t poker:latest .
docker run -i -t -p 5902:5902 --name "poker" poker:latest bash
```

* Run prepare.sh inside container to install python3.8:
```./prepare.sh```

* Run run.sh using (where <input> and <output> are input and output file names respectively):
```./run.sh < <input>.txt  > <output>.txt```
