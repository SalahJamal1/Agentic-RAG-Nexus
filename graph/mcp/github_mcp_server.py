import os

from fastmcp import FastMCP
import  requests
mcp=FastMCP(name="GithubMCP")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "X-GitHub-Api-Version": "2026-03-10",
}
@mcp.tool()
def get_github_repo():
    """
            Search the AI-Resume-Critiquer repository based on the user's question.
    """
    try:
        url = "https://api.github.com/repos/SalahJamal1/AI-Resume-Critiquer"

        response = requests.get(
                url,
                headers=HEADERS,
                timeout=10
            )

        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    mcp.run(transport="http",port=8080)
