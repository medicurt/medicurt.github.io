from enum import Enum
#This file contains enumerations. Using enumerations has the advantage that the expected possible values will be visible in 
#swagger UI for front-end devs and for back-end testing. It also means that only pre-approved string data can be passed.

class Permissions(str, Enum):
    DENY = "DENY"
    READ_ONLY = "R"
    READ_WRITE = "RW"
    FULL = "FULL"
