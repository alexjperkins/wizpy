from typing import Dict


def build_wizard_api_definition(func) -> Dict:
    return {
        "help": f"\n\t{func.__doc__ or ''}\n",
        "name": f"{func.__name__.replace('_', ' ').title()}\n",
        "service": func,
    }
