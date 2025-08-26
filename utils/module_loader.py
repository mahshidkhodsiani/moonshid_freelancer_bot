import importlib
import pkgutil
from typing import List

from aiogram import Router


def load_modules(package_name: str = "modules") -> List[Router]:
    """
    Dynamically loads all modules from the specified package and returns their routers.

    Args:
        package_name: The name of the package to load modules from

    Returns:
        List of router instances from the modules
    """
    package = importlib.import_module(package_name)
    routers = []
    for _, module_name, is_pkg in pkgutil.iter_modules(
        package.__path__, package.__name__ + "."
    ):
        if is_pkg:
            continue
        module = importlib.import_module(module_name)
        if hasattr(module, "router"):
            routers.append(module.router)

    return routers
