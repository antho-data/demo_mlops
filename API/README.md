# API for object detection with YOLO V7

A simple API allowing end users to 
- submit an image and perform object detection
- submit a correction when detection is incorrect

## Requirement

See requirements.txt for updates.

```sh
absl-py==1.2.0
anyio==3.6.1
asttokens==2.0.8
backcall==0.2.0
bcrypt==4.0.0
cachetools==5.2.0
certifi==2022.6.15
charset-normalizer==2.1.1
click==8.1.3
colorama==0.4.5
cycler==0.11.0
decorator==5.1.1
ecdsa==0.18.0
executing==1.0.0
fastapi==0.81.0
fonttools==4.37.1
google-auth==2.11.0
google-auth-oauthlib==0.4.6
greenlet==1.1.3
grpcio==1.48.1
gunicorn==20.1.0
h11==0.13.0
idna==3.3
ipython==8.4.0
jedi==0.18.1
kiwisolver==1.4.4
Markdown==3.4.1
MarkupSafe==2.1.1
matplotlib==3.5.3
matplotlib-inline==0.1.6
numpy==1.23.2
oauthlib==3.2.0
opencv-python==4.6.0.66
packaging==21.3
pandas==1.4.4
parso==0.8.3
passlib==1.7.4
pickleshare==0.7.5
Pillow==9.2.0
prompt-toolkit==3.0.31
protobuf==3.19.4
psutil==5.9.1
psycopg2-binary==2.9.3
pure-eval==0.2.2
pyasn1==0.4.8
pyasn1-modules==0.2.8
pydantic==1.10.1
Pygments==2.13.0
pyparsing==3.0.9
python-dateutil==2.8.2
python-jose==3.3.0
python-multipart==0.0.5
pytz==2022.2.1
PyYAML==6.0
requests==2.28.1
requests-oauthlib==1.3.1
rsa==4.9
scipy==1.9.1
seaborn==0.11.2
six==1.16.0
sniffio==1.3.0
SQLAlchemy==1.4.36
stack-data==0.5.0
starlette==0.19.1
tensorboard==2.10.0
tensorboard-data-server==0.6.1
tensorboard-plugin-wit==1.8.1
thop==0.1.1.post2207130030
torch==1.12.1
torchvision==0.13.1
tqdm==4.64.1
traitlets==5.3.0
typing_extensions==4.3.0
urllib3==1.26.12
uvicorn==0.18.3
wcwidth==0.2.5
Werkzeug==2.2.2
```

## Installation & Usage

```bash
# install packages
$ pip install -r requirements.txt
# start the server
$ uvicorn app.main:app --reload --port 8000

```
  - pour lancer l'api Front Office
    - set od_api_instance=FO
    - uvicorn app.main:app --reload --port 8000
  - pour lancer l'api Back Office
    - set od_api_instance=BO
    - uvicorn app.main:app --reload --port 8001

Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/).


All tests are under `tests` directory.

```bash
# Run tests
$ pytest -v
```

## Authors

François JEAN-CHARLES et Noël HENROT