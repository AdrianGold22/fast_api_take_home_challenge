from fastapi.testclient import TestClient
from app.main import app as fast_api
from sqlmodel import Session, SQLModel, create_engine
from app.routers.deps.db_session import get_db
from sqlmodel.pool import StaticPool 
import pytest
import app.models
from app.models.user import User

#client = TestClient(app)

@pytest.fixture(name="session")  
def session_fixture():  
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session  

@pytest.fixture(name="client")  
def client_fixture(session: Session):  
    def get_session_override():  
        return session

    fast_api.dependency_overrides[get_db] = get_session_override  

    client = TestClient(fast_api)  
    yield client  
    fast_api.dependency_overrides.clear()

def test_create_hero(session: Session, client: TestClient):
        user1 = User(username="adriangold",email="adrian@gmail.com",password="12345678", pokemonId=[1,2])
        session.add(user1)
        session.commit()
        response = client.get(
            "/users/"
        )
        data = response.json()

        assert response.status_code == 200
        assert data[0]["username"] == "adriangold"
        assert data[0]["email"] == "adrian@gmail.com"
     


        
