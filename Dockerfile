FROM python:3.8

WORKDIR /app
ADD requirements.txt /app

RUN apt-get update -y
RUN apt-get install -y xorg-dev
RUN apt-get install -y libnss3
RUN apt-get install -y libgl1-mesa-dri
RUN apt-get install -y libgl1-mesa-glx
RUN apt-get install -y libnss3
RUN apt-get install -y libfontconfig1
RUN apt-get install -y libxcomposite1
RUN apt-get install -y libxcursor1
RUN apt-get install -y libxi6
RUN apt-get install -y libxtst6
RUN apt-get install -y libasound2
RUN apt-get install -y libxkbcommon-x11-0
RUN apt-get install -y libgl1-mesa-glx
RUN apt-get install -y libdbus-1-3
RUN apt-get install -y build-essential
RUN apt-get install -y libgl1-mesa-dev
RUN apt-get install -y qt5-default

RUN pip3 install -r requirements.txt
ADD . /app

RUN adduser --disabled-password --gecos '' admin
USER admin

CMD python3 bot.py 