from point import Point


def test_point_to_string():
    point = Point(1, 2)
    assert str(point) == "(x=1, y=2)"


def test_point_hash():
    point = Point(1, 2)
    assert hash(point) == hash((1, 2))
