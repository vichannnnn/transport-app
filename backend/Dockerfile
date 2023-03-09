FROM python:3.10

WORKDIR ./app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

EXPOSE 8000

RUN pip install types-Pygments types-colorama types-setuptools types-ujson
RUN pip install --no-cache-dir --upgrade pip
RUN pip install -r ./app/requirements.txt
