import pytest

from vault_manager.pattern_extractor import extract_all_tags, extract_all_headings, extract_all_links

from unittest.mock import MagicMock


def test_extract_all_links_with_alias():
    extracted = extract_all_links("[[raw link|displayname]]")
    expected = {"raw link"}
    assert extracted == expected


def test_extract_all_links_with_heading():
    extracted = extract_all_links("[[sql_examples_readme#heading]]")
    expected = {"sql_examples_readme"}
    assert extracted == expected


@pytest.mark.parametrize("raw,expected",
                         [
                             ("[[Screenshot 2025-09-01 at 14.28.54.png]]", set()),
                             ("[[Screenshot 2025-09-01 at 14.28.54.png|image]]", set()),
                             ("[[document.excalidraw]]", set()),
                             ('16.52.40.excalidraw.md#^frame=XiQ60UahlYbEeW4fwgAuT', set()),
                             ("[[note title with a fullstop.]]",
                              {"note title with a fullstop."}),
                             ("[[note title with a fullstop. and some text|alias]]",
                              {"note title with a fullstop. and some text"}),
                         ])
def test_extract_all_links_ignores_non_markdown_files(raw, expected):
    extracted = extract_all_links(raw)
    assert extracted == expected


def test_extract_all_links(sample_markdown_note):
    extracted = extract_all_links(sample_markdown_note)
    expected = {"ref1", "ref2", "topic1", "topic2"}
    assert extracted == expected


def test_extract_all_tags(sample_markdown_note):
    extracted = extract_all_tags(sample_markdown_note)
    expected = {"tag1", "tag2", "tag3", "tag4"}
    assert extracted == expected


def test_extract_all_headings(sample_markdown_note):
    extracted = extract_all_headings(sample_markdown_note)
    expected = {"Title", "Content"}
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
def test_extract_all_tags_edge_cases(note, expected):
    extracted = extract_all_tags(note)
    assert extracted == expected
