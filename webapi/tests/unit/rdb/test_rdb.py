import pytest
from src.infrastructure.core.rdb.RdbSessionClient import RdbSessionClient
from src.infrastructure.core.rdb.AsyncRdbSessionClient import AsyncRdbSessionClient

def test_session_init(session):
    rdb = RdbSessionClient(session)
    assert rdb.session == session
    
    
def test_session_commit(session):
    rdb = RdbSessionClient(session)
    rdb.commit()
        
    
def test_session_rollback(session):
    rdb = RdbSessionClient(session)
    rdb.rollback()
    
    
def test_session_close(session):
    rdb = RdbSessionClient(session)
    rdb.close()


# @pytest.mark.asyncio
# async def test_async_session_init(async_session):
#     rdb = AsyncRdbSessionClient(async_session)
#     assert rdb.session == async_session
    
# @pytest.mark.asyncio
# async def test_async_session_commit(async_session):
#     rdb = AsyncRdbSessionClient(async_session)
#     await rdb.commit()
        
# @pytest.mark.asyncio 
# async def test_async_session_rollback(async_session):
#     rdb = AsyncRdbSessionClient(async_session)
#     await rdb.rollback()
    
# @pytest.mark.asyncio
# async def test_async_session_close(async_session):
#     rdb = AsyncRdbSessionClient(async_session)
#     await rdb.close()



