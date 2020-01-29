# Garmin Storm Alert

The Garmin Instinct watch provides a storm alert feature that alerts you if the air pressure decreases by a configured delta within 3 hours. I was wondering witch delta for the pressure change to use in my region. This project downloads historical weather data and then tries to predict an increase in wind speed given the decrease in air pressure. It prints a table of false-positive and false-negative rates for different pressure deltas and wind deltas.

Uses the historical weather data from Meteostat: https://meteostat.net/

Meteostat weather data is based on the listed sources: https://meteostat.net/de/sources
Namely:
- Deutscher Wetterdienst - Open Data
- Deutscher Wetterdienst - Climate Data Center
- NOAA - National Weather Service
- NOAA - Global Historical Climatology Network
- Government of Canada - Open Data
- European Data Portal
- Offene Daten Österreich

Disclaimer: The author of this project does not claim any rights on the used historical weather data!
