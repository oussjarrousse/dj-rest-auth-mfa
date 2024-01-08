import logging

logger = logging.getLogger(__name__)


def __get_class__(class_path):
    import importlib

    # Check if the class path is in the expected format (module.ClassName)
    if not "." in class_path:
        raise Exception("class Name should include modulename.classname")

    # Split the class path and separate the module and class names
    parsed_str = class_path.rsplit(
        ".", 1
    )  # rsplit is more appropriate for this use case
    module_name, class_name = parsed_str[0], parsed_str[1]

    # Attempt to import the module
    try:
        imported_module = importlib.import_module(module_name)
    except ImportError as e:
        raise ImportError(f"Could not import module {module_name}") from e

    # Attempt to retrieve the class from the imported module
    try:
        callable_class = getattr(imported_module, class_name)
    except AttributeError as e:
        raise AttributeError(
            f"Module '{module_name}' does not have a class named '{class_name}'"
        ) from e

    # Check if what we got is indeed a class
    if not isinstance(callable_class, type):
        raise TypeError(
            f"Expected a class at '{class_path}', found {type(callable_class)} instead"
        )

    return callable_class
