import pytest


@pytest.fixture
def sample_markdown_note() -> str:
    return """
    #tag4
    ---
    #tag1 #tag2 #tag3
    
    # Title
    ---
    This is a test note.

    # Content 
    It has some content and references to [[ref1]] and [[ref2]].
    
    ---
    Topics:
    - [[topic1]]
    - [[topic2]]
    """


@pytest.fixture
def sample_topic_markdown_note() -> str:
    return """
    #topic #tag1 #tag2
    """
