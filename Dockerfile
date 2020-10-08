FROM python:3.8.6
ADD . /deploy
WORKDIR /deploy
RUN pip install -r requirements.txt

EXPOSE 8080
ENTRYPOINT ["./entrypoint.sh"]
