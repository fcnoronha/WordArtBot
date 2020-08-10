# WordArtBot

![WordArtBot logo](logo.png)

The Telegram bot that generate beautiful wordArts for you! Try it on [**@bestWordArtBot**](https://t.me/bestWordArtBot).

## How to run locally

The most simple way is to build and run the Docker container, just issue `$ docker build --tag bot . && docker run -e MODE=dev -e BOT_TOKEN=<token> bot`.

Alternatively you can install all the dependencies (check the Dockerfile for more information) and run `$ export MODE=dev && export BOT_TOKEN=<token> && python3 bot.py`.

Thanks [@arizzitano](https://github.com/arizzitano/css3wordart) for creating the reproduction of WordArt in CSS3 and [@zorbaproject](https://github.com/zorbaproject/pythonWordArt) for presenting a simple template to generate the WordArt text.
