def build_wizard_api_definition(func):
    return {
        "help": f"{func.__doc__}",
        "name": f"{func.__name__.replace('_', ' ').title()}\n",
        "service": func,
    }
