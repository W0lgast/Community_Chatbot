"""
Contains a class that will contain all the knowledge known by the agent, and functions for interacting with the
data.

Kipp Freud
28/10/2019
"""

# ------------------------------------------------------------------

from data.data_reader import CCSV
from knowledge.knowledge_unit import CKnowledgeUnit
from util.message import message
import util.utilities as ut

# ------------------------------------------------------------------

TITLE_TAG = "Title"
CONTENT_TAG = "Content"

# ------------------------------------------------------------------


class CKnowledgeBase(object):
    """
    This contains all the knowledge.
    """
    def __init__(self, path_to_data):
        """
        This should be given the path to the dataset, it should parse it and store it.

        :param path_to_data: the file location of the data.
        """
        if not isinstance(path_to_data, str):
            message.logError("Given path to data is not a string instance.",
                             "CKnowledgeBase::__init__")
            ut.exit(0)

        self._knowledge = self._loadData(path_to_data)

    # ------------------------------------------------------------------
    # 'public' members
    # ------------------------------------------------------------------

    def getKnowledgeUnits(self):
        """
        :return: The :list: of :class:`CKnowledgeUnit` instances.
        """
        return self._knowledge

    # ------------------------------------------------------------------
    # 'private' members
    # ------------------------------------------------------------------

    def _loadData(self, path_to_data):
        """
        Will create :class:`CKnowledgeUnit` instances that represent knowledge contained in the data csv located
        at :param:`path_to_data`.

        :param path_to_data: The file location of the data.
        """
        csv = CCSV(path_to_data)
        row_dicts = csv.getRows()
        return self._makeKnowledgeUnits(row_dicts)

    def _makeKnowledgeUnits(self, row_dicts):
        """
        Takes a list of dictionary representations of rows, and creates :class:`CKnowledgeUnit` instances for
        each dctionary.

        :param row_dicts: A list of dictionaries encoding knowledge.
        :return: A list of :class:`CKnowledgeUnit` instances representing that data.
        """
        ans = []
        for item in row_dicts:
            keys = item.keys()
            if TITLE_TAG in keys and CONTENT_TAG in keys:
                ans.append(CKnowledgeUnit(item[TITLE_TAG], item[CONTENT_TAG]))
        return ans
