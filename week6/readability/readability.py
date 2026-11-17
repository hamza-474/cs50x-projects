from cs50 import get_string
from math import floor


def main():
    text = get_string("Text: ")
    letters = sum(1 for c in text if c.isalpha())
    words = len(text.split())
    sentences = sum(1 for c in text if c in ".!?")
    l = letters / words * 100
    s = sentences / words * 100
    index = floor(0.0588 * l - 0.296 * s - 15.8 + 0.5)
    if index >= 16:
        print("Grade 16+")
    elif index < 1:
        print("Before Grade 1")
    else:
        print(f"Grade {index}")


main()
