import httpx
import pytest

@pytest.mark.asyncio
async def test_sign_new_user(default_client: httpx.AsyncClient) -> None:
    payload = {
        "email": "testuser@packt.com",
        "username": "testuser",
        "password": "testpassword"
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    
    response = await default_client.post("/user/signup", json=payload, headers=headers)
    assert response.status_code == 200

@pytest.mark.asyncio
@pytest.mark.depends(on=['test_sign_new_user'])
async def test_sign_user_in(default_client: httpx.AsyncClient) -> None:
    # 회원가입된 사용자로 로그인
    payload = {
        "email": "testuser@packt.com",
        "password": "testpassword"
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    
    response = await default_client.post("/user/signin", json=payload, headers=headers)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "Bearer"