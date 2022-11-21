# Web app for object detection with YOLO V7

A simple web app allowing end users to 
- submit an image and perform object detection
- submit a coorrection when detection is incorrect

## Requirement

See requirements.txt for updates.

```sh
requests==2.27.1
fastapi==0.72.0
uvicorn==0.17.0
python-dotenv==0.19.2
aiofiles==0.8.0
python-multipart==0.0.5
jinja2==3.0.3
Markdown==3.3.6
pytest==6.2.5
python-jose
```

## Installation & Usage

```bash
# install packages
$ pip install -r requirements.txt
# start the web app FO
export od_webapp_instance=FO
$ uvicorn app.main:app --reload --port 8010
# start the web app BO
export od_webapp_instance=BO
$ uvicorn app.main:app --reload --port 8011
```

Visit [http://127.0.0.1:8001/](http://127.0.0.1:8001/).


All tests are under `tests` directory.

```bash
# Run tests
$ pytest -v
```

## Authors

François JEAN-CHARLES et Noël HENROT
