# MCP Setup Guide - Context7

## Overview

Context7 MCP (Model Context Protocol) server is configured for this project to provide up-to-date, version-specific documentation and code examples directly in Claude Code prompts.

## What is Context7?

Context7 eliminates outdated code generation by fetching the latest official documentation for any library or framework you're working with. Instead of relying on Claude's training data (which may be outdated), Context7 pulls real-time documentation and injects it into the context.

## Current Configuration

**Status:** ✅ Installed and Connected

**Scope:** Local config (private to your machine in this project)

**Command:** `npx -y @upstash/context7-mcp`

**Type:** stdio MCP server

## How to Use Context7

### Basic Usage

Simply add "use context7" to any prompt where you need up-to-date library documentation:

```
Example 1: Create a FastAPI endpoint with async MongoDB queries. use context7

Example 2: Implement Flutter BLoC state management with Equatable. use context7

Example 3: Set up Firebase Authentication in Flutter with Google Sign-In. use context7
```

### When to Use Context7

✅ **Use Context7 when:**
- Setting up a new library or framework
- Writing code that uses specific APIs or methods
- Need version-specific syntax or configuration
- Working with recently updated libraries
- Debugging integration issues with external packages

❌ **Not needed for:**
- General programming questions
- Project-specific business logic
- Code refactoring without library changes
- Simple debugging tasks

## Benefits for This Project

### Backend (FastAPI - be_enzo_english_test/)
- **FastAPI**: Latest async/await patterns, dependency injection, response models
- **Pydantic**: Current validation syntax and field types
- **Motor (MongoDB)**: Async MongoDB operations and aggregation pipelines
- **Firebase Admin SDK**: Latest authentication and token verification APIs
- **OpenAI API**: Current chat completion and streaming APIs

### Frontend (Flutter - flutter_enzo_english_test/ - planned)
- **Flutter SDK**: Latest widget APIs and best practices
- **flutter_bloc**: Current BLoC patterns and state management
- **GoRouter**: Latest navigation and routing syntax
- **GetIt**: Dependency injection setup
- **Dio**: HTTP client configuration and interceptors
- **Firebase Auth**: Authentication flows and Google Sign-In

## Installation for Team Members

If other developers need to set up Context7 on their machines:

```bash
# Navigate to project root
cd C:\Users\chaud\cdthong\thesis_projects

# Add Context7 MCP server
claude mcp add context7 -- npx -y @upstash/context7-mcp

# Verify installation
claude mcp list
```

## Verification Commands

```bash
# List all configured MCP servers
claude mcp list

# Check Context7 details and status
claude mcp get context7

# Remove Context7 (if needed)
claude mcp remove context7 -s local
```

## Advanced: Project-Wide Configuration (Optional)

To share MCP configuration with the entire team, create `.mcp.json` in project root:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    }
  }
}
```

**Note:** Individual developers still need Node.js v18+ installed.

## Getting an API Key (Optional)

Context7 works without an API key, but you can get higher rate limits with a free account:

1. Visit https://upstash.com/context7
2. Sign up for a free account
3. Get your API key
4. Add it to the configuration:

```bash
claude mcp add context7 --env CONTEXT7_API_KEY=your_key_here -- npx -y @upstash/context7-mcp
```

## Troubleshooting

### Context7 not responding
```bash
# Check server status
claude mcp get context7

# Restart Claude Code
# Or remove and re-add the server
claude mcp remove context7 -s local
claude mcp add context7 -- npx -y @upstash/context7-mcp
```

### Node.js not found
- Ensure Node.js v18+ is installed: `node --version`
- Add Node.js to your PATH environment variable

### Rate limits exceeded
- Get a free API key from https://upstash.com/context7
- Add the key to your configuration (see above)

## Examples for This Project

### Backend Example
```
Prompt: "Create a FastAPI router for user folder CRUD operations with:
- GET /api/v1/folders (list all folders for user)
- POST /api/v1/folders (create new folder)
- PUT /api/v1/folders/{id} (update folder)
- DELETE /api/v1/folders/{id} (delete folder)
Use MongoDB with Motor async driver and Pydantic models. use context7"
```

### Frontend Example
```
Prompt: "Create a Flutter BLoC for folder management with:
- Events: LoadFoldersEvent, CreateFolderEvent, UpdateFolderEvent, DeleteFolderEvent
- States: FolderInitial, FolderLoading, FolderSuccess, FolderError
- Use Equatable for state comparison
- Follow clean architecture with repository pattern
use context7"
```

## Support

- Context7 Documentation: https://github.com/upstash/context7
- Model Context Protocol: https://modelcontextprotocol.io/
- Claude Code MCP Docs: https://docs.claude.com/en/docs/claude-code/mcp

---

**Last Updated:** October 1, 2025
**Installed By:** Project setup
**Status:** Active
