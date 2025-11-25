import pytest

from vault_manager.pattern_extractor import (
    extract_all_tags,
    extract_all_headings,
    extract_all_links,
    is_rejected_extension,
)

from unittest.mock import MagicMock


def test_extract_all_links_with_alias():
    extracted = extract_all_links("[[raw link|displayname]]")
    expected = {"raw link"}
    assert extracted == expected


def test_extract_all_links_with_heading():
    extracted = extract_all_links("[[sql_examples_readme#heading]]")
    expected = {"sql_examples_readme"}
    assert extracted == expected


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("[[Screenshot 2025-09-01 at 14.28.54.png]]", set()),
        ("[[Screenshot 2025-09-01 at 14.28.54.png|image]]", set()),
        ("[[document.excalidraw]]", set()),
        ("16.52.40.excalidraw.md#^frame=XiQ60UahlYbEeW4fwgAuT", set()),
        ("[[note title with a fullstop.]]", {"note title with a fullstop."}),
        (
            "[[note title with a fullstop. and some text|alias]]",
            {"note title with a fullstop. and some text"},
        ),
        ("[[example 2025-09-01 12.48.30.excalidraw.md]]", set()),
        ("[[example 2025-09-01 12.48.30.md]]", {"example 2025-09-01 12.48.30"}),
        ("[[b vs. a]]", {"b vs. a"}),
        ("[[b .mdma]]", {"b .mdma"}),
    ],
)
def test_extract_all_links_ignores_non_markdown_files(raw, expected):
    extracted = extract_all_links(raw)
    assert extracted == expected


@pytest.mark.parametrize(
    "filename,expected",
    [
        # 1. Rejected extensions (lowercase)
        ("image.png", True),
        ("video.mp4", True),
        ("document.md", True),
        ("diagram.excalidraw", True),
        # 2. Rejected extensions (uppercase)
        ("IMAGE.PNG", True),
        ("Document.MD", True),
        # 3. Not rejected / unknown extension
        ("archive.zip", False),
        ("notes.note", False),
        ("file.mdm", False),  # similar to md but not exact
        # 4. No extension
        ("README", False),
        ("note", False),
        # 5. Dot in the middle but not extension
        ("version1.2", False),
        ("file.name", False),
        # 6. Edge case: empty string
        ("", False),
    ],
)
def test_is_rejected_extension(filename, expected):
    assert is_rejected_extension(filename) == expected


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
    "note,expected", [("", set()), ("  ", set()), (" #", set()), ("#tag", {"tag"})]
)
def test_extract_all_tags_edge_cases(note, expected):
    extracted = extract_all_tags(note)
    assert extracted == expected
