FROM python:3.10.4-slim-buster

WORKDIR /web

#copy the current contents into the containger at /app
COPY /web /web

# COPY requirements.txt requirements.txt

#install dependencies
RUN apt-get update  &&\
 apt-get install -y zbar-tools &&\
 apt install -y tesseract-ocr-eng &&\
 apt update &&\
 pip3 install -r requirmentes.txt 

EXPOSE 5000
ENTRYPOINT [ "python3" ]
CMD ["run.py"]
