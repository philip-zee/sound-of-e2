import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.split_string import split_string_with_padding, split_string

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

    to_print = split_string(s, w)
    print("".join(to_print))

    s = [
        ["123456789012", "1234567", "1234567890"],
        ["123", "123456789012345", "12345"],
        ["12345", "12345678901", "12"],
    ]
    w = [3, 7, 3]
    # to_print = split_string(s, w)
    # print("".join(to_print))