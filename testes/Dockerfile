FROM python:3.12.3
WORKDIR /api

# somente dependencias para deixar o api mutável
COPY libraries.txt .
RUN pip install --no-cache-dir -r libraries.txt

# para imagem autossuficiente
#COPY . .

EXPOSE 5000
CMD ["python3", "class_selector.py"]