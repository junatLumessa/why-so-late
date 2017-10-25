# Application for predicting train delays

## Table of Contents
1. [Data overview](#data-overview)
    1. [Weather data](#weather-data)
    1. [Railway data](#railway-data)
1. [Predictions](#predictions)
1. [Conclusions](#conclusions)

## Data overview

In this section we will give a brief overlook on the data to be analyzed. All the data has been collected from the past year (October 2016 - October 2017).

### Weather data

![Pic 1: Amount of snowfall in the past year.](snow.png "Snow amount")

![Pic 2: Amount of rainfall in the past year.](rrday.png "Rain amount")

![Pic 4:  Temperature and delay percentage during last year](bar-plot-all-trains.png "Air temperature and delays")

![Pic 5:  Temperature, snow and delay percentage during last year](bar-plot-snow.png "Air temperature, snow and delays")

![Pic 6:  Temperature, rain and delay percentage during last year](bar-plot-rain.png "Air temperature, rain and delays")


### Railway data

#### Most common causes for delays

| Delay cause                      | Count | Delay (min)           |
|:---------------------------------|------:|----------------------:|
| Liikenteenhoito                  | 13728 | 6.9                   |
| Matkustajapalvelu                | 11715 | 4.2                   |
| Ratatyö                          | 7253  | 4.9                   |
| Liikenteenhoitojärjestelmät      | 4697  | 9.3                   |
| Muut syyt                        | 2095  | 7.7                   |
| Sähkörata                        | 1700  | 9.8                   |
| Kalusto, moottorijunat ja vaunut | 971   | 10.4                  |
| Rata (ratarakenne)               | 797   | 5.6                   |
| Henkilökunta                     | 656   | 7.6                   |
| Onnettomuus                      | 204   | 23.6                  |
| Aikataulu ja liikennöinti        | 173   | 25.7                  |
| Junanmuodostus                   | 149   | 14.0                  |
| Vetokalusto                      | 45    | 11.2                  |

[More information](https://github.com/finnishtransportagency/metadata/blob/master/csv/delay_codes.csv) about delay causes from finnish tranpost agency 

### Top 10 stations with delays (over 3min)

| Station                          | Count |
|:---------------------------------|------:|
| Päärautatieasema                 | 12404 |
| Pasilan asema                    | 30529 |
| Oulunkylä                        | 11749 | 
| Malmi                            | 11280 | 
| Tikkurila                        | 18087 | 
| Kerava                           | 10374 | 
| Huopalahti                       | 10374 | 
| Puistola                         | 11180 | 
| Hiekkaharju                      | 10342 | 
| Käpylä                           | 10164 | 


![Pic 7:  Average delays of commuter trains](averageDelays.png "Average delays of commuter trains")

![Pic 8:  Percentages of delayed departures of commuter trains](delayedDepartures.png "Percentages of delayed departures of commuter trains")

Pictures 7 and 8 contains 'V' and 'v' trains from the train history data but they aren't apparently real commuter train lines. [Official commuter train lines listed here](https://aikataulut.reittiopas.fi/linjat/fi/train.html)

## Predictions

We tried many different kinds of models for the data.

### Logistic regression
Data was not linear and we couldn't make any linear regression analysis.

### Gaussian process classifier (with 1 kernel, default) 
### Random forest classifier (200 trees)
### Dummy classifier

## Conclusions

*ToDo*
