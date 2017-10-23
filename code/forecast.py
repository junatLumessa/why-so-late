from analyze import get_classifier_for_all_line_ids
from get_weather import get_weather_forecast_for_current_day
from get_data import get_data_for_current_day

def get_forecast_for_current_day():
    #df, timeTableRows = get_data_for_current_day()
    wd = get_weather_forecast_for_current_day()
    #rainAndSnow = wd.groupby(['PrecipitationForm'])['Precipitation1h'].sum().reset_index()


if __name__ == "__main__":
    get_forecast_for_current_day()
