# Fiat Punto prediction service

Predicts the price of a Fiat Punto (Grande/Evo) on Marktplaats ads

Project structure:
* `Autos` Django configurations files
* `api` REST API endpoint (Django App)
* `extension` Chrome extension
* `models` Jupyter notebooks used for generating model
* `scraper` Marktplaats scaper (Django App)

## Demo
![Demo gif](demo.gif)

## Getting Started

### Dependencies

* Python3
* Chrome browser

### Installing
* Install extension in Chrome

```
git clone https://github.com/marcusabu/Autos.git
cd Autos
pip install -r requirements.txt
```

### Running the server
```
python manage.py runserver
```

## Used technologies
* Python (Django)
* scikit-learn
* TensorFlow 2.0
* Javascript
* Heroku
* SQL


## Author
 
[Marcus Abukari (LinkedIn)](https://www.linkedin.com/in/marcus-abukari-3298788a/)
