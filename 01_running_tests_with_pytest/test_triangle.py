import pytest
from triangle import area_of_a_triangle

def test_float_values():
    """ Test areas when values are floats """
    assert area_of_a_triangle(2.3, 5.7) == 6.555

def test_integer_values():
    """ Test areas when values are integers """
    assert area_of_a_triangle(4, 6) == 12.0

def test_zero_base():
    """ Test areas when base is zero """
    assert area_of_a_triangle(0, 5) == 0.0

def test_zero_height():
    """ Test areas when height is zero """
    assert area_of_a_triangle(2, 0) == 0.0

def test_zero_values():
    """ Test areas when base and height are zero """
    assert area_of_a_triangle(0, 0) == 0.0

def test_negative_base():
    """ Test that ValueError is raised when base is negative """
    with pytest.raises(ValueError, match="Base must be a positive number"):
        area_of_a_triangle(-5, 10)

def test_negative_height():
    """ Test that ValueError is raised when height is negative """
    with pytest.raises(ValueError, match="Height must be a positive number"):
        area_of_a_triangle(5, -10)

def test_with_boolean():
    """ Test that TypeError is raised with boolean types """
    with pytest.raises(TypeError, match="Base must be a number"):
        area_of_a_triangle(True, 10)
    with pytest.raises(TypeError, match="Height must be a number"):
        area_of_a_triangle(2, False)

def test_with_string():
    """ Test that TypeError is raised with string types """
    with pytest.raises(TypeError, match="Base must be a number"):
        area_of_a_triangle("base", 10)
    with pytest.raises(TypeError, match="Height must be a number"):
        area_of_a_triangle(2, "height")

def test_with_nulls():
    """ Test that TypeError is raised with null types """
    with pytest.raises(TypeError, match="Base must be a number"):
        area_of_a_triangle(None, 10)
    with pytest.raises(TypeError, match="Height must be a number"):
        area_of_a_triangle(2, None)

def test_with_collections():
    """ Test that TypeError is raised with collection types """
    with pytest.raises(TypeError, match="Base must be a number"):
        area_of_a_triangle((1, 2), 10)
    with pytest.raises(TypeError, match="Height must be a number"):
        area_of_a_triangle(2, [1, 2])

