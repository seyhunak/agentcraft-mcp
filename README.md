# AgentCraft MCP Server

## Overview

AgentCraft is a partner product of Crafted™. Our AI Agent framework allows you to deploy intelligent agents that understand, learn, and evolve with your business needs. It provides premade and custom AI agents for enterprises, ensuring secure and scalable solutions.

This MCP server integrates with **AgentCraft**, allowing AI Agents to interact and exchange data securely.

## Features

- Secure AI agent communication and data exchange.
- Supports premade and custom AI agents.
- Scalable and enterprise-ready architecture.
- Supports Windsurf MCP client.
- Example integrations for Cline and 5ire MCP clients.

## Installation

### Using Distributed `pip` (Recommended)

```bash
pip install agentcraft-mcp
```

### Using `pip`

```bash
pip install -e .
pip list | grep agentcraft-mcp
```

If agentcraft-mcp isn't listed, reinstall using:

Then, run:

```bash
python -m agentcraft_mcp.server
```

### Configuration

Usage with Claude Desktop
Add this to your claude_desktop_config.json:

```json
{
  "mcpServers": {
      "AgentCraft": {
          "command": "python",
          "args": [
              "-m",
              "agentcraft_mcp.server"
          ],
          "env": {
              "AGENTCRAFT_BEARER_TOKEN": "Your AgentCraft Bearer Token for authorization",
              "ENVIRONMENT": "PRODUCTION"
          }
      }
  }
}
```

##### Available Tools

1. send_agent_data
Description: Send data to an agent.

Input:
```bash
{  
    "prompt": "Your message here"
}
```

2. receive_agent_data
Description: Receive data from an agent.
Input:
```bash
{
  "query": "Your query",
  "tracking_key": "Your tracking key",
  "response_type": "markdown"
}
```

3. get_available_agents
Description: Get a list of available agents.
```bash
Input: None
```

### License
AgentCraft MCP Server is licensed under Crafted company.

### Contact
For more information, visit AgentCraft GitHub website or we-crafted.com website.