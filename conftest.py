from vault_manager import Note, NoteGraph
import pytest


@pytest.fixture
def mock_graph():
    """Mock NoteGraph with the following initial adjacency dict:
    {
        n1 : [n2, n3, t1]
        t1 : [n1, t0]
        t0:  []
        n2 : [n1, t1, t2]
        t2 : [n4]
        n3 : [n4, t3]
        t3 : []
        n4 : [t3]
    }
    """


@pytest.fixture
def mock_graph_undirected():
    """Mock NoteGraph after being transformed to be undirected
    {
        n1 : [n2, n3, t1]
        t1 : [n1, n2, t0]
        t0:  [t1]
        n2 : [n1, t1, t2]
        t2 : [n2, n4],
        n3 : [n1, n4, t3],
        t3 : [n3, n4]
        n4 : [n3, t3, t2]
    }
    """


@pytest.fixture
def mock_topic_graph():
    """Mock NoteGraph with the following expected topic graph (weighted)
    {
        n1 : n2, n3, t1
        n2 : n1, t1, t2
        n3 : n4, t3
        n4 : t3
    }
    """
