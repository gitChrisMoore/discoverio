from pymongo import MongoClient


class DBClient(object):
    """ This provides a wrapper around the MongoClient package, and also
        allows for some default values to be added.
        test = DBClient('172.21.66.37', 'amwayio').main()
        print test.discovery_todo.find().count()
    """

    def __init__(self, ip, db, port=27017, msd=3):
        self.ip = ip
        self.port = port
        self.msd = msd
        self.db_name = db
        self.db = None

    def _define_client(self):
        try:
            self.client = MongoClient(self.ip, self.port,
                                      serverSelectionTimeoutMS=self.msd)
        except Exception as e:
            return 'could not define the mongo client ' + str(e)

    def _start_client(self):
        try:
            self.db = self.client[self.db_name]
        except Exception as e:
            return 'could not connect to the database ' + str(e)

    def main(self):
        self._define_client()
        self._start_client()
        return self.db


class NextAvailDoc(object):
    """ test = DBClient('172.21.66.37',27017,'amwayio')
        print NextAvailDoc().main(insert_db_session)
    """
    def __init__(self):
        self.session = None
        self.col_a = ''
        self.col_b = ''
        self.unique = False
        self.doc = {}

    def main(self, session, col_a='discovery_todo', col_b='discovery_complete'):
        self.col_a = col_a
        self.col_b = col_b
        self.session = session
        self._workflow()
        return self.doc

    def _workflow(self):
        while self.unique is False:
            self.doc = self.doc_get(self.col_a)
            self.doc_del(self.col_a, self.doc)
            if not self.doc_count(self.col_b, self.doc):
                self.unique = True

    def doc_get(self,col):
        return self.session[col].find({}, {'_id': False}).limit(1)[0]

    def doc_del(self, col, doc):
        return self.session[col].remove(doc)

    def doc_count(self, col, doc):
        return self.session[col].find({"ip_address": doc['ip_address']}).count()




if __name__ == '__main__':
    """ IP Address Validation
    """

