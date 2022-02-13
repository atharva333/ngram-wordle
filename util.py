from typing import List

def read_word_file(filepath: str) -> List[str]:
    """Read list of words from file"""
    word_list = []
    with open(filepath, "r") as f:
        word_list = f.readlines()
    
    return word_list