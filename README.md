[![Build Status](https://travis-ci.com/erayozer17/weather_app.svg?branch=master)](https://travis-ci.com/erayozer17/weather_app)

# Weather App with OpenWeatherMap

## Prerequisites

    - docker
    - docker-compose
    - make
    - OpenWeatherMap api key

## Open weather API key
Can be registered here https://home.openweathermap.org/users/sign_up

## Running the app
Download code via ```git clone https://github.com/erayozer17/weather_app.git```<br>
```cd weather_app```<br>
```echo "SECRET_KEY=sekritvalue" >> .env```<br>
```echo "OPEN_WEATHER_API_KEY=myopenweatherapikey" >> .env```<br>
```echo "CACHING_TIME=0" >> .env```<br>
Go in the root directory and run ```make run```. This will compile the translation files and run docker containers.<br>
Application will be ready at ```127.0.0.1:8000```


## Stoping the app
For stopping the application, run ```make stop```


## Testing the app
For running the tests and flake8, run ```make test```