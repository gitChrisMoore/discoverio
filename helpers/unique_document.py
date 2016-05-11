import time
import os
import sys
import db
from contextlib import contextmanager

class UniqueDocument:
    def __init__(self, col=None, col_check=None, unique_field=None):
        self.col = col
        self.col_check = col_check
        self.unique_field = unique_field
		self.db = db.DBWrapper()

    def handle(self, request):
        res = self._handle(request)
        if not res:
            self._successor.handle(request)
    def _handle(self, request):
        raise NotImplementedError('Must provide implementation in subclass.')