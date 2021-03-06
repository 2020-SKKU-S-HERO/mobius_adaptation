# Mobius 플랫폼 서버 구성
- Mobius 플랫폼은 oneM2M 표준을 따르는 IoT 서버 플랫폼으로 수평적인 포맷을 지향한다.

<br>

## 현재 상태
- 아두이노 Featehr M0 에서 보낸 데이터를 모비우스 서버에서 받는다.
- 받은 데이터들을 mobius DB에 저장한다.
- mobius DB에 저장돼있는 데이터들을 처리해서 shero DB에 저장한다. 이 과정을 1분 주기로 반복한다.

## 과제
- 예측 모델을 만들어 들어온 데이터들을 학습시킨다.
- 모델, DB를 제어할 수 있게 만든다.

<br>

## 구글 클라우드 플랫폼

구글 클라우드 플랫폼에 리눅스 서버를 구축하였다.


### 예측 모델 학습, 사용 방법
- 계정마다 파이썬 라이브러리가 달라진다. 현재 anaconda는 rsa-key 계정에 설치돼있다.
- rsa-key 계정으로 로그인하여 python (파일명)을 실행한다.
```python script
  python db_import.py
```

### 가상환경 접속
- 가상환경을 사용하면 모든 유저들 간에 통일된 환경을 사용할 수 있다.
- 다음 코드를 실행한다.
```python script
  conda activate carbon
```

### 접속 방법

ssh를 사용하여 접속할 수 있다. rsa key는 rsa-gcp-key 파일을 사용한다.
rsa-gcp-key 파일이 있는 곳에서 터미널을 열고 다음의 쉘 명령어를 입력한다.
외부 아이피는 34.64.238.233이다.

```shell script
ssh -i ./rsa-gcp-key shero@34.64.238.233
```

shell을 사용하지 않을 경우 putty_gen을 사용하여 rsa-key를 생성한다.
private key는 적당한 장소에 저장하고, public key를 GCP(Google Clout Platform)에 등록한다.
putty를 사용하여 '이름@34.64.238.233'으로 접속하면 된다.

### 서버 상태

구글 클라우드 플랫폼의 리눅스 서버에 MySQL과 mosquitto, Grafana를 구축하였고,
백그라운드에 파이썬으로 작성된 구독자 프로그램을 실행 중이다.

#### MySQL

MySQL은 서버 내부에서 root로 접속할 수 있다.

```shell script
mysql -u root -p
```
password는 shero이다.

서버 외부에서는 shero로 접속할 수 있다.

```shell script
mysql -h 34.64.238.233 -u shero -p
```

'sheroDB'라는 이름의 DB가 생성되어 있고, 그 안에 'co2_emissions'라는 이름의 테이블이 생성되어 있다.
해당 테이블의 열은 date_time, emissions로 2개이고, 각각 DATETIME, DOUBLE(7, 2) 타입을 갖는다.
<br>
<br>

------
Thanks to KETI for opening these marvelous codes. 

# Mobius
oneM2M IoT Server Platform

## Version
2.4.x (2.4.42)

