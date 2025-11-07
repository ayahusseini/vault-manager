import pytest

from vault_manager.pattern_extractor import extract_all_tags

from unittest.mock import MagicMock



def test_extract_all_tags(sample_markdown_note):
    extracted = extract_all_tags(sample_markdown_note)
    expected = {"tag1", "tag2", "tag3", "tag4"}  
    assert extracted == expected


@pytest.mark.parametrize(
    "note,expected",
    [
        ("", set()),
        ("  ", set()),
        (" #", set()),
        ("#tag", {'tag'})
    ]
)
def test_extract_all_tags_edge_cases(note,expected):
    extracted = extract_all_tags(note)
    assert extracted == expected