### Exercise 1
* Consider a service for concurrently sharing a set of printers from a pool for several users (all printers are equal). Define an appropriate interface (for instance using Python-like oder C-like pseudocode) for such a service so that the openness requirements are satistified
* Assume that the channel is secure.


you should define functions as atomic as possbile and return codes for errors.
define apis that are as general as possible, but not more general than necessary.

1. Function print
```
print_codes = {0:"OK",
    1:"AUTH_FAILED",
    2:"PRINTER_NOT_AVAILABLE",
    3:"DOC_NOT_VALID",
    4:"INVALID SETTINGS",
    5:"PRINTER_ERROR",
    6:"GENERAL_ERROR"
    }
```

```

#Pseudocode
# Token is a unique identifier for a printer session

def authenticate(user_id:int,PW:str) -> int: #token -1 if failed 
    return True

    def logout(token:int,user_id: int) -> int #codes 0 if ok, 1 if failed, 2 if not existing:
        return True


def print (file:Document, printer:int,token:int,settings:Settings(object)) -> int:
    def get_printing_progress(Doc:Document,printer_id:int) -> int:
        return 0

    def get_printer_status(printer_id:int,token:int) -> int #0 if ok, 1 if failed, 2 if not existing:
        return 0
    
    def get_all_printers(token:int) -> list:
        return []

    def get_printer_queue(pritner_id:int,token:int) -> list:
        return []

    def get_shortertest_queue(token:int):
        return 0

```