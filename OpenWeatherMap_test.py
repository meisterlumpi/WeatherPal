from pyowm import OWM

API_key = '<enter api key here>'

location_str = 'Hallbergmoos, DE'



owm = OWM(API_key, language='de')

if owm.is_API_online():

    obs = owm.weather_at_place(location_str)
    w = obs.get_weather()

    print(w.get_reference_time())  # get time of observation in GMT UNIXtime
    print(w.get_reference_time(timeformat='iso'))             # ...or in ISO8601
    print(w.get_clouds())                                     # Get cloud coverage
    print(w.get_rain())                                       # Get rain volume
    print(w.get_snow())                                       # Get snow volume
    print(w.get_wind())                                       # Get wind degree and speed
    print(w.get_humidity())                                   # Get humidity percentage
    print(w.get_pressure())                                   # Get atmospheric pressure
    print(w.get_temperature())                                # Get temperature in Kelvin
    print(w.get_temperature(unit='celsius'))                  # ... or in Celsius degs
    print(w.get_temperature('fahrenheit'))                    # ... or in Fahrenheit degs
    print(w.get_status())                                     # Get weather short status
    print(w.get_detailed_status())                           # Get detailed weather status
    print(w.get_weather_code())                               # Get OWM weather condition code
    print(w.get_weather_icon_name())                          # Get weather-related icon name
    print(w.get_sunrise_time())                               # Sunrise time (GMT UNIXtime or ISO 8601)
    print(w.get_sunset_time('iso'))                           # Sunset time (GMT UNIXtime or ISO 8601)

    print('\n')

    fc = owm.three_hours_forecast(location_str)
    f = fc.get_forecast()
    print(f.get_reception_time())                           # UNIX GMT time
    print(f.get_reception_time('iso'))                      # ISO8601
    print(f.get_interval())
    print(len(f))
    print(f.get_location())

    lst = f.get_weathers()
    for weather in f:
        print (weather.get_reference_time('iso'),weather.get_status())

    print('\n')

    print(fc.will_have_rain())
    print(fc.will_have_sun())
    print(fc.will_have_fog())
    print(fc.will_have_clouds())
    print(fc.will_have_snow())

else:
    print('Service is offline')
