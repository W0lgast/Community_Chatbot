'''
Contains a class for reading CSV files.

Kipp Freud
30/10/2019
'''

# ------------------------------------------------------------------

import pandas as pd
from numpy import isnan

from util.message import message
import util.utilities as ut

# ------------------------------------------------------------------

class CCSV(object):
    """
    A class for representing a CSV file.
    """

    def __init__(self, file_path):
        """
        :param file_path: A path to a CSV file.
        """
        if not isinstance(file_path, str):
            message.logError("Given path to data is not a string instance.",
                             "CKnowledgeBase::__init__")
            ut.exit(0)

        # ..todo: make a check that checks there's a CSV at the specified file location.

        self._data = pd.DataFrame( pd.read_csv(file_path) )

    # ------------------------------------------------------------------
    # 'public' members
    # ------------------------------------------------------------------

    def getRows(self):
        """
        Gets rows in CSV file encoded by :param:`_data` and returns them as a list of dictionaries.

        :return: A list of dictionaries containing the column names as keys, and column content as values.
        """
        ret = []
        column_names = list(self._data.columns)
        for ind, row in self._data.iterrows():
            r_d = { }
            for c_n in column_names:
                if isinstance(row[c_n], str) or not isnan(row[c_n]):
                    r_d[c_n] = row[c_n]
            ret.append(r_d)
        return ret
