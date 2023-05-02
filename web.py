from flask import Flask, render_template, request, redirect, url_for,json
import os, requests
from datetime import datetime
import pytz
import time 
from time import localtime, strftime

app = Flask(__name__)

@app.route('/')
def main(): 
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT,"static/data","data_json.json")
    country = json.load(open(json_url))
    return render_template('index.html', country = country)
  

@app.route('/load', methods=['POST'])
def load():
    city = request.form["city"]
    country = request.form["country"]
    unit = request.form["unit"]
    print(unit)
    selected_country = request.form["selectedOption"]
    print(selected_country)
    return redirect('/weather?city={}&country={}&unit={}'.format(city,country,unit))


@app.route('/weather', methods =['GET'])
def weather():
    city = request.args.get('city')
    country = request.args.get('country')
    unit = request.args.get('unit')
    #ountry_text = request.args.get('country_text')
    #print(country_text)
    

    if unit == 'standard': 
        unit_symbol ='K'
    elif unit == 'metric':
        unit_symbol = 'C'
    elif unit == 'imperial':
        unit_symbol = 'F'
    
    weather_url = "https://api.openweathermap.org/data/2.5/weather?q="+city+"&units="+unit+"&appid=" + "ec48f3afcee64a65c1124ce499a2eb08"
    response = requests.get(weather_url)
    weather_data = response.json()

    print(weather_data)

    print(weather_url)

    #country = weather_data['sys']['country']
    #city = weather_data['main']['name']
    lon = str(weather_data['coord']['lon'])
    lat = str(weather_data['coord']['lat'])
    temperature = round(weather_data['main']['temp'])
    humidity = weather_data['main']['humidity']
    wind_speed = weather_data['wind']['speed']
    #weather_main = weather_data['weather'].index('main')
    weather_dict = weather_data['weather']

    for weather in weather_dict: 
        weather_main = weather['main']
        weather_desc = weather['description']
        weather_icon  = weather['icon']

    print(weather_icon) 

    #temperature conversion
    if unit  == 'standard': 
        temp_conv = int(round((9/5)*(temperature-273)+32))
    elif unit == 'metric':
        temp_conv = int(round((9*temperature)/5+32))
    elif unit == 'imperial':
        temp_conv = temperature

    print(temp_conv)
    
    #clothing algorithm (draft)
    if temp_conv < 25 : 
        clothing = "winter jacket"
    elif temp_conv in range (25, 44): 
        clothing = "light to medium coat"
    elif temp_conv in range (45,66): 
        clothing = "fleece"
    elif temp_conv in range (65, 79): 
        clothing = "short sleeves"
    elif temp_conv > 80: 
        clothing = "shorts"

    
    if clothing is "fleece": 
        clothing_comment = "wear something long sleeved like a hoodie"
    elif clothing is "winter jacket": 
        clothing_comment= "It's really cold, wear your winter jacket, gloves, mufflers to keep you warm"
    elif clothing is "light to medium coat":
        clothing_comment= "layering really helps in this kind of weather"
    elif clothing is "short sleeves": 
        clothing_comment = "it's a warm day today wear whatever you wanr!"
    elif clothing_comment is "shorts": 
        clothing_comment ="it's so hot today wear something light"

    #get an hourly forecast
    forecast_url = "https://api.openweathermap.org/data/2.5/forecast?q="+city+"&units="+unit+"&appid=" + "ec48f3afcee64a65c1124ce499a2eb08"
    response_for = requests.get(forecast_url)
    forecast_data = response_for.json()

   # print(forecast_data)
    #print(forecast_url)
    print('////')
    list_weather = forecast_data['list']
    #print(list_weather)

    weather_time = []
    list_prob = []
    list_temp = []
    list_icon = []
    for time in list_weather: 
        date = time['dt']
        date_txt = time['dt_txt']
        print(date)
        print(date_txt)

        next_temp = time['main']['temp']
        list_temp.append(next_temp)

        icon_weather = weather['icon']
        list_icon.append(icon_weather)


        #convert to local time 
        local_time = localtime(date)
        #arrange time in 
        readable_time = strftime("%A %I:%M %p",local_time)

        weather_time.append(readable_time)


        #get the precpitation probability 
        prob = time['pop']
        list_prob.append(prob)
        
        prob_percip = list_prob[0]

        if prob_percip > 0: 
            prob_percip = prob_percip*100
            comment = "raining : bring an umbrella"
        
        print(weather_time)


        # for i in weather_time in range(1,3): 
        #     first_hour = weather_time[i]
        #     second_hour = weather_time[i]
        
       

        
        #local_time = pytz.utc.localize(date_txt).asimezone(pytz.timezone('America/New_York'))

        
    
    print(local_time)
    print(weather_time)

    first_hour = weather_time[0]
    second_hour = weather_time[1]
    third_hour = weather_time[2]
    first_temp = list_temp[0]
    first_icon = list_icon[0]
    
    second_temp = list_temp[1]
    second_icon = list_icon[1]
    
    third_temp = list_temp[2]
    third_icon = list_icon[2]

    print(first_hour)
    print(second_hour)
    print(third_hour)

     
    #bring umbrella or wear a raincoat
    
    #check if rain or snow exist 
    if 'rain' in weather_data: 
        rain = weather_data['rain']['1h']
        comment = "raining : bring an umbrella"
    elif 'snow' in weather_data: 
        comment = 'snowing : dress warmly'
    else: 
        comment = "enjoy the weather"
    
    #print(rain)
    
    dt = str(datetime.utcnow())
    print(dt)

    #sunglasses/hat/uv index if applicable
    uvi_url = "https://api.openuv.io/api/v1/uv?lat="+lat+"&lng="+lon+"&alt=100&dt="+dt
    # data = {
    #     "url":"https://api.openuv.io/api/v1/uv?lat="+lat+"&lng="+lon+"&alt=100&dt="+dt ,
    #     "x-acces-token": "openuv-553wwrlgzld6h8-io"

    # }

    uv_response = requests.get(uvi_url, headers ={"x-access-token" : "openuv-553wwrlgzld6h8-io"})
    uvi_data = uv_response.json()
    print(uvi_url)
    print(uvi_data)

    uv = uvi_data['result']['uv']
    print(uv)

    uv = round(uv)

    uv_status = ""

    if uv in range (0,3): 
        uv_status = "low: Apply sunscreen"
    if uv in range (3,6): 
        uv_status = "moderate: Don't forget to wear sunscreen!"
    if uv in range(6,8):
        uv_status = "high: Apply Sunscreen and Wear a Hat or Sunglasses!"
    if uv in range(8,11): 
        uv_status = "very high: Wear a protective layer and Apply Sunscreen before going out"
    if uv > 11: 
        uv_status = "extreme : Avoid the Sun"

    print(uv_status)
    

    #get today's date 
    get_date= datetime.now()
    date_today = get_date.strftime("%A,%B %d, %Y")
    time_now = get_date.strftime("%H:%M %p")
    print(date_today)

  

    #activities to do based on the weather
    
    return render_template('weatherpage.html', unit_symbol=unit_symbol, city = city, country = country, temperature=temperature, humidity=humidity, 
    wind_speed=wind_speed, weather_main=weather_main, weather_desc=weather_desc, weather_icon=weather_icon, clothing =clothing, prob_percip=prob_percip,
    comment=comment, uv=uv, date_today=date_today, time_now=time_now ,first_hour = first_hour, first_icon= first_icon, first_temp = first_temp, 
    second_hour = second_hour, second_icon = second_icon, second_temp = second_temp, third_hour=third_hour, third_icon = third_icon, third_temp=third_temp, uv_status=uv_status, 
    clothing_comment=clothing_comment )

       

if __name__ == "__main__": 
    app.run(port =8000, debug= True)


