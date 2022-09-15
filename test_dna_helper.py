import pytest

from dna_helper import new_dna, combine_dna


@pytest.mark.parametrize('base,size', [('abcdefgh', 2), ('a', 9)])
def test_new_dna(base, size):
    dna = new_dna(base, size)
    assert len(dna) == size
    assert all([b in base for b in dna])


@pytest.mark.parametrize('dna1,dna2', [('abcdefgh', 'ijklmnop'), ('a', 'b')])
def test_combine_dna(dna1, dna2):
    dna = combine_dna(dna1, dna2, len(dna1))
    assert len(dna) == len(dna1)
    assert all([b in dna1 or b in dna2 for b in dna])
