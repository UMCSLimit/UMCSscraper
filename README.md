# UMCSscraper

# routings:

## weather:
* /weather - returns most up to date weather
* /weather_hourly - returns weather for: 3h 6h 9h ahead and 1,2,3,4 days ahead.

`Icons format:0 - bezchmurnie (clear sky) 
1 - zarezerwowane dla innych,
2 - burza (thunderstorm),
3 - mżawka (drizzle),
5 - deszcz (rain),
6 - śnieg (snow),
7 - fog/smoke/haze,
8 - zachmurzone niebo (Clouds)`

## UMCS related:
* /instagram - gets posts from instagram (links) + description + number of likes
* /events - gets current events from UMCS main website
## Moria related:
* /aula105 - returns 2 upcoming classes in 105 inf Aula Duża
## ZTM related:
* /ztm - returns metadata (?)
* /ztm/getBuses - returns all busses
* /ztm/<int> - returns bus details about sepcified ID
  
