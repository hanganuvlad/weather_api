# weather_api

This API was created to take weather info about a specified city for 3 days in advance, using www.weatherapi.com.

This is going to store in a database values as: date, city, max temperature, min temperature, total
precipitation, humidity. sunrise hour and sunset hour using SQLite and Flask libraries.

If a combination of date and city already exists in the database, the code will replace the old information with the new one.
