import math

def longest_repeating_substring(s: str) -> str:
    n = len(s)
    suffixes = [s[i:] for i in range(n)]
    suffixes.sort()

    def lcp(a, b):
        i = 0
        while i < min(len(a), len(b)) and a[i] == b[i]:
            i += 1
        return a[:i]

    longest = ""
    for i in range(n - 1):
        common = lcp(suffixes[i], suffixes[i + 1])
        if len(common) > len(longest):
            longest = common

    return longest


def longest_repeating_substring_lcp(s: str) -> str:
    suffixes = sorted(range(len(s)), key=lambda i: s[i:])
    longest_len = 0
    start = 0

    for i in range(len(suffixes) - 1):
        a, b = suffixes[i], suffixes[i + 1]
        length = 0
        while (a + length < len(s) and
               b + length < len(s) and
               s[a + length] == s[b + length]):
            length += 1

        if length > longest_len:
            longest_len = length
            start = a

    return s[start:start + longest_len]



from collections import deque, defaultdict

class FirstNonRepeating:
    def __init__(self):
        self.count = defaultdict(int)
        self.queue = deque()

    def process(self, char):
        self.count[char] += 1

        if self.count[char] == 1:
            self.queue.append(char)

        # Remove repeated characters from the front
        while self.queue and self.count[self.queue[0]] > 1:
            self.queue.popleft()

        return self.queue[0] if self.queue else None



def longest_unique_substring(s):
    char_map = {}  # Tracks the last seen index of each character
    max_length = 0
    start = 0
    
    for i in range(len(s)):
        print(f"B: i is {i} for {s[i]}, char_map is {char_map}, start is {start}, max_length is {max_length}")
        # If char seen before and is within the current window
        if s[i] in char_map and char_map[s[i]] >= start:
            start = char_map[s[i]] + 1
            
        char_map[s[i]] = i
        max_length = max(max_length, i - start + 1)
        print(f"E: i is {i} for {s[i]}, char_map is {char_map}, start is {start}, max_length is {max_length}")

    return max_length


def my_longest_unique_substring(s):
    chars = set()
    left = 0
    max_len = 0

    index = 0
    for c in s:
        if c in chars:
            print(f"resetting left for char {c} in pos {index} with max of {max_len}")
            left = index
            chars = set()

        chars.add(c)
        max_len = max(max_len, index - left + 1)

        index += 1

    return max_len

def split_string_with_padding(text, length, elements):
    """
    Breaks a string into a list of strings of a specified length.
    Pads the final string with spaces if it is shorter than the length.
    """
    if length <= 0:
        return [text]

    # Create the initial list of chunks
    chunks = [text[i:i + length] for i in range(0, len(text), length)]

    # Check if the last chunk needs padding
    if chunks and len(chunks[-1]) < length:
        chunks[-1] = chunks[-1].ljust(length)

    if len(chunks) < elements:
        for _ in range(elements - len(chunks)):
            chunks.append(" " * length)
    return chunks


def my_new_print(s, w):
    for i in range(len(s)):
        lengths = [len(s[i][j]) / w[j] for j in range(len(s[i]))]
        max_len = math.ceil(max(lengths))
        chunks = [split_string_with_padding(s[i][j], w[j], max_len) for j in range(len(s[i]))]
        for k in range(max_len):
            p = "|".join([chunks[j][k] for j in range(len(s[i]))])
            print(p)


if __name__ == "__main__":
    test_str = "banana"
    # print(f"The longest repeating substring in '{test_str}' is '{longest_repeating_substring(test_str)}'")
    # print(f"The longest repeating substring using LCP in '{test_str}' is '{longest_repeating_substring_lcp(test_str)}'")
    # print(f"Longest unique length: {longest_unique_substring('quoraasksandanswers')}")
    # print(f"Longest unique length: {my_longest_unique_substring('quoraasksandanswers')}")

    s = [
        ["abcde", "defgh"],
        ["ij", "klmnopq"]
    ]
    w = [2, 5]
    
# Output:
# ab|defgh
# c |     
# ij|klmno
#   |pq   
    
    my_new_print(s, w)

    s = [
        ["123456789012", "1234567", "1234567890"],
        ["123", "123456789012345", "12345"],
        ["12345", "12345678901", "12"],
    ]
    w = [3, 7, 3]
    my_new_print(s, w)


# Suppose that you have a list s of m lists, with each s[i] containing
# n nonempty strings. We want to print these strings as a table in a 
# terminal. The table needs to have n columns, the kth one having width 
# w[k]. Each pair of adjacent columns must be separated by a pipe 
# character ('|').
 
# Visualization:
 
# s[0][0]  |s[0][1]  | ... |s[0][n-1]
# s[1][0]  |s[1][1]  | ... |s[1][n-1]
# ...
# s[m-1][0]|s[m-1][1]| ... |s[m-1][n-1]
 
# If a string s[i][k] is longer than than the width w[k] of its column,
# it will be wrapped. This means that the row of the table will span at
# least ceil(len(s[i][k]) / w[k]) lines of text. For example, if you 
# need to print the string 'abcdefghij' in a column of width 4, it
# should look like
# ...|abcd|...
# ...|efgh|...
# ...|ij  |...
# and so the row containing that string must span at least 3 lines of
# text.
 
# Given s and w, print the table. (No need to worry about space/time complexity.)
 
# Examples:
# Input:
# s = [
#   ["abc", "defgh"],
#   ["ij", "klmnopq"]
# ]
# w = [2, 5]
# Output:
# ab|defgh
# c |     
# ij|klmno
#   |pq   
 
# Input:
# s = [
#  ["123456789012", "1234567", "1234567890"],
#  ["123", "123456789012345", "12345"],
#  ["12345", "12345678901", "12"],
# ]
# w = [3, 7, 3]
# Output:
# 123|1234567|123
# 456|       |456
# 789|       |789
# 012|       |0  
# 123|1234567|123
#    |8901234|45 
#    |5      |   
# 123|1234567|12 
# 45 |8901   |   