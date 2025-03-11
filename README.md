# databricks-mcp

Experimental [MCP](https://modelcontextprotocol.io/introduction) server for working with the [Databricks API](https://docs.databricks.com/api/workspace/introduction)

## Developing

This project is managed with [uv](https://github.com/astral-sh/uv). Once you have `uv` installed:

### Environment

Copy `server/example.env` to `server/.env`. Record your Databricks workspace URL as `DATABRICKS_API_HOST`. Allocate a PAT in Databricks by going to your user settings, then under "Developer", click "Manage" under access tokens. Record that token in `server/.env` as `DATABRICKS_API_TOKEN`.

```
uv sync
uv run server/databricks.py
```

### Debugging 

You can run the inspector using `npx` with this command (assuming you're running from the project directory).

```
npx @modelcontextprotocol/inspector uv --directory $PWD/server run databricks.py 
```
