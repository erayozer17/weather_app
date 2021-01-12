# Weather App with OpenWeatherMap

## Prerequisites

    - docker
    - docker-compose
    - make

## Running the app
Download code via ```git clone https://github.com/erayozer17/weather_app.git```<br>
Go in the root directory and run ```make run```. This will compile the translation files and run docker containers.<br>
Application will be ready at ```127.0.0.1:8000```


## Stoping the app
For stopping the application, run ```make stop```


## Testing the app
For running the tests and flake8, run ```make test```