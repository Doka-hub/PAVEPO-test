import httpx

from app.config.settings import get_settings


def get_yandex_auth_url():
    settings = get_settings()
    base_url = "https://oauth.yandex.ru/authorize"
    return f"{base_url}?response_type=code&client_id={settings.YANDEX_CLIENT_ID}"


async def exchange_code_for_user_info(code: str):
    settings = get_settings()
    token_url = "https://oauth.yandex.ru/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": settings.YANDEX_CLIENT_ID,
        "client_secret": settings.YANDEX_CLIENT_SECRET,
    }
    async with httpx.AsyncClient() as client:
        token_response = await client.post(token_url, data=data)
        token_data = token_response.json()
        access_token = token_data.get("access_token")
        user_info_url = "https://login.yandex.ru/info"
        headers = {"Authorization": f"OAuth {access_token}"}
        user_info_response = await client.get(user_info_url, headers=headers)
        return user_info_response.json()
