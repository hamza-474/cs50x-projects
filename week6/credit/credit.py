from cs50 import get_int


def main():
    card = str(get_int("Number: "))
    if not is_valid(card):
        print("INVALID")
        return
    if len(card) == 15 and card[:2] in ["34", "37"]:
        print("AMEX")
    elif len(card) == 16 and 51 <= int(card[:2]) <= 55:
        print("MASTERCARD")
    elif len(card) in [13, 16] and card[0] == "4":
        print("VISA")
    else:
        print("INVALID")


def is_valid(card):
    total = 0
    for i, digit in enumerate(reversed(card)):
        n = int(digit)
        if i % 2 == 1:
            n *= 2
            total += n // 10 + n % 10
        else:
            total += n
    return total % 10 == 0


main()
