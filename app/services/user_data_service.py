from app.infraestructure.github.client import GithubClient
from app.infraestructure.github.queries import GET_USER_DATA

"""
Service for fetching and processing user data from GitHub.

Classes:
    UserDataService: Provides methods to fetch user data and summarize programming language usage.

Methods:
    __init__(github_client: GithubClient)
        Initializes the service with a GitHub client.

    async fetch_user_data(username: str) -> dict
        Fetches user data from GitHub for the specified username.

    get_language_resume(payload: dict) -> list[dict]
        Summarizes the total size of code written in each programming language across the user's repositories.

Args:
    github_client (GithubClient): An instance of the GitHub client used to execute queries.
    username (str): The GitHub username to fetch data for.
    payload (dict): The user data payload containing repository and language information.

    dict: User data fetched from GitHub.
    list[dict]: A list of dictionaries, each containing a language and its total size, sorted by size in descending order.
"""
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
