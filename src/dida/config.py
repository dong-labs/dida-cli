"""配置管理模块

继承 dong.config.Config，管理 dida-cli 的用户配置。
"""

from dong.config import Config


class DidaConfig(Config):
    """待咚咚配置类"""

    @classmethod
    def get_name(cls) -> str:
        return "dida"

    @classmethod
    def get_defaults(cls) -> dict:
        return {
            "default_status": "pending",
            "default_priority": 0,
            "default_limit": 20,
            "statuses": ["pending", "in_progress", "completed", "cancelled"],
        }


# 便捷函数
def get_config() -> dict:
    return DidaConfig.load()

def get_default_status() -> str:
    return DidaConfig.get("default_status", "pending")

def get_default_priority() -> int:
    return DidaConfig.get("default_priority", 0)

def get_default_limit() -> int:
    return DidaConfig.get("default_limit", 20)

def get_statuses() -> list:
    return DidaConfig.get("statuses", ["pending", "in_progress", "completed", "cancelled"])
