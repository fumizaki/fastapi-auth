from sqlalchemy.orm import Session

class RdbSessionClient:
    def __init__(self, session: Session) -> None:
        self.session = session
        
    def commit(self) -> None:
        self.session.commit()
        
    def rollback(self) -> None:
        self.session.rollback()
        
    def close(self) -> None:
        self.session.close()