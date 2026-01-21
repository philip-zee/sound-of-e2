import math
from typing import List

"""
Suppose that you have a list s of m lists, with each s[i] containing
n nonempty strings. We want to print these strings as a table in a 
terminal. The table needs to have n columns, the kth one having width 
w[k]. Each pair of adjacent columns must be separated by a pipe 
character ('|').
 
Visualization:
 
s[0][0]  |s[0][1]  | ... |s[0][n-1]
s[1][0]  |s[1][1]  | ... |s[1][n-1]
...
s[m-1][0]|s[m-1][1]| ... |s[m-1][n-1]
 
If a string s[i][k] is longer than than the width w[k] of its column,
it will be wrapped. This means that the row of the table will span at
least ceil(len(s[i][k]) / w[k]) lines of text. For example, if you 
need to print the string 'abcdefghij' in a column of width 4, it
should look like
...|abcd|...
...|efgh|...
...|ij  |...
and so the row containing that string must span at least 3 lines of
text.
 
Given s and w, print the table. (No need to worry about space/time complexity.)
 
Examples:
Input:
s = [
  ["abc", "defgh"],
  ["ij", "klmnopq"]
]
w = [2, 5]
Output:
ab|defgh
c |     
ij|klmno
  |pq   
 
Input:
s = [
 ["123456789012", "1234567", "1234567890"],
 ["123", "123456789012345", "12345"],
 ["12345", "12345678901", "12"],
]
w = [3, 7, 3]
Output:
123|1234567|123
456|       |456
789|       |789
012|       |0  
123|1234567|123
   |8901234|45 
   |5      |   
123|1234567|12 
45 |8901   |   
"""

def split_string_with_padding(text: str, length: int, elements: int) -> List[str]:
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


def split_string(s: List[List[str]], w: List[int]) -> List[str]:
    """
    Splits and vertically aligns multiple strings into fixed-width columns.

    For each row in `s`, this function:
    - Splits each string element into chunks of width specified in `w`
    - Pads shorter chunks so all columns have equal height
    - Combines corresponding chunks across columns using '|' as a separator
    - Appends each combined line to the result list with a trailing newline

    Args:
        s (list[list[str]]): A list of rows, where each row is a list of strings
                             representing column values.
        w (list[int]): A list of integers specifying the fixed width for each column.

    Returns:
        list[str]: A list of formatted strings, each representing a single
                   line of the vertically aligned, column-formatted output.

    Notes:
        - Column heights are determined by the maximum number of chunks needed
          for any string in the row.
        - Uses `split_string_with_padding` to ensure consistent chunk sizes.
    """
    results: List[str] = []

    for row in s:
        # Determine how many vertical chunks are needed for this row
        max_len = math.ceil(
            max(len(value) / width for value, width in zip(row, w))
        )

        # Split each column into padded chunks
        column_chunks = [
            split_string_with_padding(value, width, max_len)
            for value, width in zip(row, w)
        ]

        print(column_chunks)
        # Combine chunks row by row
        for chunk_row in zip(*column_chunks):
            results.append("|".join(chunk_row) + "\n")

    return results
