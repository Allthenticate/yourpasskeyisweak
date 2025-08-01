from termcolor import colored


def print_info(text: str):
    print(colored("* " + text, "light_grey"))


def print_important(text: str):
    print(colored("** " + text, "red", attrs=["bold"]))

def print_pwned(text: str, **kwargs):
    print(colored(text, "blue", attrs=["bold"]), **kwargs)
