from enum import Enum


class JwtType(Enum):
    """
    jwt token 类型
    """

    ADMIN = 1
    USER = 2