## Introduction
Mobius is the open source IoT server platform based on the oneM2M (http://www.oneM2M.org) standard. As oneM2M specifies, Mobius provides common services functions (e.g. registration, data management, subscription/notification, security) as middleware to IoT applications of different service domains. Not just oneM2M devices, but also non-oneM2M devices (i.e. by oneM2M interworking specifications and KETI TAS) can connect to Mobius.

## Certification
Mobius has been received certification of ‘oneM2M standard’ by TTA (Telecommunications Technology Association). oneM2M Certification guarantees that oneM2M products meet oneM2M Specification and Test requirements which ensure interoperability. As Mobius is certified, it will be used as a golden sample to validate test cases and testing system.

<div align="center">
<img src="https://user-images.githubusercontent.com/29790334/40639101-e9ecd06c-6349-11e8-9fc2-0806d9bf5dc7.png" width="800"/>
</div>

TRSL (Test Requirements Status List) is available on oneM2M certification website (http://www.onem2mcert.com/sub/sub05_01.php).

## System Stucture
In oneM2M architecture, Mobius implements the IN-CSE which is the cloud server in the infrastructure domain. IoT applications communicate with field domain IoT gateways/devices via Mobius.

<div align="center">
<img src="https://user-images.githubusercontent.com/29790334/28322739-d7fddbc4-6c11-11e7-9180-827be6d997f0.png" width="800"/>
</div>

## Connectivity Stucture
To enable Internet of Things, things are connected to &Cube via TAS (Thing Adaptation Software), then &Cube communicate with Mobius over oneM2M standard APIs. Also IoT applications use oneM2M standard APIs to retrieve thing data control things of Mobius.

<div align="center">
<img src="https://user-images.githubusercontent.com/29790334/28322868-33e97f4c-6c12-11e7-97fc-6de66c06add7.png" width="800"/>
</div>

## Software Architecture

<div align="center">
<img src="https://user-images.githubusercontent.com/29790334/28245393-a1159d5e-6a40-11e7-8948-4262bf29c371.png" width="800"/>
</div>

## Supported Protocol Bindings
- HTTP
- CoAP
- MQTT
- WebSocket

## Installation
The Mobius is based on Node.js framework and uses MySQL for database.
<div align="center">
<img src="https://user-images.githubusercontent.com/29790334/28322607-7be7d916-6c11-11e7-9d20-ac07961971bf.png" width="600"/>
</div><br/>

- [MySQL Server](https://www.mysql.com/downloads/)<br/>
The MySQL is an open source RDB database so that it is free and ligth. And RDB is very suitable for storing tree data just like oneM2M resource stucture. Most of nCube-Rosemary will work in a restricted hardware environment and the MySQL can work in most of embeded devices.

- [Node.js](https://nodejs.org/en/)<br/>
Node.js® is a JavaScript runtime built on Chrome's V8 JavaScript engine. Node.js uses an event-driven, non-blocking I/O model that makes it lightweight and efficient. Node.js' package ecosystem, npm, is the largest ecosystem of open source libraries in the world. Node.js is very powerful in service impelementation because it provide a rich and free web service API. So, we use it to make RESTful API base on the oneM2M standard.

- [Mosquitto](https://mosquitto.org/)<br/>
Eclipse Mosquitto™ is an open source (EPL/EDL licensed) message broker that implements the MQTT protocol versions 3.1 and 3.1.1. MQTT provides a lightweight method of carrying out messaging using a publish/subscribe model. This makes it suitable for "Internet of Things" messaging such as with low power sensors or mobile devices such as phones, embedded computers or microcontrollers like the Arduino.

- [Mobius](https://github.com/IoTKETI/Mobius/archive/master.zip)<br/>
Mobius source codes are written in javascript. So they don't need any compilation or installation before running.

## Mobius Docker Version
We deploy Mobius as a Docker image using the virtualization open source tool Docker.

- [Mobius_Docker](https://github.com/IoTKETI/Mobius_Docker)<br/>

## Configuration
- Import SQL script<br/>
After installation of MySQL server, you need the DB Schema for storing oneM2M resources in Mobius. You can find this file in the following Mobius source directory.
```
[Mobius home]/mobius/mobiusdb.sql
```
- Run Mosquitto MQTT broker<br/>
```
mosquitto -v
```
- Open the Mobius source home directory
- Install dependent libraries as below
```
npm install
```
- Modify the configuration file "conf.json" per your setting
```
{
  "csebaseport": "7579", //Mobius HTTP hosting  port
  "dbpass": "*******"    //MySQL root password
}
```

## Run
Use node.js application execution command as below
```
node mobius.js
```

<div align="center">
<img src="https://user-images.githubusercontent.com/29790334/28245526-c9db7850-6a43-11e7-9bfd-f0b4fb20e396.png" width="700"/>
</div><br/>

## Library Dependencies
This is the list of library dependencies for Mobius 
- body-parser
- cbor
- coap
- crypto
- events
- express
- file-stream-rotator
- fs
- http
- https
- ip
- js2xmlparser
- merge
- morgan
- mqtt
- mysql
- shortid
- url
- util
- websocket
- xml2js
- xmlbuilder

## Document
If you want more details please download the full [installation guide document](https://github.com/IoTKETI/Mobius/raw/master/doc/Installation%20Guide_Mobius_v2.0.0_EN(170718).pdf).

# Author
Jaeho Kim (jhkim@keti.re.kr)
Il Yeup Ahn (iyahn@keti.re.kr)
