import httpx
import pytest

from auth.jwt_handler import create_access_token
from models.users import Event

@pytest.fixture(scope="module")
async def access_token() -> str:
    return create_access_token("testuser@pact.com")

@pytest.fixture(scope="module")
async def mock_event() -> Event:
    new_event = Event(
        creator="testuser@packt.com",
        title="FastAPI Book Launch",
        image="https://linktomyimage.com/image.png",
        description="we will be discussing the contents of the FASTAPI book in this event.Ensure to come with your own copy to win gifts!",
        tags=["fastapi", "python", "book", "launch"],
        location="Goole Meet"
    )

    await Event.insert_one(new_event)

    yield new_event

@pytest.mark.asyncio
async def test_get_events(default_client: httpx.AsyncClient, mock_event: Event) -> None:
    response = await default_client.get("/event/")
    assert response.status_code == 200
    assert response.json()[0]["_id"] == str(mock_event.id)

@pytest.mark.asyncio
async def test_get_event(default_client: httpx.AsyncClient, mock_event: Event) -> None:
    url = f"/event/{str(mock_event.id)}"
    response = await default_client.get(url)
    assert response.status_code == 200
    assert response.json()["_id"] == str(mock_event.id)
    assert response.json()["creator"] == mock_event.creator

@pytest.mark.asyncio
async def test_post_event(default_client: httpx.AsyncClient, access_token: str) -> None:
    response = await default_client.get("/event/")

    payload = {
        "title": "FastAPI Book Launch",
        "image": "https://linktomyimage.com/image.png",
        "description": "we will be discussing the contents of the FASTAPI book in this event.Ensure to come with your own copy to win gifts!",
        "tags": ["fastapi", "python", "book", "launch"],
        "location": "Goole Meet"
    }
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    test_response = await default_client.post("/event/new", json=payload, headers=headers)

    assert test_response.status_code == 200
    assert response.json() == test_response.json()

@pytest.mark.asyncio
async def test_get_event_count(default_client: httpx.AsyncClient) -> None:
    
    response = await default_client.get("/event/")

    events = response.json()

    assert response.status_code == 200
    assert len(events) == 2

@pytest.mark.asyncio
async def test_update_event(default_client: httpx.AsyncClient, mock_event: Event, access_token: str) -> None:
    url = f"/event/{str(mock_event.id)}"
    test_payload = {
        "title": "Updated FastAPI event"
    }
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    url = f"/event/{str(mock_event.id)}"

    response = await default_client.put(url, json=test_payload, headers=headers)

    assert response.status_code == 200
    assert response.json()["title"] == test_payload["title"]

@pytest.mark.asyncio
async def test_delete_event(default_client: httpx.AsyncClient, mock_event: Event, access_token: str) -> None:
    test_response = {
        "message": "Event deleted successfully"
    }
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    url = f"/event/{str(mock_event.id)}"

    response = await default_client.delete(url, headers=headers)

    assert response.status_code == 200
    assert response.json() == test_response

@pytest.mark.asyncio
async def test_get_event_again(default_client: httpx.AsyncClient) -> None:
    url = f"/event/{str(mock_event.id)}"

    response = await default_client.get(url)

    assert response.status_code == 404
    assert response.json()["creator"] == mock_event.creator
    assert response.json()["_id"] == str(mock_event.id)