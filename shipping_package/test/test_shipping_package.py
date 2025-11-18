import pytest
import sys
from pathlib import Path

# Add src directory to path so we can import shipping_package
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from shipping_package import ShippingPackage


class TestShippingPackageIsBulky:
    """Test cases for the is_bulky method."""
    
    @pytest.mark.parametrize("width,height,length,mass,expected", [
        (151, 10, 10, 5, True),        # Bulky by width
        (10, 151, 10, 5, True),        # Bulky by height
        (10, 10, 151, 5, True),        # Bulky by length
        (100, 100, 101, 5, True),      # Bulky by volume
        (99, 100, 100, 5, False),      # Not bulky within limits
        (50, 50, 50, 5, False),        # Not bulky, all dimensions small
    ])
    def test_is_bulky(self, width, height, length, mass, expected):
        """Test is_bulky method with various package dimensions."""
        package = ShippingPackage(width=width, height=height, length=length, mass=mass)
        assert package.is_bulky() == expected



class TestShippingPackageIsHeavy:
    """Test cases for the is_heavy method."""
    
    @pytest.mark.parametrize("width,height,length,mass,expected", [
        (10, 10, 10, 21, True),        # Mass exceeds 20
        (10, 10, 10, 50, True),        # Mass significantly exceeds
        (10, 10, 10, 20, False),       # At exactly 20 (not heavy)
        (10, 10, 10, 19, False),       # Below 20
        (10, 10, 10, 1, False),        # Very light
    ])
    def test_is_heavy(self, width, height, length, mass, expected):
        """Test is_heavy method with various package masses."""
        package = ShippingPackage(width=width, height=height, length=length, mass=mass)
        assert package.is_heavy() == expected


class TestShippingPackageSort:
    """Test cases for the sort method."""
    
    @pytest.mark.parametrize("width,height,length,mass,expected", [
        (151, 10, 10, 21, "REJECT"),   # Bulky and heavy
        (100, 100, 101, 21, "REJECT"), # Volume exceeds and heavy
        (151, 10, 10, 20, "SPECIAL"),  # Bulky but not heavy
        (10, 10, 10, 21, "SPECIAL"),   # Heavy but not bulky
        (10, 10, 10, 10, "STANDARD"),  # Neither bulky nor heavy
        (50, 50, 50, 20, "STANDARD"),  # At limits (not exceeding)
    ])
    def test_sort(self, width, height, length, mass, expected):
        """Test sort method with various package characteristics."""
        package = ShippingPackage(width=width, height=height, length=length, mass=mass)
        assert package.sort() == expected
