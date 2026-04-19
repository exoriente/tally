from tally.int_distribution import create_int_distribution


def test_1d6() -> None:
    dis = create_int_distribution(1, 6, int.__add__)
    assert dis.d == {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}
    assert dis.average() == 3.5


def test_2d6() -> None:
    dis = create_int_distribution(2, 6, int.__add__)
    assert dis.d == {
        2: 1,
        3: 2,
        4: 3,
        5: 4,
        6: 5,
        7: 6,
        8: 5,
        9: 4,
        10: 3,
        11: 2,
        12: 1,
    }
    assert dis.average() == 7
