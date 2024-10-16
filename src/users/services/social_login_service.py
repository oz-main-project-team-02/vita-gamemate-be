import requests


class SocialLoginService:

    client_id: str
    redirect_uri: str
    login_uri: str

    def social_login(self, context: dict = None) -> str:
        if context is not None:
            return self.basic_url() + f"&scope={context["scope"]}"

        return self.basic_url()

    def basic_url(self) -> str:
        return f"{self.login_uri}?client_id={self.client_id}&redirect_uri={self.redirect_uri}&response_type=code"


class SocialLoginCallbackService:

    grant_type: str = "authorization_code"
    content_type: str = "application/x-www-form-urlencoded"
    client_id: str
    client_secret: str
    redirect_uri: str
    token_uri: str
    profile_uri: str

    def create_token_request_data(self, code: str) -> dict:
        token_request_data = {
            "grant_type": self.grant_type,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "code": code,
        }

        return token_request_data

    def get_auth_headers(self, token_request_data: dict) -> dict:
        token_response = requests.post(
            self.token_uri,
            data=token_request_data,
            headers={"Content-type": self.content_type},
        )

        if token_response.status_code != 200:
            raise ValueError(token_response.text)

        token_json = token_response.json()
        auth_headers = {"Authorization": f"Bearer {token_json.get('access_token')}"}

        return auth_headers

    def get_user_info(self, auth_headers: dict) -> dict:
        user_info_response = requests.get(self.profile_uri, headers=auth_headers)
        user_info_data = user_info_response.json()

        return user_info_data
