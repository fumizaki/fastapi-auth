
class RdbContraintError(Exception):
    """
    制約をデータベースが満たしていないときに発生するエラー
    """
    pass


class RdbRecordNotFoundError(Exception):
    pass