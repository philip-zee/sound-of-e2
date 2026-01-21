import pytest
from split_string import split_string_with_padding, split_string


class TestSplitStringWithPadding:
    @pytest.mark.parametrize("text,length,elements,expected", [
        # Basic case: text fits evenly
        ("ABCDEF", 2, 3, ["AB", "CD", "EF"]),
        
        # Needs padding in last chunk
        ("ABCDE", 2, 3, ["AB", "CD", "E "]),
        
        # Single character per chunk
        ("ABC", 1, 3, ["A", "B", "C"]),
        
        # Needs extra empty chunks
        ("AB", 2, 4, ["AB", "  ", "  ", "  "]),
        
        # Empty string
        ("", 2, 2, ["  ", "  "]),
        
        # Single element requested
        ("HELLO", 3, 1, ["HEL", "LO "]),
        
        # Length is 0 (edge case)
        ("ABC", 0, 2, ["ABC"]),
        
        # Already padded
        ("ABCD", 2, 2, ["AB", "CD"]),
        
        # Long string with padding
        ("ABCDEFGHIJ", 3, 4, ["ABC", "DEF", "GHI", "J  "]),
    ])
    def test_split_string_with_padding(self, text, length, elements, expected):
        result = split_string_with_padding(text, length, elements)
        assert result == expected
        # assert len(result) == elements, f"Expected {elements} elements, got {len(result)}"
        # for chunk in result:
        #     assert len(chunk) == length, f"Chunk '{chunk}' should have length {length}"


class TestSplitString:
    @pytest.mark.parametrize("s,w,expected", [
        # Basic 2x2 table
        (
            [["ab", "cde"], ["fg", "hij"]],
            [2, 3],
            # Expected: 2 rows, each with line separators
            "ab|cde\nfg|hij\n"
        ),
        
        # Single row, two columns
        (
            [["hello", "world"]],
            [3, 5],
            "hel|world\nlo |     \n"
        ),
        
        # Single row, single column
        (
            [["test"]],
            [4],
            "test\n"
        ),
        (
            [["abcde", "defgh"], ["ij", "klmnopq"]],
            [2, 5],
            "ab|defgh\ncd|     \ne |     \nij|klmno\n  |pq   \n"
        ),
    ])
    def test_split_string_basic_structure(self, s, w, expected):
        result = split_string(s, w)
        assert isinstance(result, list)
        assert len(result) > 0
        # Check that result contains strings and newlines
        assert any("\n" in str(item) or "|" in str(item) for item in result)
        assert "".join(result) == expected
    
    @pytest.mark.parametrize("s,w", [
        ([["abc", "defgh"], ["ij", "klmnopq"]], [2, 5]),
        ([["123456789012", "1234567", "1234567890"]], [3, 7, 3]),
    ])
    def test_split_string_formatting(self, s, w):
        result = split_string(s, w)
        result_str = "".join(result)
        
        # Check that pipes are present (column separators)
        assert "|" in result_str
        
        # Check that newlines are present (row separators)
        assert "\n" in result_str