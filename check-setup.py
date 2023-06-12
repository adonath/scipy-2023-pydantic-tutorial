import importlib
import warnings
from pathlib import Path

MODULE_IMPORT_NAMES = {
    "PyYAML": "yaml",
}


message_success = (
    "******************************************************************\n"
    "* Congratulations! You are ready to begin the Pydantic tutorial! *\n"
    "******************************************************************\n"
)

message_failure = (
    "*********************************************************************\n"
    "* Please install missing dependencies before starting the tutorial! *\n"
    "*********************************************************************\n"
)


def get_info_dependencies():
    """Get dependency infos."""
    info = {}

    with Path("requirements.txt").open() as fh:
        dependencies = [line.strip() for line in fh.readlines()]

    for name in dependencies:
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                import_name = MODULE_IMPORT_NAMES.get(name, name)
                module = importlib.import_module(import_name)

            module_version = getattr(module, "__version__", "no version info found")
        except ImportError:
            module_version = "not installed"
        info[name] = module_version

    return info


def print_info(info, title):
    """Print info."""
    info_all = f"\n{title}:\n\n"

    for key, value in info.items():
        info_all += f"\t{key:22s} : {value:<10s} \n"

    print(info_all + "\n")


if __name__ == "__main__":
    info = get_info_dependencies()
    print_info(info, title="Tutorial Dependencies")

    if "not installed" in info.values():
        print(message_failure)
    else:
        print(message_success)
