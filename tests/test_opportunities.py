import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.main import app
from app.database.models.base import Base
from app.core.config import get_settings

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/crm_db_test"

engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(autouse=True, scope="session")
def setup_test_db():
    async def _setup():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    import asyncio
    asyncio.get_event_loop().run_until_complete(_setup())


@pytest.fixture
async def db_session():
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_create_opportunity(client: AsyncClient):
    payload = {
        "company_name": "Test Corp",
        "contact_name": "Test User",
        "contact_email": "test@testcorp.com",
        "opportunity_name": "Test Opportunity",
        "description": "A test opportunity",
        "estimated_value": 50000.0,
        "currency": "USD",
        "stage": "Lead nuevo",
        "priority": "Media",
        "probability": 20,
        "owner": "Test Owner",
    }
    response = await client.post("/api/v1/opportunities", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["company_name"] == "Test Corp"
    assert data["opportunity_name"] == "Test Opportunity"
    assert data["is_active"] is True


@pytest.mark.asyncio
async def test_list_opportunities(client: AsyncClient):
    response = await client.get("/api/v1/opportunities")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "skip" in data
    assert "limit" in data


@pytest.mark.asyncio
async def test_update_opportunity(client: AsyncClient):
    create_payload = {
        "company_name": "Update Corp",
        "contact_name": "Update User",
        "contact_email": "update@testcorp.com",
        "opportunity_name": "Update Opportunity",
        "stage": "Contactado",
        "priority": "Alta",
        "probability": 50,
    }
    create_response = await client.post("/api/v1/opportunities", json=create_payload)
    assert create_response.status_code == 201
    opp_id = create_response.json()["id"]

    update_payload = {
        "stage": "Negociación",
        "priority": "Crítica",
        "probability": 75,
    }
    update_response = await client.put(f"/api/v1/opportunities/{opp_id}", json=update_payload)
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["stage"] == "Negociación"
    assert data["priority"] == "Crítica"
    assert data["probability"] == 75


@pytest.mark.asyncio
async def test_delete_opportunity(client: AsyncClient):
    create_payload = {
        "company_name": "Delete Corp",
        "contact_name": "Delete User",
        "contact_email": "delete@testcorp.com",
        "opportunity_name": "Delete Opportunity",
        "stage": "Lead nuevo",
        "priority": "Baja",
        "probability": 10,
    }
    create_response = await client.post("/api/v1/opportunities", json=create_payload)
    assert create_response.status_code == 201
    opp_id = create_response.json()["id"]

    delete_response = await client.delete(f"/api/v1/opportunities/{opp_id}")
    assert delete_response.status_code == 204

    get_response = await client.get(f"/api/v1/opportunities/{opp_id}")
    assert get_response.status_code == 404
