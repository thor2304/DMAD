FROM python:3.12-rc-slim

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN pip install -e . --no-deps

CMD python3 DMAD/CODE/main.py