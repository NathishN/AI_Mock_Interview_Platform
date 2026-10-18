"""Generator for Category H: Coding, Logical Thinking, and Problem-Solving (40 questions).
20 questions in 01.json, 20 in 02.json.
Coding category: algorithmic code, sample input/output, time & space complexity, key points, common mistakes, follow-ups.
"""
import json
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parents[2] / "data" / "src" / "H_coding"

PART1 = [
    {
        "q": "Write a Python function to check whether a given string is a palindrome, ignoring non-alphanumeric characters and casing.",
        "sub": "String Algorithms",
        "d": "Beginner",
        "ans": "A palindrome reads identical forwards and backwards. The optimal two-pointer approach cleans the string or skips non-alphanumeric characters in a single pass without extra memory allocation:\n\n```python\ndef is_palindrome(s: str) -> bool:\n    left, right = 0, len(s) - 1\n    while left < right:\n        while left < right and not s[left].isalnum():\n            left += 1\n        while left < right and not s[right].isalnum():\n            right -= 1\n        if s[left].lower() != s[right].lower():\n            return False\n        left += 1\n        right -= 1\n    return True\n```\n\nSample Input: `\"A man, a plan, a canal: Panama\"` -> Expected Output: `True`. Sample Input: `\"race a car\"` -> Expected Output: `False`. Time Complexity: O(n) single pass. Space Complexity: O(1) auxiliary space.",
        "kp": ["Two-pointer approach converges inward from string boundaries", "Filter non-alphanumeric characters with `.isalnum()` and normalize with `.lower()`", "Time Complexity: O(n) linear scan", "Space Complexity: O(1) in-place without creating filtered copies"],
        "cm": ["Creating filtered intermediate strings `[c for c in s if c.isalnum()]`, consuming O(n) unnecessary space", "Not handling empty strings or single-character strings (both are valid palindromes)", "Case sensitivity bugs by forgetting `.lower()`"],
        "fu": ["How would you solve this recursively?", "How do you check if an integer is a palindrome without converting it to a string?"],
        "tags": ["coding", "palindrome", "two-pointers", "strings", "algorithms"]
    },
    {
        "q": "Write a Python function to check whether an integer is a palindrome without converting it to a string.",
        "sub": "Mathematical Algorithms",
        "d": "Intermediate",
        "ans": "To check integer palindromes without string conversion, reverse the second half of the number mathematically and compare it with the first half:\n\n```python\ndef is_palindrome_int(x: int) -> bool:\n    if x < 0 or (x % 10 == 0 and x != 0):\n        return False\n    reversed_half = 0\n    while x > reversed_half:\n        reversed_half = reversed_half * 10 + x % 10\n        x //= 10\n    return x == reversed_half or x == reversed_half // 10\n```\n\nSample Input: `121` -> Expected Output: `True`. Sample Input: `-121` -> Expected Output: `False`. Sample Input: `10` -> Expected Output: `False`. Negative numbers cannot be palindromes due to leading `-`. Reversing only half the digits prevents integer overflow. Time Complexity: O(log10(n)) proportional to digit count. Space Complexity: O(1) constant.",
        "kp": ["Negative numbers and non-zero multiples of 10 can never be palindromes", "Reverse only the second half of the integer to avoid potential overflow", "Middle digit in odd-length numbers is handled via `reversed_half // 10`", "Time Complexity: O(log10(n)); Space Complexity: O(1)"],
        "cm": ["Converting integer to string `str(x) == str(x)[::-1]`, which violates the interview constraint", "Forgetting that numbers ending in 0 (like 10, 100) are not palindromes except 0 itself", "Reversing the entire 32-bit integer, risking overflow in languages like C/Java"],
        "fu": ["Why does reversing only half the digits prevent integer overflow in C/Java?", "What is the time complexity in terms of the number of digits d?"],
        "tags": ["coding", "math", "palindrome", "integer-reversal", "algorithms"]
    },
    {
        "q": "Write a Python function to reverse the words in a sentence string while preserving single spaces.",
        "sub": "String Algorithms",
        "d": "Beginner",
        "ans": "To reverse words in a sentence while trimming extra spaces:\n\n```python\ndef reverse_words(s: str) -> str:\n    words = s.split()\n    return ' '.join(reversed(words))\n```\n\n`s.split()` without arguments automatically handles arbitrary whitespace, trimming leading/trailing spaces and collapsing consecutive spaces into single tokens. `reversed(words)` reverses the list in O(n) time, and `' '.join()` constructs the final normalized string. Sample Input: `\"  the sky   is blue  \"` -> Expected Output: `\"blue is sky the\"`. Time Complexity: O(n) where n is string length. Space Complexity: O(n) to hold split words.",
        "kp": ["`s.split()` without arguments splits on whitespace and collapses consecutive spaces", "`reversed(words)` or `words[::-1]` reverses word order", "`' '.join(...)` produces single-spaced output", "Time Complexity: O(n); Space Complexity: O(n)"],
        "cm": ["Using `s.split(' ')` with an explicit space delimiter, which retains empty strings from multiple spaces", "Reversing character-by-character instead of word-by-word", "Failing to strip leading and trailing whitespace"],
        "fu": ["How would you reverse words in-place if the input was a mutable character array `list[str]`?", "What is the three-step reversal algorithm (reverse entire array, then reverse each word)?"],
        "tags": ["coding", "strings", "reverse-words", "two-pointers"]
    },
    {
        "q": "Write a Python function to find the maximum sum of a contiguous subarray using Kadane's Algorithm.",
        "sub": "Array Algorithms",
        "d": "Intermediate",
        "ans": "Kadane's Algorithm computes the maximum contiguous subarray sum in a single linear pass:\n\n```python\ndef max_subarray_sum(nums: list[int]) -> int:\n    if not nums:\n        raise ValueError(\"List cannot be empty\")\n    max_current = max_global = nums[0]\n    for num in nums[1:]:\n        max_current = max(num, max_current + num)\n        if max_current > max_global:\n            max_global = max_current\n    return max_global\n```\n\nAt each index, we decide whether to extend the previous running subarray (`max_current + num`) or start a fresh subarray at `num` (`max(num, max_current + num)`). Sample Input: `[-2, 1, -3, 4, -1, 2, 1, -5, 4]` -> Expected Output: `6` (subarray `[4, -1, 2, 1]`). Time Complexity: O(n). Space Complexity: O(1).",
        "kp": ["Recurrence relation: `max_current = max(num, max_current + num)`", "Initializes with `nums[0]` to handle arrays containing all negative numbers", "Time Complexity: O(n) single pass; Space Complexity: O(1) in-place", "Returns optimal contiguous subarray sum"],
        "cm": ["Initializing `max_global` to 0, which fails on arrays of all negative integers (e.g., `[-3, -1, -2]`)", "Using O(n^2) nested loops checking every subarray combination", "Confusing contiguous subarrays with non-contiguous subsequences"],
        "fu": ["How would you return the starting and ending indices of the maximal subarray?", "Can Kadane's algorithm be adapted to find the maximum product subarray?"],
        "tags": ["coding", "kadanes-algorithm", "arrays", "dynamic-programming"]
    },
    {
        "q": "Write a Python function to solve the Two Sum problem: return 0-based indices of two numbers that add up to a target.",
        "sub": "Hash Map Algorithms",
        "d": "Beginner",
        "ans": "Using a hash map allows solving Two Sum in a single O(n) pass by storing each number's index as we iterate:\n\n```python\ndef two_sum(nums: list[int], target: int) -> list[int]:\n    seen = {}\n    for i, num in enumerate(nums):\n        diff = target - num\n        if diff in seen:\n            return [seen[diff], i]\n        seen[num] = i\n    return []\n```\n\nFor each number, we calculate its required complement (`target - num`). If the complement exists in our dictionary `seen`, we return the pair of indices `[seen[diff], i]`. If not, we store `seen[num] = i`. Sample Input: `nums = [2, 7, 11, 15], target = 9` -> Expected Output: `[0, 1]`. Time Complexity: O(n) average hash table lookups. Space Complexity: O(n) auxiliary map.",
        "kp": ["Single-pass hash table lookup achieves O(n) linear time", "Tracks required complement `target - num`", "Key is array element; Value is its original 0-based index", "Time Complexity: O(n); Space Complexity: O(n)"],
        "cm": ["Using brute-force nested loops taking O(n^2) time", "Populating the entire dictionary before checking, causing duplicate numbers to overwrite indices", "Returning array values instead of array indices"],
        "fu": ["How do you solve Two Sum if the input array is already sorted in O(1) space?", "How would you return all unique pairs that sum to target without duplicate pairs?"],
        "tags": ["coding", "two-sum", "hash-map", "arrays", "algorithms"]
    },
    {
        "q": "Write a Python function to move all zeros in an integer list to the end in-place while maintaining relative order of non-zeros.",
        "sub": "Two-Pointer Algorithms",
        "d": "Beginner",
        "ans": "Using a two-pointer approach moves zeros to the end in-place without allocating a second array:\n\n```python\ndef move_zeroes(nums: list[int]) -> None:\n    insert_pos = 0\n    for i in range(len(nums)):\n        if nums[i] != 0:\n            nums[insert_pos], nums[i] = nums[i], nums[insert_pos]\n            insert_pos += 1\n```\n\n`insert_pos` tracks where the next non-zero element belongs. When `nums[i] != 0`, we swap `nums[insert_pos]` and `nums[i]`, and advance `insert_pos`. Non-zero elements retain their relative ordering, and zeros migrate toward the end. Sample Input: `[0, 1, 0, 3, 12]` -> Output: `[1, 3, 12, 0, 0]`. Time Complexity: O(n). Space Complexity: O(1) strictly in-place.",
        "kp": ["Two-pointer partition pattern swaps non-zero elements forward", "Maintains relative order of all non-zero elements", "Time Complexity: O(n) single pass; Space Complexity: O(1) in-place", "Avoids creating a new list"],
        "cm": ["Using `nums.remove(0)` followed by `nums.append(0)` in a loop (O(n^2) time due to element shifting)", "Allocating a new list `[x for x in nums if x != 0] + [0]*zeros` when in-place modification is required", "Losing relative order of non-zero elements"],
        "fu": ["What is the minimum number of write operations needed if the array has mostly zeros?", "How does this algorithm relate to the partitioning step of QuickSort?"],
        "tags": ["coding", "two-pointers", "arrays", "in-place", "algorithms"]
    },
    {
        "q": "Write a Python function to remove duplicates from a sorted integer array in-place and return the new length.",
        "sub": "Two-Pointer Algorithms",
        "d": "Beginner",
        "ans": "Since the array is already sorted, duplicate elements are contiguous. We use two pointers: a write pointer `write_idx` and a scan pointer `read_idx`:\n\n```python\ndef remove_duplicates_sorted(nums: list[int]) -> int:\n    if not nums:\n        return 0\n    write_idx = 1\n    for read_idx in range(1, len(nums)):\n        if nums[read_idx] != nums[read_idx - 1]:\n            nums[write_idx] = nums[read_idx]\n            write_idx += 1\n    return write_idx\n```\n\nWe overwrite elements in-place only when the current element differs from the preceding element. Elements beyond `write_idx` are ignored. Sample Input: `[0, 0, 1, 1, 1, 2, 2, 3, 3, 4]` -> Returns: `5`, with `nums[:5] = [0, 1, 2, 3, 4]`. Time Complexity: O(n). Space Complexity: O(1) in-place.",
        "kp": ["Capitalizes on sorted property: duplicates are adjacent", "Slow pointer `write_idx` overwrites unique values", "Returns length of unique prefix without allocating extra memory", "Time Complexity: O(n); Space Complexity: O(1)"],
        "cm": ["Using `set(nums)` and reassigning, which creates a new object and may lose sorted order", "Deleting elements using `nums.pop(i)` or `del nums[i]` inside a loop (O(n^2) list shifting)", "Off-by-one errors on edge cases with 0 or 1 element"],
        "fu": ["How would you allow at most two duplicates (Remove Duplicates from Sorted Array II)?", "Why is in-place array modification preferred in embedded or high-throughput systems?"],
        "tags": ["coding", "two-pointers", "arrays", "sorted-array", "in-place"]
    },
    {
        "q": "Write a Python function to find the missing number in an array containing distinct integers from 0 to n.",
        "sub": "Mathematical & Bitwise",
        "d": "Beginner",
        "ans": "An array of length n contains distinct numbers from the range `[0, n]`. Exactly one number is missing. Method 1 (Summation formula): compute expected sum `n * (n + 1) // 2` and subtract the actual array sum in O(n) time and O(1) space. Method 2 (XOR bitwise approach): XOR all indices `0` to `n` with all array values; since `x ^ x = 0` and `x ^ 0 = x`, all pairs cancel out, leaving the missing number:\n\n```python\ndef missing_number_xor(nums: list[int]) -> int:\n    n = len(nums)\n    missing = n\n    for i, num in enumerate(nums):\n        missing ^= i ^ num\n    return missing\n```\n\nSample Input: `[3, 0, 1]` -> Output: `2`. Sample Input: `[9,6,4,2,3,5,7,0,1]` -> Output: `8`. Time Complexity: O(n). Space Complexity: O(1). XOR avoids potential arithmetic overflow.",
        "kp": ["Gauss sum formula: `n * (n + 1) // 2` gives expected sum in O(1)", "XOR property: `a ^ a = 0` and `a ^ 0 = a` cancels duplicates", "XOR bitwise approach prevents integer overflow in fixed-width integer languages", "Time Complexity: O(n); Space Complexity: O(1)"],
        "cm": ["Sorting the array first (O(n log n) time penalty)", "Using a hash set lookup, consuming O(n) unnecessary auxiliary memory", "Off-by-one errors in determining n (`len(nums)`)"],
        "fu": ["What if two numbers are missing instead of one? How do you partition with XOR?", "How does XOR encryption work in cryptography?"]
    },
    {
        "q": "Write a Python function to determine if two input strings are valid anagrams of each other.",
        "sub": "String Algorithms",
        "d": "Beginner",
        "ans": "Two strings are anagrams if they have the identical character frequency counts. Optimal solution uses `collections.Counter` or an integer frequency array of size 26 for ASCII lowercase:\n\n```python\nfrom collections import Counter\n\ndef is_anagram(s: str, t: str) -> bool:\n    if len(s) != len(t):\n        return False\n    return Counter(s) == Counter(t)\n```\n\nEarly exit: return `False` immediately if string lengths differ. `Counter(s) == Counter(t)` constructs and compares frequency hash maps in O(n) time and O(k) space (where k is unique characters). Sorting `sorted(s) == sorted(t)` runs in O(n log n) time. Sample Input: `s = \"anagram\", t = \"nagaram\"` -> Output: `True`. Sample Input: `s = \"rat\", t = \"car\"` -> Output: `False`.",
        "kp": ["Early exit check: if lengths differ, return False immediately", "Hash map frequency counting via `collections.Counter` runs in O(n) time", "Sorting approach `sorted(s) == sorted(t)` runs in O(n log n) time", "Time Complexity: O(n); Space Complexity: O(1) if alphabet is fixed (26 chars)"],
        "cm": ["Calling `s.count(c)` inside a loop over characters, causing O(n^2) quadratic time", "Forgetting early exit on unequal string lengths", "Not considering Unicode or case normalization if required by question constraints"],
        "fu": ["How would you solve Group Anagrams across a list of 100,000 strings in O(N * K) time?", "How do you implement an array of size 26 using `ord(c) - ord('a')`?"],
        "tags": ["coding", "anagram", "strings", "hash-map", "counter"]
    },
    {
        "q": "Write a Python function to implement Binary Search on a sorted list. Return the index or -1 if not found.",
        "sub": "Search Algorithms",
        "d": "Beginner",
        "ans": "Binary search repeatedly divides a sorted search interval in half:\n\n```python\ndef binary_search(nums: list[int], target: int) -> int:\n    low, high = 0, len(nums) - 1\n    while low <= high:\n        mid = (low + high) // 2\n        if nums[mid] == target:\n            return mid\n        elif nums[mid] < target:\n            low = mid + 1\n        else:\n            high = mid - 1\n    return -1\n```\n\nMaintain search bounds `low` and `high`. Calculate `mid`. If `nums[mid] == target`, target is found. If `nums[mid] < target`, search the right half (`low = mid + 1`); otherwise search the left half (`high = mid - 1`). Sample Input: `nums = [-1, 0, 3, 5, 9, 12], target = 9` -> Output: `4`. Time Complexity: O(log n). Space Complexity: O(1) iterative.",
        "kp": ["Precondition: input array must be sorted in ascending order", "Loop condition `low <= high` ensures single-element intervals are checked", "Pointer updates: `low = mid + 1` and `high = mid - 1` prevent infinite loops", "Time Complexity: O(log n); Space Complexity: O(1)"],
        "cm": ["Using `low < high` instead of `low <= high`, missing target when it sits at array boundaries", "Applying binary search on unsorted collections or linked lists", "Recursive binary search without tail-call optimization, consuming O(log n) call stack space"],
        "fu": ["How do you find the first and last position of an element in a sorted array with duplicates?", "How does binary search find the peak element in a mountain array?"],
        "tags": ["coding", "binary-search", "algorithms", "searching", "arrays"]
    },
    {
        "q": "Write a Python function to validate whether a string of brackets `()[]{}` is properly balanced and closed.",
        "sub": "Stack Algorithms",
        "d": "Intermediate",
        "ans": "Using a Last-In-First-Out (LIFO) stack ensures opening brackets are matched with the correct closing brackets in proper nested order:\n\n```python\ndef is_valid_parentheses(s: str) -> bool:\n    mapping = {')': '(', '}': '{', ']': '['}\n    stack = []\n    for char in s:\n        if char in mapping:\n            top = stack.pop() if stack else '#'\n            if mapping[char] != top:\n                return False\n        else:\n            stack.append(char)\n    return not stack\n```\n\nWhen encountering an opening bracket, push it to the stack. When encountering a closing bracket, pop the top of the stack and check if it matches the closing bracket's pair. If mismatched or stack was empty, return `False`. After scanning, return `True` only if stack is empty. Sample Input: `\"()[]{}\"` -> `True`. Sample Input: `\"([)]\"` -> `False`. Time Complexity: O(n). Space Complexity: O(n).",
        "kp": ["Stack data structure enforces Last-In-First-Out matching order", "Map closing brackets to opening brackets in a lookup dictionary", "Pop and compare on closing brackets; return False on mismatch or empty stack", "Final check: stack must be empty (`return not stack`)"],
        "cm": ["Using simple integer counters, which fails on mixed nested brackets like `\"([)]\"`", "Calling `stack.pop()` without checking if stack is empty (causes IndexError)", "Forgetting the final `not stack` check, incorrectly returning True for unclosed openers like `\"((\"`"],
        "fu": ["How would you return the length of the longest valid parentheses substring?", "How do web browsers use stacks to validate HTML opening and closing tags?"],
        "tags": ["coding", "stack", "parentheses", "data-structures", "algorithms"]
    },
    {
        "q": "Write a Python function to find the second largest element in an array in O(n) time without sorting.",
        "sub": "Array Algorithms",
        "d": "Intermediate",
        "ans": "Tracking the largest and second largest elements in a single linear pass avoids O(n log n) sorting overhead and handles duplicates:\n\n```python\ndef second_largest(nums: list[int]) -> int | None:\n    if len(nums) < 2:\n        return None\n    first = second = -float('inf')\n    for n in nums:\n        if n > first:\n            second = first\n            first = n\n        elif first > n > second:\n            second = n\n    return second if second != -float('inf') else None\n```\n\nInitialize `first` and `second` to `-float('inf')` to properly support negative numbers. If `n > first`, shift `first` to `second` and update `first`. If `first > n > second`, update `second`. Sample Input: `[12, 35, 1, 10, 34, 1]` -> Output: `34`. Sample Input: `[10, 10, 10]` -> Output: `None`. Time Complexity: O(n). Space Complexity: O(1).",
        "kp": ["Single pass O(n) time; O(1) constant auxiliary space", "Initialize trackers to negative infinity (`-float('inf')`) for negative inputs", "Strict inequality `first > n > second` handles duplicate maximums correctly", "Returns None if fewer than two distinct elements exist"],
        "cm": ["Sorting array and indexing `nums[-2]`, which fails if duplicate maximums exist (e.g., `[10, 10, 5]` returns 10)", "Initializing tracking variables to 0, which fails on lists containing negative numbers", "Not handling empty lists or single-element inputs"],
        "fu": ["How would you extend this to find the K-th largest element using a min-heap in O(n log k) time?", "What is the Quickselect algorithm and how does it achieve O(n) average time for K-th largest?"],
        "tags": ["coding", "arrays", "second-largest", "algorithms", "time-complexity"]
    },
    {
        "q": "Write an efficient Python function to calculate the N-th Fibonacci number. Compare iterative vs recursive approaches.",
        "sub": "Dynamic Programming",
        "d": "Beginner",
        "ans": "Naive recursion `fib(n-1) + fib(n-2)` has exponential O(2^n) time complexity due to redundant recalculations. The optimal iterative approach runs in O(n) time and O(1) space by maintaining only the previous two terms:\n\n```python\ndef fibonacci(n: int) -> int:\n    if n < 0:\n        raise ValueError(\"n must be non-negative\")\n    if n <= 1:\n        return n\n    prev2, prev1 = 0, 1\n    for _ in range(2, n + 1):\n        prev2, prev1 = prev1, prev2 + prev1\n    return prev1\n```\n\nSample Input: `n = 0` -> `0`. Sample Input: `n = 1` -> `1`. Sample Input: `n = 10` -> `55`. Time Complexity: O(n) linear loop. Space Complexity: O(1) constant memory. Python automatically supports arbitrary-precision integers, preventing overflow.",
        "kp": ["Naive recursion causes exponential O(2^n) time and stack overflow", "Iterative state tracking computes N-th Fibonacci in O(n) time and O(1) space", "Base cases: `fib(0) = 0`, `fib(1) = 1`", "Space optimization: only the last two values (`prev1`, `prev2`) are retained in memory"],
        "cm": ["Using naive recursion for n > 35, freezing the program", "Allocating an entire list of size n when only the last two values are needed", "Off-by-one errors on base cases n=0 and n=1"],
        "fu": ["How does `@functools.lru_cache` optimize the recursive implementation to O(n)?", "How can Fibonacci be computed in O(log n) time using 2x2 matrix exponentiation?"],
        "tags": ["coding", "fibonacci", "dynamic-programming", "math", "algorithms"]
    },
    {
        "q": "Write a Python function to check whether a given integer N is prime in O(sqrt(N)) time.",
        "sub": "Mathematical Algorithms",
        "d": "Beginner",
        "ans": "A prime number is an integer greater than 1 divisible only by 1 and itself. We optimize trial division to O(sqrt(n)) because factors appear in pairs `(a, b)` where `a * b = n`; at least one factor must be `<= sqrt(n)`:\n\n```python\ndef is_prime(n: int) -> bool:\n    if n <= 1:\n        return False\n    if n <= 3:\n        return True\n    if n % 2 == 0 or n % 3 == 0:\n        return False\n    i = 5\n    while i * i <= n:\n        if n % i == 0 or n % (i + 2) == 0:\n            return False\n        i += 6\n    return True\n```\n\nChecking `6k ± 1` skips all multiples of 2 and 3, reducing division checks by two-thirds. Sample Input: `11` -> `True`. Sample Input: `25` -> `False`. Sample Input: `1` -> `False`. Time Complexity: O(sqrt(n)). Space Complexity: O(1).",
        "kp": ["Primes are strictly integers > 1", "Trial division up to `sqrt(n)` runs in O(sqrt(n)) time", "6k ± 1 optimization skips multiples of 2 and 3", "Time Complexity: O(sqrt(n)); Space Complexity: O(1)"],
        "cm": ["Checking factors up to n instead of sqrt(n), causing unnecessary iterations", "Classifying 0 or 1 as prime numbers (neither is prime)", "Using floating point `math.sqrt(n)` without adding 1, causing precision truncations"],
        "fu": ["What is the Sieve of Eratosthenes and how does it find all primes up to N in O(N log log N) time?", "What is the Fermat Little Theorem test for probabilistic primality testing?"],
        "tags": ["coding", "primes", "math", "algorithms", "number-theory"]
    },
    {
        "q": "Write a Python function to calculate the factorial of a non-negative integer N iteratively and recursively.",
        "sub": "Mathematical Algorithms",
        "d": "Beginner",
        "ans": "Factorial of N (`N!`) is the product of all positive integers `<= N`; `0!` is defined as `1`. 1) Iterative implementation (O(n) time, O(1) space):\n\n```python\ndef factorial_iterative(n: int) -> int:\n    if n < 0:\n        raise ValueError(\"Factorial undefined for negative numbers\")\n    result = 1\n    for i in range(2, n + 1):\n        result *= i\n    return result\n```\n\n2) Recursive implementation: `return 1 if n <= 1 else n * factorial_recursive(n - 1)`. Sample Input: `5` -> `120`. Sample Input: `0` -> `1`. Iterative is preferred because it avoids Python's recursion limit for large inputs. In production, `math.factorial(n)` is C-optimized and significantly faster.",
        "kp": ["0! is defined as 1; negative numbers have undefined factorial", "Iterative approach runs in O(n) time and O(1) space without call stack limits", "Recursive approach runs in O(n) time and O(n) stack frames", "Standard library `math.factorial(n)` is C-optimized"],
        "cm": ["Forgetting base case `0! = 1`", "Not validating negative inputs (should raise ValueError)", "Hitting recursion depth limit on large numbers in recursive version"],
        "fu": ["How does Python handle arbitrary-precision integers without overflow during large factorial calculations?", "What is Stirling's approximation formula for estimating large factorials?"],
        "tags": ["coding", "factorial", "math", "recursion", "algorithms"]
    },
    {
        "q": "Write a Python function to perform basic String Compression (Run-Length Encoding) using counts of repeated characters.",
        "sub": "String Algorithms",
        "d": "Intermediate",
        "ans": "Run-length encoding compresses consecutive duplicate characters into character-count pairs (e.g., `\"aabcccccaaa\"` -> `\"a2b1c5a3\"`). Return original string if compressed string is not shorter:\n\n```python\ndef compress_string(s: str) -> str:\n    if not s:\n        return \"\"\n    compressed = []\n    count = 1\n    for i in range(1, len(s)):\n        if s[i] == s[i - 1]:\n            count += 1\n        else:\n            compressed.append(f\"{s[i - 1]}{count}\")\n            count = 1\n    compressed.append(f\"{s[-1]}{count}\")\n    result = \"\".join(compressed)\n    return result if len(result) < len(s) else s\n```\n\nSample Input: `\"aabcccccaaa\"` -> Output: `\"a2b1c5a3\"`. Sample Input: `\"abcdef\"` -> Output: `\"abcdef\"` (compressed `\"a1b1c1d1e1f1\"` is longer). Time Complexity: O(n). Space Complexity: O(n).",
        "kp": ["Appends characters and run counts using a list before `\"\".join()` for O(n) time", "Handles trailing character group after loop terminates", "Returns original string if compressed length is not strictly shorter", "Time Complexity: O(n); Space Complexity: O(n)"],
        "cm": ["Using string concatenation `res += char + str(count)` in a loop (O(n^2) time)", "Missing the final run group of characters after loop exits", "Returning compressed string even when it is longer than original (e.g., 'a' -> 'a1')"],
        "fu": ["How would you decompress a run-length encoded string in O(n) time?", "When is Run-Length Encoding effective vs ineffective for image compression (e.g., BMP vs JPEG)?"],
        "tags": ["coding", "strings", "run-length-encoding", "compression", "algorithms"]
    },
    {
        "q": "Write a Python function to rotate a list of N integers to the right by K steps in-place.",
        "sub": "Array Algorithms",
        "d": "Intermediate",
        "ans": "Rotating an array right by K steps can be achieved in O(n) time and O(1) space using the Three-Step Array Reversal algorithm: 1) Normalize `k = k % len(nums)`, 2) Reverse the entire array, 3) Reverse the first `k` elements, 4) Reverse the remaining `n - k` elements:\n\n```python\ndef rotate(nums: list[int], k: int) -> None:\n    n = len(nums)\n    k = k % n\n    def reverse(start: int, end: int) -> None:\n        while start < end:\n            nums[start], nums[end] = nums[end], nums[start]\n            start += 1\n            end -= 1\n    reverse(0, n - 1)      # Reverse entire array\n    reverse(0, k - 1)      # Reverse first k elements\n    reverse(k, n - 1)      # Reverse remaining elements\n```\n\nSample Input: `nums = [1,2,3,4,5,6,7], k = 3` -> Output: `[5,6,7,1,2,3,4]`. Time Complexity: O(n). Space Complexity: O(1) strictly in-place.",
        "kp": ["Normalize k: `k = k % n` handles k larger than array length", "Three-step reversal: reverse all -> reverse first k -> reverse remainder", "Time Complexity: O(n); Space Complexity: O(1) in-place", "Avoids allocating auxiliary array"],
        "cm": ["Rotating 1 step k times sequentially in a loop, resulting in O(n * k) slow time", "Forgetting `k = k % n`, causing IndexError when k exceeds array length", "Allocating a new sliced list `nums[-k:] + nums[:-k]` when in-place modification is required"],
        "fu": ["How does cyclic replacements (Juggling algorithm) rotate an array in O(n) using GCD?", "How do you rotate an array to the left instead of right using reversal?"],
        "tags": ["coding", "arrays", "array-rotation", "reversal-algorithm", "in-place"]
    },
    {
        "q": "Write a Python function to find the longest common prefix string among an array of strings.",
        "sub": "String Algorithms",
        "d": "Beginner",
        "ans": "Vertical scanning compares characters column by column across all strings:\n\n```python\ndef longest_common_prefix(strs: list[str]) -> str:\n    if not strs:\n        return \"\"\n    for i, char in enumerate(strs[0]):\n        for string in strs[1:]:\n            if i == len(string) or string[i] != char:\n                return strs[0][:i]\n    return strs[0]\n```\n\nIterate through characters of the first string `strs[0]`. For each character at index `i`, check if any other string is either shorter (`i == len(string)`) or has a mismatched character (`string[i] != char`). If so, return `strs[0][:i]`. If loop completes, `strs[0]` is the common prefix. Sample Input: `[\"flower\",\"flow\",\"flight\"]` -> Output: `\"fl\"`. Sample Input: `[\"dog\",\"racecar\",\"car\"]` -> Output: `\"\"`. Time Complexity: O(S) where S is sum of characters. Space Complexity: O(1).",
        "kp": ["Vertical scanning compares characters across all words column-by-column", "Terminates early on first mismatch or when shortest string is exhausted", "Handles empty input list or single-string inputs", "Time Complexity: O(S) where S is total characters; Space: O(1)"],
        "cm": ["Comparing strings pairwise horizontally without early termination on empty prefix", "Index out of bounds errors when checking strings shorter than the first string", "Sorting the array first (O(N log N * M)) when linear vertical scan is faster"],
        "fu": ["How can a Trie (Prefix Tree) be used to solve longest common prefix?", "How does binary search over prefix lengths compare in performance?"],
        "tags": ["coding", "strings", "longest-common-prefix", "algorithms"]
    },
    {
        "q": "Write a Python function to merge two sorted integer lists into a single sorted list in O(n + m) time.",
        "sub": "Merge Algorithms",
        "d": "Beginner",
        "ans": "Using two pointers achieves optimal O(n + m) linear time without sorting:\n\n```python\ndef merge_sorted_lists(l1: list[int], l2: list[int]) -> list[int]:\n    merged = []\n    i = j = 0\n    while i < len(l1) and j < len(l2):\n        if l1[i] <= l2[j]:\n            merged.append(l1[i])\n            i += 1\n        else:\n            merged.append(l2[j])\n            j += 1\n    merged.extend(l1[i:])\n    merged.extend(l2[j:])\n    return merged\n```\n\nCompare current elements `l1[i]` and `l2[j]`. Append the smaller element to `merged` and advance its pointer. Once one list is exhausted, append remaining elements of the other list. This is the core merge step of MergeSort. Sample Input: `l1 = [1, 2, 4], l2 = [1, 3, 4]` -> Output: `[1, 1, 2, 3, 4, 4]`. Time Complexity: O(n + m). Space Complexity: O(n + m).",
        "kp": ["Two-pointer comparison traverses both lists simultaneously", "Appends remaining elements via `.extend()` after one list is exhausted", "Core merge routine used in Merge Sort and external sorting", "Time Complexity: O(n + m); Space Complexity: O(n + m)"],
        "cm": ["Concatenating lists and calling `sorted(l1 + l2)` (O((n+m) log(n+m)) time penalty)", "Missing elements from the longer list when the while loop terminates", "Using `<=` comparison preserves sorting stability for equal elements"],
        "fu": ["How do you merge two sorted arrays in-place if array 1 has trailing buffer space (LeetCode 88)?", "How does `heapq.merge(*iterables)` merge multiple sorted streams lazily in O(N log K)?"],
        "tags": ["coding", "merge-sort", "arrays", "two-pointers", "sorting"]
    },
    {
        "q": "Write a Python function to detect a cycle in a Singly Linked List using Floyd's Cycle-Finding Algorithm (Tortoise and Hare).",
        "sub": "Linked List Algorithms",
        "d": "Intermediate",
        "ans": "Floyd's Cycle-Finding Algorithm uses two pointers moving at different speeds to detect cycles in O(n) time and O(1) space:\n\n```python\nclass ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef has_cycle(head: ListNode | None) -> bool:\n    slow = fast = head\n    while fast and fast.next:\n        slow = slow.next          # 1 step\n        fast = fast.next.next     # 2 steps\n        if slow is fast:\n            return True\n    return False\n```\n\n`slow` advances 1 node per iteration; `fast` advances 2 nodes. If no cycle exists, `fast` reaches the end (`None`). If a cycle exists, `fast` enters the loop and catches up to `slow` from behind. Time Complexity: O(n). Space Complexity: O(1) constant memory.",
        "kp": ["Slow pointer moves 1 step; Fast pointer moves 2 steps", "Fast pointer catches up to slow pointer if a cycle exists", "Fast pointer reaches None if no cycle exists", "Time Complexity: O(n); Space Complexity: O(1) in-place"],
        "cm": ["Checking `fast.next` without checking `fast` first, raising AttributeError", "Using a hash set to store seen nodes, consuming O(n) extra space instead of O(1)", "Modifying node values destructively to mark visited nodes"],
        "fu": ["How do you find the exact node where the cycle begins (Floyd's algorithm phase 2)?", "How does cycle detection apply to detecting deadlocks in operating systems?"]
    }
]

