my_input = (236491, 713787)

possible_passwords = 0

for n in range(my_input[0], my_input[1]+1):
    # all of these numbers will be in my input range.
    # all numbers in the range are 6 digits.
    doubles = set()  # Collect any digit that appears in a double
    triples = set()  # Collect any digit that appears in a triple
    previous_digit = None
    uberprevious_digit = None
    only_increasing = True
    while n > 0 and only_increasing:
        n, digit = divmod(n, 10)
        if (digit == previous_digit):
            doubles.add(digit)
        if (digit == previous_digit == uberprevious_digit):
            triples.add(digit)
        if previous_digit is not None and digit > previous_digit:
            only_increasing = False
            break
        uberprevious_digit = previous_digit
        previous_digit = digit
    if only_increasing and (doubles - triples):
        # only_increasing and there were doubles that were not in triples
        possible_passwords += 1

print(f'Possible passwords in range: {possible_passwords}')

    


