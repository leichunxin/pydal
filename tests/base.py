from ._compat import unittest
from ._adapt import DEFAULT_URI, drop
from pydal import DAL, Field

class TestReferenceNOTNULL(unittest.TestCase):
#1:N not null

    def testRun(self):
        db = DAL(DEFAULT_URI, check_reserved=['all'])
        db.define_table('tt', Field('vv'))
        db.define_table('ttt', Field('vv'), Field('tt_id', 'reference tt', notnull=True))
        self.assertRaises(Exception, db.ttt.insert, vv='pydal')
        # The following is mandatory for backends as PG to close the aborted transaction
        db.commit()
        drop(db.ttt)
        drop(db.tt)
        db.close()
        
class TestReferenceUNIQUE(unittest.TestCase):
# 1:1 relation

    def testRun(self):
        db = DAL(DEFAULT_URI, check_reserved=['all'])
        db.define_table('tt', Field('vv'))
        db.define_table('ttt', Field('vv'), Field('tt_id', 'reference tt', unique=True))
        id_i = db.tt.insert(vv='pydal')
        # Null tt_id
        db.ttt.insert(vv='pydal')
        # first insert is OK
        db.ttt.insert(tt_id=id_i)
        self.assertRaises(Exception, db.ttt.insert, tt_id=id_i)
        # The following is mandatory for backends as PG to close the aborted transaction
        db.commit()
        drop(db.ttt)
        drop(db.tt)
        db.close()
        
class TestReferenceUNIQUENotNull(unittest.TestCase):
# 1:1 relation not null

    def testRun(self):
        db = DAL(DEFAULT_URI, check_reserved=['all'])
        db.define_table('tt', Field('vv'))
        db.define_table('ttt', Field('vv'), Field('tt_id', 'reference tt', unique=True, notnull=True))
        self.assertRaises(Exception, db.ttt.insert, vv='pydal')
        db.commit()
        id_i = db.tt.insert(vv='pydal')
        # first insert is OK
        db.ttt.insert(tt_id=id_i)
        self.assertRaises(Exception, db.ttt.insert, tt_id=id_i)
        # The following is mandatory for backends as PG to close the aborted transaction
        db.commit()
        drop(db.ttt)
        drop(db.tt)
        db.close()