PART2 = [
    {
        "q": "Explain Bubble Sort, Selection Sort, and Insertion Sort. Compare their time and space complexities.",
        "sub": "Elementary Sorting",
        "d": "Beginner",
        "ans": "1) Bubble Sort: repeatedly steps through the list, compares adjacent elements, and swaps them if in wrong order. Largest unsorted element 'bubbles up' to the end on each pass. Best: O(n) with swap flag; Average/Worst: O(n^2); Space: O(1); Stable. 2) Selection Sort: repeatedly finds minimum element from unsorted portion and swaps it with the first unsorted position. Makes minimum number of writes (at most n swaps). Best/Average/Worst: O(n^2) always; Space: O(1); Unstable. 3) Insertion Sort: iterates through array, picking current element and inserting it into its correct sorted position among previously scanned elements. Excellent for small or nearly sorted arrays. Best: O(n); Average/Worst: O(n^2); Space: O(1); Stable.",
        "kp": ["Bubble Sort: adjacent swaps; O(n^2) time, O(1) space; stable", "Selection Sort: finds minimum and swaps; O(n^2) always, minimum writes; unstable", "Insertion Sort: shifts elements to insert; O(n) best case on nearly sorted data; stable", "All three have O(1) constant auxiliary space"],
        "cm": ["Assuming Selection Sort is stable (swapping can move duplicate elements across each other)", "Forgetting the early-exit optimization flag in Bubble Sort for already-sorted lists", "Using O(n^2) elementary sorts on large datasets (> 10,000 elements)"],
        "fu": ["Why is Insertion Sort used as the base case in hybrid algorithms like Timsort for small partitions (n <= 32)?", "What is an 'inversion' in an array and how does it relate to sorting complexity?"]
    },
    {
        "q": "Explain Merge Sort and Quick Sort. What are their average and worst-case complexities, and when is each preferred?",
        "sub": "Divide and Conquer Sorting",
        "d": "Intermediate",
        "ans": "1) Merge Sort: Divide-and-Conquer algorithm that divides array into two halves, recursively sorts them, and merges sorted halves. Guranteed O(n log n) time in best, average, and worst cases. Stable sort. Disadvantage: requires O(n) auxiliary memory for merge buffers. Preferred for linked lists and external disk sorting. 2) Quick Sort: Divide-and-Conquer algorithm that selects a 'pivot' element, partitions array such that elements smaller than pivot are on left and larger on right, and recursively sorts partitions. Average time: O(n log n); Worst case: O(n^2) when pivot selection is poor (e.g., sorted array with first element as pivot). Unstable sort. Advantage: O(log n) in-place space, excellent cache locality, faster in practice on arrays.",
        "kp": ["Merge Sort: guaranteed O(n log n) best/average/worst; O(n) space; stable", "Quick Sort: O(n log n) average, O(n^2) worst case; O(log n) space in-place; unstable", "Quick Sort preferred for in-memory array sorting due to cache locality", "Merge Sort preferred for linked lists and external sorting where stable O(n log n) is needed"],
        "cm": ["Selecting the first element as pivot in Quick Sort on sorted inputs (triggers worst-case O(n^2) time)", "Assuming Quick Sort requires O(1) space (recursive call stack requires O(log n) space)", "Believing Merge Sort can be easily performed in-place on arrays without complex overhead"],
        "fu": ["How does Median-of-Three or randomized pivot selection prevent Quick Sort's O(n^2) worst case?", "Why is Merge Sort stable while standard Quick Sort is unstable?"]
    },
    {
        "q": "Explain Heap Sort and Priority Queues. What are the time complexities for insertion, deletion, and heapify?",
        "sub": "Heap Algorithms",
        "d": "Intermediate",
        "ans": "A Binary Heap is a complete binary tree satisfying the Heap Property: in a Min-Heap, each parent node is `<= ` its children (root is minimum); in a Max-Heap, each parent is `>=` its children (root is maximum). Array representation: for node at index `i`, left child is `2i + 1`, right child is `2i + 2`, and parent is `(i - 1) // 2`. Operations: 1) `Insert (heappush)`: append to end and bubble up; O(log n). 2) `Extract Min/Max (heappop)`: replace root with last element and bubble down (sift down); O(log n). 3) `Build Heap (heapify)`: converts unorganized array of N elements into a valid heap in O(n) linear time. Heap Sort builds a Max-Heap and repeatedly swaps root with end, achieving guaranteed O(n log n) time and O(1) in-place auxiliary space.",
        "kp": ["Heap property: parent is always <= (min-heap) or >= (max-heap) children", "Binary heap mapped compactly into flat array using index arithmetic", "Heapify constructs a heap from unsorted array in O(n) linear time", "Heap Sort: guaranteed O(n log n) time in all cases with O(1) auxiliary space"],
        "cm": ["Assuming building a heap of N elements takes O(N log N) (it takes O(N) due to mathematical series convergence)", "Confusing a Binary Heap with a Binary Search Tree (heap has no left < right ordering)", "Using standard sorting when a Priority Queue is only querying top-K elements"],
        "fu": ["Why does `heapify()` run in O(n) time rather than O(n log n)?", "How does Python's `heapq` module implement Min-Heaps? How do you create a Max-Heap with it?"]
    },
    {
        "q": "What is the Sieve of Eratosthenes algorithm? Write a Python function to generate all prime numbers up to N.",
        "sub": "Mathematical Algorithms",
        "d": "Intermediate",
        "ans": "The Sieve of Eratosthenes is an ancient, highly efficient algorithm for finding all prime numbers up to a specified integer N. Algorithm: create a boolean array of size N+1 initialized to True (indices 0 and 1 set to False). For each number `p` starting from 2 up to `sqrt(N)`, if `is_prime[p]` is True, mark all multiples of `p` starting from `p*p` up to N as False. Remaining True indices are primes:\n\n```python\ndef sieve_of_eratosthenes(n: int) -> list[int]:\n    if n < 2:\n        return []\n    is_prime = [True] * (n + 1)\n    is_prime[0] = is_prime[1] = False\n    p = 2\n    while p * p <= n:\n        if is_prime[p]:\n            for multiple in range(p * p, n + 1, p):\n                is_prime[multiple] = False\n        p += 1\n    return [i for i, prime in enumerate(is_prime) if prime]\n```\n\nTime Complexity: O(N log log N). Space Complexity: O(N) boolean array.",
        "kp": ["Marks multiples of primes starting from `p * p`", "Loop runs until `p * p <= n`", "Time Complexity: O(N log log N) almost linear", "Space Complexity: O(N) boolean array"],
        "cm": ["Starting multiple marking at `2*p` instead of `p*p`, doing redundant work already completed by smaller primes", "Checking primes independently using trial division for each number up to N (O(N * sqrt(N)) slow)", "Allocating list of primes dynamically instead of using fixed-size boolean lookup table"],
        "fu": ["What is a Segmented Sieve and how does it find primes in a range `[L, R]` with O(sqrt(R)) memory?", "Why does the inner loop start at `p * p` instead of `2 * p`?"]
    },
    {
        "q": "Explain the Tower of Hanoi mathematical puzzle. Write a recursive Python solution and state its complexity.",
        "sub": "Recursion",
        "d": "Intermediate",
        "ans": "The Tower of Hanoi consists of three rods (Source, Target, Auxiliary) and N disks of different sizes. Rules: 1) Move one disk at a time, 2) Only the top disk can be moved, 3) No disk may be placed on top of a smaller disk. Recursive strategy: to move N disks from Source to Target: a) Move N-1 disks from Source to Auxiliary, b) Move N-th (largest) disk directly from Source to Target, c) Move N-1 disks from Auxiliary to Target:\n\n```python\ndef tower_of_hanoi(n: int, source: str, target: str, auxiliary: str) -> None:\n    if n == 1:\n        print(f\"Move disk 1 from {source} to {target}\")\n        return\n    tower_of_hanoi(n - 1, source, auxiliary, target)\n    print(f\"Move disk {n} from {source} to {target}\")\n    tower_of_hanoi(n - 1, auxiliary, target, source)\n```\nTotal moves required: `2^N - 1`. Time Complexity: O(2^N) exponential. Space Complexity: O(N) call stack depth.",
        "kp": ["Divide problem into three recursive steps", "Base case: `n == 1` moves single disk directly to target", "Total moves required is strictly `2^N - 1`", "Time Complexity: O(2^N); Space Complexity: O(N) call stack"],
        "cm": ["Confusing target and auxiliary rods in the second recursive call", "Forgetting the base case n=1", "Attempting to solve for N > 30, which requires billions of operations"],
        "fu": ["How do you prove that the minimum number of moves is `2^N - 1` using mathematical induction?", "Can Tower of Hanoi be solved iteratively using binary Gray codes?"]
    },
    {
        "q": "Write a Python function to calculate `pow(x, n)` (x raised to the power n) in O(log n) time using Binary Exponentiation.",
        "sub": "Mathematical Algorithms",
        "d": "Intermediate",
        "ans": "Naive multiplication `x * x * ... * x` takes O(n) time. Binary Exponentiation (Exponentiation by Squaring) computes `x^n` in O(log n) time using properties: if n is even, `x^n = (x^2)^(n/2)`; if n is odd, `x^n = x * (x^2)^((n-1)/2)`:\n\n```python\ndef my_pow(x: float, n: int) -> float:\n    if n < 0:\n        x = 1 / x\n        n = -n\n    result = 1.0\n    current_product = x\n    while n > 0:\n        if n % 2 == 1:\n            result *= current_product\n        current_product *= current_product\n        n //= 2\n    return result\n```\n\nSample Input: `x = 2.0, n = 10` -> Output: `1024.0`. Sample Input: `x = 2.0, n = -2` -> Output: `0.25`. Handles negative exponents and `n=0`. Time Complexity: O(log n). Space Complexity: O(1) iterative.",
        "kp": ["Binary exponentiation squares the base and halves the exponent at each step", "Reduces multiplications from O(n) linear to O(log n) logarithmic", "Handles negative exponents by inverting base `x = 1/x` and `n = -n`", "Iterative implementation runs in O(1) auxiliary space"],
        "cm": ["Linear loop multiplying x by itself n times (too slow for large n)", "Not handling negative exponents (e.g., 2^-2 = 0.25)", "Integer overflow in languages without arbitrary precision (use modular exponentiation)"],
        "fu": ["What is Modular Exponentiation `(x^n) % m` and why is it foundational in RSA cryptography?", "How does Python's built-in `pow(x, n, m)` execute modular exponentiation efficiently in C?"]
    },
    {
        "q": "Write a Python function to compute the sum of digits of a non-negative integer iteratively and recursively.",
        "sub": "Basic Algorithms",
        "d": "Beginner",
        "ans": "To compute digit sum: extract the last digit using modulo 10 (`n % 10`) and strip it using integer division (`n // 10`) until n becomes 0. 1) Iterative:\n\n```python\ndef sum_of_digits(n: int) -> int:\n    total = 0\n    n = abs(n)\n    while n > 0:\n        total += n % 10\n        n //= 10\n    return total\n```\n\n2) Recursive: `return n if n < 10 else (n % 10) + sum_of_digits(n // 10)`. Sample Input: `12345` -> Output: `15`. Time Complexity: O(d) where d is digit count (`log10(n)`). Space Complexity: O(1) iterative. Note: converting to string `sum(int(c) for c in str(n))` works in Python but allocates string memory and is slower.",
        "kp": ["Modulo 10 extracts last digit; integer division `// 10` strips last digit", "Iterative while-loop runs in O(log10(n)) time and O(1) space", "Base case for recursion: `n < 10: return n`", "Handle negative numbers using `abs(n)`"],
        "cm": ["Converting to string and summing characters when arithmetic solution was requested", "Infinite loop when input is negative without using `abs(n)`", "Confusing sum of digits with digital root (single-digit repeated sum)"],
        "fu": ["What is Digital Root and how can it be calculated in O(1) time using the modulo 9 formula?", "How do you count the total number of digits in an integer using `math.log10`?"]
    },
    {
        "q": "Explain the classic 'River Crossing Puzzle' (Farmer, Wolf, Goat, and Cabbage) and its logical state-space solution.",
        "sub": "Logical Puzzles",
        "d": "Beginner",
        "ans": "Problem: A farmer must transport a Wolf, a Goat, and a Cabbage across a river using a boat that can only carry the farmer and one item at a time. Constraints: If left alone together on either bank without the farmer, the wolf will eat the goat, or the goat will eat the cabbage. Solution (7 steps): 1) Take Goat across (Bank 1: Wolf, Cabbage; Bank 2: Goat), 2) Farmer returns alone, 3) Take Wolf across, 4) Bring Goat back to Bank 1 (preventing wolf eating goat on Bank 2), 5) Take Cabbage across (Bank 2: Wolf, Cabbage), 6) Farmer returns alone, 7) Take Goat across. All four safely reach Bank 2. In computer science, this is modeled as Breadth-First Search (BFS) over valid states in a state-space graph.",
        "kp": ["Key insight: step 4 brings the goat back to prevent conflict on Bank 2", "Goat is the critical bottleneck involved in both conflict pairs", "Model as graph search (BFS) where nodes are legal bank states", "Guarantees safety of all entities across 7 minimal transitions"],
        "cm": ["Leaving wolf and goat together on either bank without the farmer", "Forgetting that items can be brought BACK on return trips", "Trying random guessing instead of structured state-space constraint analysis"],
        "fu": ["How do you model this puzzle formally as a graph search problem in Python using BFS?", "What is the Missionaries and Cannibals puzzle and how does its state space compare?"]
    },
    {
        "q": "Explain the 3-liter and 5-liter Water Jug Puzzle to measure exactly 4 liters. What is the mathematical foundation (Bézout's identity)?",
        "sub": "Logical Puzzles",
        "d": "Intermediate",
        "ans": "Problem: You have an unmarked 3-liter jug, an unmarked 5-liter jug, and an unlimited water source. Measure exactly 4 liters. Solution: 1) Fill 5L jug completely (0, 5), 2) Pour from 5L into 3L jug until full, leaving 2L in 5L jug (3, 2), 3) Empty 3L jug (0, 2), 4) Pour the 2L from 5L jug into 3L jug (2, 0), 5) Fill 5L jug completely (2, 5), 6) Pour from 5L into 3L jug until 3L jug is full (needs 1L). The 5L jug now contains exactly 4 liters: `5 - 1 = 4L`. Mathematical foundation: Bézout's Identity states that for integers a and b, the equation `a*x + b*y = d` has integer solutions if and only if d is a multiple of `gcd(a, b)`. Since `gcd(3, 5) = 1`, any integer volume between 1 and 5 can be measured.",
        "kp": ["Step-by-step state sequence: (0,5) -> (3,2) -> (0,2) -> (2,0) -> (2,5) -> (3,4)", "Result: 4 liters left in the 5L jug", "Bézout's Identity: solvable if target volume is a multiple of gcd(jug_a, jug_b)", "Can be modeled algorithmically as BFS in a state-space graph"],
        "cm": ["Attempting to eyeball or estimate half-full jugs (violates exact constraint rules)", "Trying to measure a volume that is not a multiple of gcd(a, b)", "Failing to document each jug's volume state clearly step-by-step"],
        "fu": ["Can you measure 4 liters if the jugs were 2L and 6L? Why or why not based on GCD?", "How do you write a Python BFS function to solve arbitrary water jug problems?"]
    },
    {
        "q": "Explain the Monty Hall Probability Problem. Why should the contestant always switch doors?",
        "sub": "Probability & Logic",
        "d": "Intermediate",
        "ans": "Problem: A game show has 3 doors. Behind one door is a car (prize); behind the other two are goats. You pick Door 1. The host (Monty Hall), who knows what is behind every door, opens Door 3, revealing a goat. He asks: 'Do you want to stick with Door 1 or switch to Door 2?' Mathematical analysis: 1) When you picked Door 1, your probability of picking the car was 1/3; the probability the car was behind Door 2 or 3 was 2/3. 2) Monty Hall is constrained: he ALWAYS opens a goat door. His action does not change your initial 1/3 probability on Door 1. Instead, the entire 2/3 probability of the unchosen doors concentrates onto the remaining unopened Door 2. 3) Switching wins the car 2/3 of the time; staying wins only 1/3 of the time. You should always switch.",
        "kp": ["Initial pick probability is 1/3; unpicked doors combine to 2/3 probability", "Host's action is non-random: he always reveals a goat, concentrating 2/3 probability on the remaining door", "Switching doubles winning chances from 33.3% to 66.7%", "Classic demonstration of conditional probability and Bayes' Theorem"],
        "cm": ["Assuming it is a 50/50 coin flip because two closed doors remain (ignores host's non-random information)", "Failing to realize the host knows where the prize is and never opens the car door", "Counter-intuitive trap: human intuition equates remaining options with equal probabilities"],
        "fu": ["What happens if the host did NOT know where the car was and opened a door randomly (Monty Fall)?", "How does expanding the problem to 100 doors make the 99/100 switching logic intuitively obvious?"]
    },
    {
        "q": "What is Big-O, Big-Omega, and Big-Theta notation in asymptotic complexity analysis?",
        "sub": "Complexity Analysis",
        "d": "Beginner",
        "ans": "Asymptotic notation characterizes algorithm efficiency as input size N grows toward infinity: 1) Big-O (`O(f(N))`): Asymptotic Upper Bound. Represents the worst-case growth rate; the algorithm will perform no worse than this bound: `T(N) <= c * f(N)` for large N. 2) Big-Omega (`Omega(f(N))`): Asymptotic Lower Bound. Represents the best-case growth rate; the algorithm will perform at least this well: `T(N) >= c * f(N)`. 3) Big-Theta (`Theta(f(N))`): Asymptotic Tight Bound. Applies when upper and lower bounds coincide; the algorithm grows precisely at this rate: `c1 * f(N) <= T(N) <= c2 * f(N)`. In industry interviews, developers colloquially say 'Big-O' when they technically refer to Big-Theta tight bounds of worst-case runtime.",
        "kp": ["Big-O: upper bound (worst-case ceiling; no worse than f(N))", "Big-Omega: lower bound (best-case floor; at least f(N))", "Big-Theta: tight bound (sandwiched between bounds; grows exactly as f(N))", "Ignores constant factors and lower-order terms as N approaches infinity"],
        "cm": ["Including constant multipliers or lower-order terms (e.g., writing O(2N + 5) instead of O(N))", "Confusing worst-case time with Big-O (Big-O is a mathematical bound, not a case)", "Assuming O(1) means instantaneous (O(1) means constant operations, which could take 10 seconds)"],
        "fu": ["Why do we drop constants and lower-order terms in asymptotic analysis?", "What is Amortized Time Complexity and how does it apply to dynamic array appending?"]
    },
    {
        "q": "Explain Amortized Time Complexity with the example of dynamic array resizing (Python list `append`).",
        "sub": "Complexity Analysis",
        "d": "Intermediate",
        "ans": "Amortized analysis evaluates the average time per operation over a long sequence of operations, accounting for rare, expensive operations balanced by frequent, cheap operations. Dynamic Array Example (Python list / C++ std::vector): appending to an array with spare capacity takes O(1) time. When capacity is full, appending triggers a resize: 1) Allocate a new array double the capacity (2X), 2) Copy all N elements over (O(N) cost), 3) Append the new element. Although the resize operation takes O(N), it happens very infrequently (after 1, 2, 4, 8, 16... inserts). Averaged across all N inserts, total work is `N (cheap inserts) + 2N (copies) = 3N` operations, yielding `3N / N = O(1)` amortized time per append.",
        "kp": ["Amortized analysis averages cost over a sequence of operations", "Python list `append()` is O(1) amortized, but occasionally O(N) worst-case during resize", "Geometric doubling (e.g., 2X capacity) guarantees O(1) amortized cost", "Arithmetic expansion (e.g., adding +10 slots) degrades amortized append to O(N)"],
        "cm": ["Claiming dynamic array append is strictly O(1) worst-case (it is O(N) worst-case during resize)", "Thinking fixed-amount resizing (+100 items) is as efficient as doubling (it causes quadratic O(N^2) total time)", "Confusing average-case complexity with amortized complexity"],
        "fu": ["What would be the amortized time if a dynamic array resized by adding 100 fixed slots instead of doubling?", "How does Python list over-allocation strategy work in CPython (`list_resize`)?"]
    },
    {
        "q": "What is the difference between Time Complexity and Space Complexity? What is Auxiliary Space?",
        "sub": "Complexity Analysis",
        "d": "Beginner",
        "ans": "1) Time Complexity: quantifies the number of basic operations (comparisons, arithmetic steps) executed by an algorithm as a function of input size N. 2) Space Complexity: quantifies the total memory required by the algorithm during execution, including input data storage. 3) Auxiliary Space: the extra or temporary memory allocated by the algorithm EXCLUDING the space taken by the input data itself. In interview coding, 'space complexity' almost always refers to Auxiliary Space. Example: finding the maximum element in an array of size N requires O(N) input space, but O(1) auxiliary space because it only uses a single tracking variable.",
        "kp": ["Time Complexity measures operation count growth relative to input size N", "Space Complexity measures total memory consumption", "Auxiliary Space measures strictly extra temporary memory beyond input data", "Recursive call stacks consume auxiliary space proportional to recursion depth"],
        "cm": ["Counting input data memory as auxiliary space", "Forgetting call stack frames in recursive algorithms when calculating space complexity", "Assuming memory allocation inside loops gets garbage collected instantly without peak memory overhead"],
        "fu": ["What is an 'in-place' algorithm and what auxiliary space does it typically require?", "Why does recursive tree traversal have O(h) auxiliary space where h is tree height?"]
    },
    {
        "q": "How do you detect and fix an off-by-one error (OBOE) in array iteration loops?",
        "sub": "Debugging & Code Quality",
        "d": "Beginner",
        "ans": "An Off-By-One Error (OBOE) occurs when a loop iterates one time too many or one time too few, typically caused by incorrect boundary operators (`<` vs `<=`) or misunderstanding zero-based indexing. Classic manifestations: 1) `IndexError: list index out of range` when accessing `arr[len(arr)]` instead of `arr[len(arr) - 1]`, 2) Skipping the final boundary element by using `<` instead of `<=`, and 3) Range mismatches in Python's half-open intervals `range(start, stop)` where `stop` is exclusive. Debugging strategy: test boundary values (n=0, n=1, n=2, and last element), verify half-open interval conventions, and prefer pythonic iterators `for item in arr:` or `enumerate()` over manual index manipulation.",
        "kp": ["OBOE: loop executes one iteration too many or too few", "Zero-based indexing: valid indices for length N are `0` through `N-1`", "Python `range(start, stop)` is half-open: includes start, excludes stop", "Test boundary conditions: empty input, single element, first and last indices"],
        "cm": ["Accessing `arr[len(arr)]` (raises IndexError)", "Writing `range(0, len(arr) - 1)` when intending to visit all elements", "Using `<=` on length checks in 0-based indexing: `i <= len(arr)`"],
        "fu": ["Why does computer science widely favor half-open intervals `[start, end)` over closed intervals?", "How does `enumerate(arr)` eliminate manual index off-by-one errors in Python?"]
    },
    {
        "q": "What is the 25-Horse Race Puzzle? What is the minimum number of races needed to find the top 3 fastest horses?",
        "sub": "Logical Puzzles",
        "d": "Intermediate",
        "ans": "Problem: 25 horses, a 5-lane track (max 5 horses per race), and no stopwatch (you only learn relative finish order). Find the top 3 fastest horses. Solution (7 races total): 1) Races 1-5: divide 25 horses into 5 groups of 5. Race each group. Order horses within each group A1>A2>A3>A4>A5, B1>B2... E1>E2... Discard 4th and 5th horses from all groups (they cannot be top 3). 15 horses remain. 2) Race 6: race the 5 group winners (A1, B1, C1, D1, E1). Suppose order is A1 > B1 > C1 > D1 > E1. A1 is guaranteed the overall #1 fastest horse! D and E groups are eliminated entirely. C2 and C3 are eliminated (since C1 was 3rd). B3 is eliminated. 3) Race 7: race remaining contenders for 2nd and 3rd: {A2, A3, B1, B2, C1}. Top 2 finishers in Race 7 are the overall #2 and #3 horses. Exactly 7 races.",
        "kp": ["Races 1-5 determine intra-group rankings; eliminate bottom 2 of each group", "Race 6 races group winners; identifies #1 fastest horse (A1) and eliminates D & E groups", "Deduce remaining contenders: only A2, A3, B1, B2, C1 can possibly be 2nd or 3rd", "Race 7 among the 5 remaining candidates determines #2 and #3 horses"],
        "cm": ["Assuming 6 races are sufficient (Race 6 alone cannot order A2 vs B1)", "Racing eliminated horses that mathematically cannot be in the top 3", "Forgetting that A1 is already confirmed #1 and does not need to run in Race 7"],
        "fu": ["How would the solution change if you needed to find the top 5 fastest horses?", "How does this logic apply to tournament tree selection in computer algorithms?"]
    },
    {
        "q": "How do you detect memory leaks in long-running Python programs using `tracemalloc`?",
        "sub": "Debugging & Profiling",
        "d": "Intermediate",
        "ans": "While Python uses automatic garbage collection, memory leaks occur when unused objects remain referenced by global variables, long-lived caches, circular closures, or unclosed file descriptors. The standard library `tracemalloc` module tracks memory allocations per code line:\n\n```python\nimport tracemalloc\n\ntracemalloc.start()\n# execute suspicious workflow\nsnapshot1 = tracemalloc.take_snapshot()\n# execute workflow again\nsnapshot2 = tracemalloc.take_snapshot()\n\ntop_stats = snapshot2.compare_to(snapshot1, 'lineno')\nfor stat in top_stats[:5]:\n    print(stat)\n```\n`compare_to()` highlights lines allocating growing memory buffers across iterations, pinpointing memory leaks.",
        "kp": ["`tracemalloc` traces memory allocations back to exact source code lines", "Take snapshots before and after suspicious workflows to compare differences", "Identifies leaks caused by unbounded caches, global lists, and lingering references", "Low runtime overhead suitable for staging diagnostics"],
        "cm": ["Assuming Python cannot have memory leaks because it has a garbage collector", "Using global list accumulators without bounded eviction policies", "Ignoring unclosed connections and file descriptors that consume OS resources"],
        "fu": ["How does `gc.collect()` force garbage collection and return unreachable object counts?", "How does `objgraph` visualize object reference graphs to locate circular reference leaks?"]
    },
    {
        "q": "What is the difference between a shallow bug and a heisenbug in software engineering?",
        "sub": "Debugging Terminology",
        "d": "Beginner",
        "ans": "1) Bohrbug (Standard / Shallow Bug): a reproducible, deterministic bug that reliably manifests whenever a specific set of input conditions occurs, regardless of environment or debugging tools. Easily isolated and fixed using unit tests and debuggers. 2) Heisenbug: an elusive, non-deterministic bug that disappears or alters its behavior when an engineer attempts to observe or debug it (named after Heisenberg's Uncertainty Principle). Common causes: race conditions in multithreaded code (adding `print()` or attaching a debugger changes thread timing, hiding the race), uninitialized memory in C/C++, compiler optimizations, or timing-dependent network socket delays. Resolving heisenbugs requires non-intrusive logging, stress testing, and concurrency analysis tools.",
        "kp": ["Bohrbug: deterministic, easily reproducible with fixed inputs", "Heisenbug: disappears or mutates behavior when investigated or debugged", "Heisenbugs typically stem from race conditions, concurrency timing, or uninitialized state", "Inserting print statements or debuggers alters thread timing, masking the bug"],
        "cm": ["Assuming a bug is fixed because it stopped appearing after adding a print statement", "Relying on luck rather than thread sanitizers and concurrency stress tests", "Dismissing intermittent production crashes as 'one-time cosmic ray glitches'"],
        "fu": ["What is a Race Condition and how do Thread Sanitizers detect them automatically?", "How does asynchronous cooperative concurrency reduce multithreading heisenbugs?"]
    },
    {
        "q": "Explain the Two-Pointer technique in array algorithms. What are the opposite-directional and same-directional patterns?",
        "sub": "Algorithmic Patterns",
        "d": "Intermediate",
        "ans": "The Two-Pointer technique optimizes nested-loop O(n^2) array problems into linear O(n) time by maintaining two index pointers: 1) Opposite-Directional (Converging): pointers start at opposite ends (`left = 0`, `right = len - 1`) and move toward each other based on comparison conditions. Used on sorted arrays (Two Sum II, Container With Most Water, Palindrome verification). 2) Same-Directional (Fast & Slow / Sliding Window): both pointers move in the same direction. Fast pointer scans while slow pointer tracks write positions or window boundaries (e.g., Move Zeroes, Remove Duplicates, Longest Substring Without Repeating Characters). Pointers advance conditionally, ensuring every element is visited a constant number of times.",
        "kp": ["Transforms O(n^2) nested loop algorithms into O(n) linear passes", "Opposite-directional: converging from ends (Two Sum sorted, Palindromes)", "Same-directional: Fast/Slow pointers (Remove duplicates, Cycle detection)", "Sliding Window is a specialized variant of same-directional two-pointers"],
        "cm": ["Applying opposite-directional pointers on unsorted arrays for target sum problems", "Forgetting to advance pointers inside loops, causing infinite execution", "Off-by-one errors in pointer initialization (`right = len(arr)` instead of `len(arr) - 1`)"],
        "fu": ["How does the Sliding Window pattern differ from general two pointers?", "How does the 'Container With Most Water' algorithm decide which pointer to advance?"]
    },
    {
        "q": "What is the Sliding Window algorithmic pattern? Contrast fixed-size vs dynamic-size sliding windows.",
        "sub": "Algorithmic Patterns",
        "d": "Intermediate",
        "ans": "The Sliding Window pattern maintains a contiguous sub-range of an array or string that slides across data to track metrics (sums, character counts) in O(n) time without recomputing from scratch: 1) Fixed-Size Window: window width K is constant. Initialize sum of first K elements. As window shifts right, add the incoming element and subtract the outgoing element in O(1): `window_sum += arr[i] - arr[i - K]`. Total time is O(n) vs O(n*k) brute force (e.g., Maximum sum subarray of size K). 2) Dynamic-Size Window: window expands by advancing right pointer until a condition is satisfied or violated, then contracts by advancing left pointer until condition restores (e.g., Smallest subarray with sum >= S, Longest substring with K distinct characters).",
        "kp": ["Fixed-size: add incoming element and subtract outgoing element in O(1)", "Dynamic-size: expand right pointer, contract left pointer based on condition", "Avoids redundant recalculations, reducing quadratic O(n^2) to linear O(n)", "Common auxiliary data structures: hash map or Counter to track window state"],
        "cm": ["Recalculating window sum from scratch on every step, degrading back to O(n*k)", "Not shrinking dynamic window correctly when constraint is violated", "Off-by-one errors when subtracting the outgoing element (`arr[i - k]`)"],
        "fu": ["How do you solve 'Longest Substring Without Repeating Characters' using a dynamic sliding window?", "When is a Monotonic Deque used with sliding windows (Sliding Window Maximum)?"]
    },
    {
        "q": "How do you systematically analyze and prove the Time and Space Complexity of a recursive algorithm?",
        "sub": "Complexity Analysis",
        "d": "Intermediate",
        "ans": "To analyze recursive complexity: 1) Formulate Recurrence Relation: express runtime `T(n)` in terms of subproblem sizes and non-recursive work. E.g., Merge Sort: `T(n) = 2*T(n/2) + O(n)`. 2) Solve Recurrence: a) Master Theorem: for `T(n) = a*T(n/b) + O(n^d)`, compare `log_b(a)` to `d`. If equal, `T(n) = O(n^d * log n)`. b) Recursion Tree Method: visualize call tree, compute work done per level, and sum across all tree levels (`height * work_per_level`). 3) Space Complexity: maximum depth of the recursion tree on the call stack multiplied by memory allocated per frame (e.g., O(n) for linear recursion, O(log n) for balanced divide-and-conquer). Memoization adds auxiliary cache memory.",
        "kp": ["Formulate recurrence relation: `T(n) = a*T(n/b) + f(n)`", "Solve using Master Theorem or Recursion Tree method", "Space complexity equals maximum call stack depth plus auxiliary allocations", "Balanced binary divide-and-conquer has call stack depth O(log n)"],
        "cm": ["Assuming number of recursive calls equals time complexity without multiplying by work per call", "Ignoring call stack memory when stating space complexity of recursive functions", "Applying Master Theorem on non-divide-and-conquer recurrences (like Fibonacci)"],
        "fu": ["What are the three cases of the Master Theorem?", "How does the Akra-Bazzi method generalize the Master Theorem for unequal subproblem partitions?"]
    }
]

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    f1 = OUT_DIR / "01.json"
    f2 = OUT_DIR / "02.json"
    f1.write_text(json.dumps(PART1, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    f2.write_text(json.dumps(PART2, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(PART1)} to 01.json, {len(PART2)} to 02.json (Total: {len(PART1) + len(PART2)})")

if __name__ == "__main__":
    main()
