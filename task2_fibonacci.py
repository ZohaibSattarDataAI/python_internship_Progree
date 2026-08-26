"""
TASK 2: Core Algorithmic Fibonacci Generation Module
------------------------------------------------------
Objective : Build a Python module calculating exact sequence values under
            varying parameter limits (bounds).

Features:
    - Clean function that generates Fibonacci numbers up to a given count (n)
      or up to a given upper-bound value (limit).
    - Parameter sanitization: rejects negative bounds / invalid types.
    - Returns output as a structured Python list.
    - Benchmarks execution runtime using the `timeit` framework.
"""

import timeit


def generate_fibonacci(n: int) -> list:
    """
    Generate the first `n` Fibonacci numbers.

    Parameters
    ----------
    n : int
        The number of Fibonacci terms to generate (must be >= 0).

    Returns
    -------
    list[int]
        A structured list containing the Fibonacci sequence.

    Raises
    ------
    TypeError
        If `n` is not an integer.
    ValueError
        If `n` is negative.
    """
    # ---- Parameter sanitization ----
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"Expected an integer for 'n', got {type(n).__name__}")
    if n < 0:
        raise ValueError("Parameter 'n' cannot be negative.")

    # ---- Edge cases ----
    if n == 0:
        return []
    if n == 1:
        return [0]

    sequence = [0, 1]
    while len(sequence) < n:
        sequence.append(sequence[-1] + sequence[-2])

    return sequence


def generate_fibonacci_upto(limit: int) -> list:
    """
    Generate Fibonacci numbers whose value does not exceed `limit`.

    Parameters
    ----------
    limit : int
        The maximum value a Fibonacci term can have (must be >= 0).

    Returns
    -------
    list[int]
        Structured list of Fibonacci numbers <= limit.
    """
    if not isinstance(limit, int) or isinstance(limit, bool):
        raise TypeError(f"Expected an integer for 'limit', got {type(limit).__name__}")
    if limit < 0:
        raise ValueError("Parameter 'limit' cannot be negative.")

    sequence = []
    a, b = 0, 1
    while a <= limit:
        sequence.append(a)
        a, b = b, a + b

    return sequence


def benchmark(func_call: str, globals_dict: dict, number: int = 1000) -> float:
    """
    Benchmark a function call using the timeit framework.

    Parameters
    ----------
    func_call : str
        The statement to time, e.g. "generate_fibonacci(30)".
    globals_dict : dict
        The globals() namespace so timeit can resolve the function.
    number : int
        How many times to execute the statement (default 1000).

    Returns
    -------
    float
        Total execution time in seconds for `number` runs.
    """
    total_time = timeit.timeit(func_call, globals=globals_dict, number=number)
    avg_time = total_time / number
    print(f"[BENCHMARK] '{func_call}' -> total: {total_time:.6f}s "
          f"| avg per run: {avg_time * 1e6:.3f} µs (over {number} runs)")
    return total_time


if __name__ == "__main__":
    # ---- Demo / manual test ----
    print("First 10 Fibonacci numbers:", generate_fibonacci(10))
    print("Fibonacci numbers up to 100:", generate_fibonacci_upto(100))

    # ---- Sanitization demo ----
    for bad_value in [-5, "abc", 3.5]:
        try:
            generate_fibonacci(bad_value)
        except (TypeError, ValueError) as e:
            print(f"Sanitization caught invalid input ({bad_value!r}): {e}")

    # ---- Runtime benchmarking with timeit ----
    benchmark("generate_fibonacci(30)", globals(), number=1000)
    benchmark("generate_fibonacci_upto(10_000)", globals(), number=1000)
