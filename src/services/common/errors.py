class UserAlreadyExistsError(Exception):
    """ユーザーがすでに存在する場合のエラー"""
    pass

class UserNotFoundError(Exception):
    """ユーザーが存在しない場合のエラー"""
    pass