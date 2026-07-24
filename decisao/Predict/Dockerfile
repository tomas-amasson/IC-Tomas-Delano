FROM python:3.12.3
WORKDIR /dec

ENV TZ=America/Sao_Paulo


COPY libs.txt .
COPY testmodel.pmml .

RUN apt-get update
RUN apt-get install -y --no-install-recommends default-jre
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r libs.txt

EXPOSE 3308
CMD ["python3", "predictAPI.py"]
