import numpy as np
import pandas as pd

from Seasonality.seasonality import seasonality


class Weekly_Seasonality(seasonality):
    def add_weekly_seasonality(self,data):
        """
        Add weekly seasonality component to the time series data.

        Parameters:
            data (DatetimeIndex): The time index for the data.


        Returns:
            numpy.ndarray: The seasonal component of the time series.
        """

        seasonal_component = np.sin(2 * np.pi * data.dayofweek / 7)
        seasonal_component += 1

        return pd.Series(seasonal_component)
