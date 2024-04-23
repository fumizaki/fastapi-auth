from src.infrastructure.core.rdb.RdbSessionClient import RdbSessionClient


def test_init(session):
    rdb = RdbSessionClient(session)
    assert rdb.session == session
    
    
def test_commit(session):
    rdb = RdbSessionClient(session)
    rdb.commit()
        
    
def test_rollback(session):
    rdb = RdbSessionClient(session)
    rdb.rollback()
    
    
def test_close(session):
    rdb = RdbSessionClient(session)
    rdb.close()
