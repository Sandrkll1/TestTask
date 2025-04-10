import pkgutil
from pathlib import Path


def get_modules_from_package(package: str) -> list[str]:
    package_path = Path(package.replace(".", "/"))
    modules = []
    for _, module_name, is_pkg in pkgutil.iter_modules([str(package_path)]):
        full_module_name = f"{package}.{module_name}"
        modules.append(full_module_name)
        if is_pkg:
            modules.extend(get_modules_from_package(full_module_name))
    return modules
