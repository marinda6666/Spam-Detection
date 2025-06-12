import pandas as pd
import logging
from zenml import step
import re
from nltk import SnowballStemmer
from nltk.corpus import stopwords


STOPWORDS = set(stopwords.words("english"))


class CleanData:
    """
    Clean DataFrme
    """

    def __init__(self, df: pd.DataFrame):
        """
        Args:
            df: dataset DataFrame
        """
        self.df = df

    def preprocess_text(self, text: str) -> str:
        """
        Clean single text

        Args:
            text: string to clean
        """
        stemmer = SnowballStemmer("english")
        clean_text = re.sub(r"[^\w\s]", "", text)
        clean_text = " ".join(
            [stemmer.stem(x) for x in clean_text.lower().split() if x not in STOPWORDS]
        )
        return clean_text

    def preprocess_data(self):
        """
        Clean whole DataFrame
        """
        for index, row in self.df.iterrows():
            self.df.at[row.Index, "mail"] = self.preprocess_text(row["mail"])

    def get_prerpocessed_data(self):
        """
        return preprocessed data
        """

        self.preprocess_data()
        return self.df


@step
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean DataFrme

    Args:
        df: dataset DataFrame
    """

    try:
        data = CleanData(df)
        return data.get_prerpocessed_data()
    except Exception as e:
        logging.error("Error with cleaning DataFrame: {e}")
        raise e
