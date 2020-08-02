FROM heroku/heroku:18
FROM python:3.8

ADD . . 
WORKDIR .

RUN apt-get update -y
RUN apt-get install -y xorg-dev
#RUN apt-get install libgl1-mesa-dri libgl1-mesa-glx libnss3 libfontconfig1 libxcomposite1 libxcursor1 libxi6 libxtst6 libasound2

RUN pip3 install -r requirements.txt

#CMD python3 bot.py