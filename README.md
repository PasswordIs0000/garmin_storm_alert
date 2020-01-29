# Garmin Storm Alert

The Garmin Instinct watch provides a storm alert feature that alerts you if the air pressure decreases by a configured delta within 3 hours. I was wondering witch delta for the pressure change to use in my region. This project downloads historical weather data and then tries to predict an increase in wind speed given the decrease in air pressure. It prints a table of false-positive and false-negative rates for different pressure deltas and wind deltas.

Uses the historical weather data from https://meteostat.net/

Please change the station ID to your nearest station if you want to evaluate the storm alert feature.
