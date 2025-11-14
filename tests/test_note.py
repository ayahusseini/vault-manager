"""Tests implementation of the note object"""
import unittest
import pytest
from vault_manager.note_graph import Note
from unittest.mock import MagicMock, mock_open, patch


@pytest.mark.parametrize(
    "raw_name, expected_name",
    [
        ("Note One.md", "note one"),
        ("Another_Note.md", "another_note"),
        ("Third-Note.markdown", "third-note"),
        (r"some/folder/example.md", "example"),
        (r"some/folder/example", "example")
    ]
)
def test_note_name_normalization(raw_name, expected_name):
    """Test that note names are normalized correctly."""
    normalized_name = Note.normalise_name(raw_name)
    assert normalized_name == expected_name

def test_lazy_loading_of_note_content(sample_markdown_note):
    """Test that note content is loaded lazily."""
    mock_filepath = "test_note.md"
    
    with patch("builtins.open", mock_open(read_data=sample_markdown_note)):
        note = Note(mock_filepath, "test note")
        assert not note._content_loaded
        tags = note.tags
        assert note._content_loaded
        assert set(tags) == {"tag1", "tag2", "tag3", "tag4"}
        assert note.is_topic is False
        assert set(note.raw_links) == {"ref1", "ref2", "topic1", "topic2"}
        
def test_lazy_loading_of_topic_note_content(sample_topic_markdown_note):
    """Test that note content is loaded lazily."""
    mock_filepath = "test_note.md"
    
    with patch("builtins.open", mock_open(read_data=sample_topic_markdown_note)):
        note = Note(mock_filepath, "test note")
        assert not note._content_loaded
        tags = note.tags
        assert note._content_loaded
        assert set(tags) == {"tag1", "tag2", "topic"}
        assert note.is_topic
        assert note.raw_links == []