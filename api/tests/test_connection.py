import pytest
from api.database import connection

def test_engine_created():
    assert connection.engine is not None
    assert str(connection.engine.url) == "sqlite:///:memory:"

def test_session_local():
    session = connection.SessionLocal()
    assert session is not None
    session.close()

def test_get_db_generator():
    gen = connection.get_db()
    db_session = next(gen)  # Pega a sessão do generator
    assert db_session is not None
    try:
        # simula uso do banco
        assert hasattr(db_session, "query")
    finally:
        # finaliza o generator, que chama db.close()
        with pytest.raises(StopIteration):
            next(gen)
