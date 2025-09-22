from app.infraestructure.github.client import GithubClient
from app.infraestructure.github.queries import GET_USER_DATA


class UserDataService:
    def __init__(self, github_client: GithubClient):
        self.github_client = github_client

    async def fetch_user_data(self, username: str) -> dict:
        variables = {"login": username}
        result = await self.github_client.execute_query(GET_USER_DATA, variables)
        return result["data"]["user"]

    def get_language_resume(self, payload: dict) -> list[dict]:
        language_totals = {}

        for repo in payload["repositories"]["nodes"]:
            for edge in repo["languages"]["edges"]:
                lang_name = edge["node"]["name"]
                lang_size = edge["size"]
                language_totals[lang_name] = language_totals.get(lang_name, 0) + lang_size

        # Convert list to dict and sort reverse.
        language_list = [{"language": k, "size": v} for k, v in language_totals.items()]
        language_list.sort(key=lambda x: x["size"], reverse=True)

        return language_list
