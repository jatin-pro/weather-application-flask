import string
import requests
from flask import Flask, render_template, request , redirect , url_for 

from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisisasecret'
db = SQLAlchemy(app)

class City(db.Model): 
      id = db.Column(db.Integer , primary_key=True)
      name = db.Column(db.String(50),nullable=False)

def weather_api(city): 
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=d7cdcf0f917a0cbc7ba86b22cf1f04e6"
    r = requests.get(url).json()
    return r



@app.route('/')
def weather_app(): 
      cities = City.query.all()
      weather_data = []
      for city in cities: 
            r = weather_api(city.name)
            weather = { 
              'city': city.name, 
              'temperature' : r['main']['temp'],
              'description' :  r['weather'][0]['description'],
               'icon' : r['weather'][0]['icon'],

            }
            weather_data.append(weather)
      return render_template('weather.html', weather_data=weather_data)
    



@app.route('/',methods=['POST'])
def method_name():
   err_message = ''
   new_city = request.form.get('city')
   new_city = new_city.lower()
   new_city = string.capwords(new_city)
   if new_city:
         existing_city = City.query.filter_by(name=new_city).first()
         if not existing_city:
               city_data = weather_api(new_city)
               if city_data['cod']==200:
                     new_city_obj = City(name=new_city)
                     db.session.add(new_city_obj)
                     db.session.commit()
              
   return redirect(url_for('weather_app'))

@app.route('/delete/<name>')
def delete_city( name ):
    city = City.query.filter_by(name=name).first()
    db.session.delete(city)
    db.session.commit()
    
    return redirect(url_for('weather_app'))

if __name__ == '__main__':
 app.run(debug=True)
   

