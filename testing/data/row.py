''' Unit tests for the db_para_retriever '''
# pylint: disable=missing-function-docstring


class Row():
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
