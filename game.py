from email.errors import MisplacedEnvelopeHeaderDefect
from enum import Enum
import random
import time

class LetterState(Enum):
    UNKNOWN = 0
    MISPOSITIONED = 1
    CORRECT = 2

