import string
from random import *


# random.randint(a, b)
# Return a random integer N such that a <= N <= b. Alias for randrange(a, b+1).
def somewhat_random_string(a=12, b=12):
    characters = string.ascii_letters + string.digits
    return ''.join(choice(characters) for x in range(randint(a, b)))


x = somewhat_random_string()
print(f'for a=12 and b==12 (default), x is {x}')

x = somewhat_random_string(1, 2)
print(f'for a=1 and b==2, x is {x}')

x = somewhat_random_string(8, 9)
print(f'for a=8 and b==9, x is {x}')


x = somewhat_random_string(10, 20)
print(f'for a=10 and b==20, x is {x}')