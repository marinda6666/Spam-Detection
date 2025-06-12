import pandas as pd
from zenml import step
import logging


class ObtainData:
    """
    Obtaining the data from the data_path
    """

    def __init__(self, data_path: str):
        """
        Args:
            data_path: path to data
        """
        self.data_path = data_path

    def get_data(self):
        """
        Obtaining the data from the data_path
        """
        logging.info(f"Obtaining data from {self.data_path}")
        return pd.read_csv(self.data_path)


@step
def obtain_data(data_path: str) -> pd.DataFrame:
    """
    Obtaining the data from the data_path

    Args:
        data_path: path to the data
    Returns:
        pd.DataFrame: obtained data
    """

    try:
        data = ObtainData(data_path)
        df = data.get_data()
        return df

    except Exception as e:
        logging.error(f"Error while obtaining data: {e}")
        raise e
