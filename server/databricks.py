from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
import logging
from urllib.parse import urlencode

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

dotenv_result = load_dotenv()
if not dotenv_result:
    logger.warning(".env not found or not readable")

# Initialize FastMCP server
mcp = FastMCP("databricks")

# Constants
DATABRICKS_API_ROOT = "/api/2.2/"
USER_AGENT = "databricks-mcp/1.0"

databricks_host = os.getenv("DATABRICKS_API_HOST").strip("/")
databricks_token = os.getenv("DATABRICKS_API_TOKEN")

async def make_databricks_request(url: str) -> dict[str, Any] | None:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Authorization": f"Bearer {databricks_token}",
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            await response.raise_for_status()
            return response.json()   
        except Exception as e:
            logger.error(f"Error making request to Databricks: {e}")
            return None

@mcp.tool
async def list_jobs(limit: int, name_filter: str, page_token: str) -> str:
    """
    List all jobs on a Databricks workspace
    limit: number of jobs to return
    name_filter: filter jobs by name, case insensitive
    page_token: Use next_page_token or prev_page_token returned from the previous request to list the next or previous page of jobs respectively.
    """
    params = {}
    if limit:
        params["limit"] = limit
    if name_filter:
        params["name_filter"] = name_filter
    if page_token:
        params["page_token"] = page_token

    query_string = urlencode(params)
    url = f"{databricks_host}{DATABRICKS_API_ROOT}jobs/list?{query_string}"

    result = await make_databricks_request(url)

if __name__ == "__main__":
    logger.info("Running congress API")
    mcp.run(transport="stdio")
