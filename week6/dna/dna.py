import csv
import sys


def main():
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    rows = []
    with open(sys.argv[1]) as file:
        reader = csv.DictReader(file)
        strs = reader.fieldnames[1:]
        for row in reader:
            rows.append(row)

    with open(sys.argv[2]) as file:
        sequence = file.read()

    counts = {}
    for s in strs:
        counts[s] = longest_match(sequence, s)

    for row in rows:
        if all(int(row[s]) == counts[s] for s in strs):
            print(row["name"])
            return

    print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Iterate through the sequence, checking for subsequence matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # Return longest run found
    return longest_run


main()
