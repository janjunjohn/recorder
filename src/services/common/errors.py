# User
class UserAlreadyExistsError(Exception):
    """ユーザーがすでに存在する場合のエラー"""
    pass


class UserNotFoundError(Exception):
    """ユーザーが存在しない場合のエラー"""
    pass


class PasswordNotMatchError(Exception):
    """ユーザーのパスワードが一致しない場合のエラー"""
    pass


# Task
class TaskAlreadyExistsError(Exception):
    """タスクがすでに存在している場合のエラー"""
    

class TaskNotFoundError(Exception):
    """タスクが存在しない場合のエラー"""
    pass


# common
class InvalidUUIDError(Exception):
    """UUIDが不正な場合のエラー"""
    pass
