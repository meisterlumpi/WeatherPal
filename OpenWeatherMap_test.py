from pyowm import OWM
import unicodedata

API_key = '<enter api key here>'

location_str = 'Hallbergmoos, DE'



owm = OWM(API_key, language='de')

if owm.is_API_online():

    obs = owm.weather_at_place(location_str)
    w = obs.get_weather()

    print('reference_time())                 ', w.get_reference_time())                             # get time of observation in GMT UNIXtime
    print('reference_time(timeformat="iso")) ', w.get_reference_time(timeformat="iso"))             # ...or in ISO8601
    print('clouds())                         ', w.get_clouds())                                     # Get cloud coverage
    print('rain())                           ', w.get_rain())                                       # Get rain volume
    print('snow())                           ', w.get_snow())                                       # Get snow volume
    print('wind())                           ', w.get_wind())                                       # Get wind degree and speed
    print('humidity())                       ', w.get_humidity())                                   # Get humidity percentage
    print('pressure())                       ', w.get_pressure())                                   # Get atmospheric pressure
    print('temperature())                    ', w.get_temperature())                                # Get temperature in Kelvin
    print('temperature(unit="celsius"))      ', w.get_temperature(unit="celsius"))                  # ... or in Celsius degs
    print('temperature("fahrenheit"))        ', w.get_temperature("fahrenheit"))                    # ... or in Fahrenheit degs
    print('status())                         ', w.get_status())                                     # Get weather short status
    print('detailed_status())                ', w.get_detailed_status())                            # Get detailed weather status
    print('weather_code())                   ', w.get_weather_code())                               # Get OWM weather condition code
    print('weather_icon_name())              ', w.get_weather_icon_name())                          # Get weather-related icon name


    base_url = 'http://openweathermap.org/img/w/'  # 10d.png
    img_file_name = unicodedata.normalize('NFKD', w.get_weather_icon_name()).encode('ascii', 'ignore')
    img_file_url = base_url + img_file_name + '.png'

    print('weather icon url: ', img_file_url)

    print('sunrise_time())                   ', w.get_sunrise_time())                               # Sunrise time (GMT UNIXtime or ISO 8601)
    print('sunset_time("iso"))               ', w.get_sunset_time("iso"))                           # Sunset time (GMT UNIXtime or ISO 8601)

    print('\n')

    fc = owm.three_hours_forecast(location_str)
    f = fc.get_forecast()
    print('forecast:')
    print('reception_time())      ', f.get_reception_time())                           # UNIX GMT time
    print('reception_time("iso")) ', f.get_reception_time("iso"))                      # ISO8601
    print('interval())            ', f.get_interval())
    print(len(f))
    print('location()             ', f.get_location())

    lst = f.get_weathers()
    for weather in f:
        print (weather.get_reference_time("iso"), weather.get_status())

    print('\n')

    print('will_have_rain()   ', fc.will_have_rain())
    print('will_have_sun()    ', fc.will_have_sun())
    print('will_have_fog()    ', fc.will_have_fog())
    print('will_have_clouds() ', fc.will_have_clouds())
    print('will_have_snow()   ', fc.will_have_snow())

else:
    print('Service is offline')
