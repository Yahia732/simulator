import numpy as np


class missing_values:
    def __init__(self,percentage_missing=0.05):
        """
        Parameters:

            percentage_missing (Float): percentage of missing value.

        """
        self.percentage_missing=percentage_missing


    def add_missing_values(self,data):
        """
        Add missing values to the time series data within a specified date range.



        Returns:
            numpy.ndarray: The time series data with missing values.
        """
        num_missing = int(len(data) * self.percentage_missing)
        missing_indices = np.random.choice(len(data), size=num_missing, replace=False)

        data_with_missing = data.copy()
        data_with_missing[missing_indices] = np.nan

        return data_with_missing