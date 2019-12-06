my_input = (236491, 713787)

possible_passwords = 0

for n in range(my_input[0], my_input[1]+1):
    # all of these numbers will be in my input range.
    # all numbers in the range are 6 digits.
    has_double = False
    previous_digit = None
    only_increasing = True
    while n > 0 and only_increasing:
        n, digit = divmod(n, 10)
        has_double = has_double or (digit == previous_digit)
        if previous_digit is not None and digit > previous_digit:
            only_increasing = False
            break
        previous_digit = digit
    if has_double and only_increasing:
        possible_passwords += 1

print(f'Possible passwords in range: {possible_passwords}')

    


