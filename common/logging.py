import os
from colorama import Fore, Style

def logdebug(msg: str) -> None:
    if os.environ.get("DEBUG"):
        print(Fore.RED + msg)
        print(Style.RESET_ALL, end='\r')