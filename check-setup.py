import argparse
import importlib
import warnings
from pathlib import Path

MODULE_IMPORT_NAMES = {
    "PyYAML": "yaml",
    "mypy": "mypy.version",
}

IGNORE_MODULES = {"pre-commit"}


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
        dependencies = [line.strip().split("=")[0] for line in fh.readlines()]

    for name in dependencies:
        if name in IGNORE_MODULES:
            continue
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
    parser = argparse.ArgumentParser(
        prog="Pydantic Tutorial Setup Check",
        description="Check if all dependencies are installed.",
    )

    parser.add_argument(
        "-s", "--strict", action="store_true", help="Fail for missing imports."
    )
    args = parser.parse_args()

    info = get_info_dependencies()
    print_info(info, title="Tutorial Dependencies")

    if "not installed" in info.values():
        if args.strict:
            raise ImportError("Missing dependencies.")

        print(message_failure)
    else:
        print(message_success)
