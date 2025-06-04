simple_code1 = """
import math 
b=math.sqrt(16)
print(b)
"""

simple_code2 = """
a = 1
b = 2
c = a + b
print(c)
"""

complex_code1 = """
import numpy as np
import json
from datetime import datetime

# Generate sample data
data = np.random.randn(100)
stats = {
    'mean': float(np.mean(data)),
    'std': float(np.std(data)),
    'min': float(np.min(data)),
    'max': float(np.max(data)),
    'timestamp': datetime.now().isoformat()
}

# Create a simple histogram
hist, bins = np.histogram(data, bins=10)
histogram_data = {
    'counts': hist.tolist(),
    'bins': bins.tolist()
}

result = {
    'stats': stats,
    'histogram': histogram_data,
    'data_length': len(data)
}
"""

# Example 2: Algorithm implementation
complex_code2 = """
def fibonacci_generator(n):
    a, b = 0, 1
    fib_sequence = []
    for _ in range(n):
        fib_sequence.append(a)
        a, b = b, a + b
    return fib_sequence

def prime_checker(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def find_primes_in_range(start, end):
    return [num for num in range(start, end + 1) if prime_checker(num)]

# Execute algorithms
fib_20 = fibonacci_generator(20)
primes_100 = find_primes_in_range(1, 100)

result = {
    'fibonacci_sequence': fib_20,
    'primes_under_100': primes_100,
    'fibonacci_sum': sum(fib_20),
    'prime_count': len(primes_100)
}
"""

# Example 3: Text processing and analysis
complex_code3 = """
import re
from collections import Counter

text = '''
Python is a high-level programming language. Python emphasizes code readability 
with its notable use of significant whitespace. Python's design philosophy 
emphasizes code readability with its use of significant indentation.
'''

# Text analysis
words = re.findall(r'\\b\\w+\\b', text.lower())
word_count = Counter(words)
sentences = [s.strip() for s in text.split('.') if s.strip()]

# Calculate readability metrics
avg_word_length = sum(len(word) for word in words) / len(words)
avg_sentence_length = sum(len(sentence.split()) for sentence in sentences) / len(sentences)

result = {
    'total_words': len(words),
    'unique_words': len(set(words)),
    'most_common_words': word_count.most_common(5),
    'avg_word_length': round(avg_word_length, 2),
    'avg_sentence_length': round(avg_sentence_length, 2),
    'sentences': sentences
}
"""

# Example 4: Data structures and sorting
complex_code4 = """
import random
import time

class SortingAlgorithms:
    @staticmethod
    def bubble_sort(arr):
        n = len(arr)
        comparisons = 0
        for i in range(n):
            for j in range(0, n - i - 1):
                comparisons += 1
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr, comparisons
    
    @staticmethod
    def quick_sort(arr):
        if len(arr) <= 1:
            return arr, 0
        
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        
        left_sorted, left_comp = SortingAlgorithms.quick_sort(left)
        right_sorted, right_comp = SortingAlgorithms.quick_sort(right)
        
        return left_sorted + middle + right_sorted, left_comp + right_comp + len(arr)

# Generate test data
test_data = [random.randint(1, 100) for _ in range(20)]
bubble_data = test_data.copy()
quick_data = test_data.copy()

# Time the algorithms
start_time = time.time()
bubble_result, bubble_comparisons = SortingAlgorithms.bubble_sort(bubble_data)
bubble_time = time.time() - start_time

start_time = time.time()
quick_result, quick_comparisons = SortingAlgorithms.quick_sort(quick_data)
quick_time = time.time() - start_time

result = {
    'original_data': test_data,
    'bubble_sort': {
        'result': bubble_result,
        'comparisons': bubble_comparisons,
        'time_seconds': round(bubble_time, 6)
    },
    'quick_sort': {
        'result': quick_result,
        'comparisons': quick_comparisons,
        'time_seconds': round(quick_time, 6)
    }
}
"""

# Example 5: Mathematical computation
complex_code5 = """
import math
from decimal import Decimal, getcontext

# Set precision for decimal calculations
getcontext().prec = 50

def calculate_pi_leibniz(iterations):
    pi_estimate = 0
    for n in range(iterations):
        pi_estimate += ((-1) ** n) / (2 * n + 1)
    return 4 * pi_estimate

def factorial_large(n):
    if n == 0 or n == 1:
        return 1
    result = Decimal(1)
    for i in range(2, n + 1):
        result *= i
    return result

def stirling_approximation(n):
    return math.sqrt(2 * math.pi * n) * (n / math.e) ** n

# Mathematical calculations
pi_approx = calculate_pi_leibniz(10000)
large_factorial = factorial_large(50)
stirling_approx = stirling_approximation(50)

result = {
    'pi_approximation': round(pi_approx, 10),
    'pi_error': abs(pi_approx - math.pi),
    'factorial_50': str(large_factorial),
    'stirling_approximation': round(stirling_approx, 2),
    'stirling_error_percent': round(abs(float(large_factorial) - stirling_approx) / float(large_factorial) * 100, 4)
}
"""