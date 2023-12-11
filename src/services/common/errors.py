class UserAlreadyExistsError(Exception):
    """ユーザーがすでに存在する場合のエラー"""
    pass


class UserNotFoundError(Exception):
    """ユーザーが存在しない場合のエラー"""
    pass


class PasswordNotMatchError(Exception):
    """ユーザーのパスワードが一致しない場合のエラー"""
    pass
