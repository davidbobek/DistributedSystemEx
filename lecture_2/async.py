import sys
import time
from codetiming import Timer


def sync_fib(n):
    """
    Synchronous Fibonacci numbers: get the n-th Fibonacci number with a delay
    equal to the previous Fibonacci number.

    The Fibonacci numbers are 0, 1, 1, 2, 3, 5, 8, 13, 21,...

    :param n: The index of the Fibonacci number to calculate
    :return: The n-th Fibonacci number
    """
    if n == 0 or n == 1:
        return n

    a = 0
    b = 1
    c = 1
    for index in range(1, n):
        c = a + b
        a = b
        b = c

    time.sleep(c)
    print(c, end=",")
    return c


def main(nfib):
    """
    This is the main function.
    Call it with any parameter you like.
    """
    with Timer(text="Total time = {:.1f}"):
        for index in range(nfib):
            sync_fib(index)


if __name__ == "__main__":
    main(int(sys.argv[1]))
