class ShippingPackage:
    """A class representing a shipping package with dimensions and mass."""
    
    def __init__(self, width, height, length, mass):
        """
        Initialize a shipping package with dimensions and mass.
        
        Args:
            width: The width of the package
            height: The height of the package
            length: The length of the package
            mass: The mass/weight of the package
        """
        self._width = width
        self._height = height
        self._length = length
        self._mass = mass
    
    @property
    def width(self):
        """Get the width of the package."""
        return self._width
    
    @property
    def height(self):
        """Get the height of the package."""
        return self._height
    
    @property
    def length(self):
        """Get the length of the package."""
        return self._length
    
    @property
    def mass(self):
        """Get the mass of the package."""
        return self._mass
    
    def is_bulky(self):
        """Determine if the package is considered bulky.
        
        A package is considered bulky if any of its dimensions exceed 100 units.
        
        Returns:
            True if the package is bulky, False otherwise.
        """
        return any(dim > 150 for dim in (self._width, self._height, self._length)) or self._width * self._height * self._length >= 1_000_000
    
    def is_heavy(self):
        """Determine if the package is considered heavy.
        
        A package is considered heavy if its mass exceeds 20 units.
        
        Returns:
            True if the package is heavy, False otherwise.
        """
        return self._mass > 20
    
    def sort(self):
        """Return a tuple of the package dimensions sorted in ascending order."""
        if self.is_bulky() and self.is_heavy():
            return "REJECT"
        elif self.is_bulky() or self.is_heavy():
            return "SPECIAL"
        else:
            return "STANDARD"
    
    def __repr__(self):
        """Return a string representation of the package."""
        return f"ShippingPackage(width={self._width}, height={self._height}, length={self._length}, mass={self._mass})"
