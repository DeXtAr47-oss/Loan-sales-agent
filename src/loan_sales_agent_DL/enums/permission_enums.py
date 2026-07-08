from enum import Enum

class PermissionEnums(str, Enum):
    VIEW = "VIEW"
    EDIT = "EDIT"
    CREATE = "CREATE"
    DELETE = "DELETE"
    APPROVE = "APPROVE"