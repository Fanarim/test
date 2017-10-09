#!/usr/bin/env python3

for num in range(100, 0, -1):
    is_five_divisible = bool(num % 5) == 0
    is_three_divisible = bool(num % 3) == 0

    if is_three_divisible and is_five_divisible:
        print('Physics')
    elif is_five_divisible:
        print('Chemistry')
    elif is_three_divisible:
        print('Biology')
    else:
        print(num)
