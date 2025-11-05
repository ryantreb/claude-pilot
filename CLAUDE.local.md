# CLAUDE.local.md

Direct development guidance for quick changes without spec-driven flow.

## Core Rules

**Git:** READ-ONLY - `git status/diff/log/show/branch` ✅ | `git add/commit/push` ❌
**Python:** `uv` not pip | One-line docstrings | No inline comments | Edit > Create
**Standards:** TDD mandatory | DRY/YAGNI | Clean imports | Check diagnostics before/after
**Context:** 80% limit (160k) = MESSAGE tokens + ~35k overhead | At limit → `/remember` → `/clear`
**Evidence:** Show actual output, never claim "should work" | Tests must pass AND code must execute

## Quick Change Workflow

**For small changes (< 5 files), follow these steps:**

### 1. Initial Diagnostics & Research
- Run `getDiagnostics()` - Must start with zero errors
- Query Cipher: `ask_cipher("What do we know about X? Past implementations?")`
- Search codebase: `search_code(path="/workspaces/...", query="similar patterns")`
- Check CLAUDE.md for project conventions

### 2. TodoWrite for Tracking
- Create task list even for small changes
- Mark tasks `in_progress` when starting
- Mark `completed` ONLY when tests pass AND code executes

### 3. TDD Implementation (MANDATORY)
**RED-GREEN-REFACTOR for EVERY change:**
1. Write failing test FIRST with expected behavior
2. Run test: `uv run pytest tests/path/test.py::test_name -v` → MUST FAIL
3. Write minimal code to pass the test
4. Run test again → MUST PASS
5. Refactor if needed (keeping tests green)

**Code written before test = DELETE and restart with test**

### 4. Execute Actual Code
**CRITICAL: Don't just run tests, execute the actual program:**
- ETL: `uv run python src/main.py` → Check logs/output
- API: `curl localhost:8000/endpoint` → Check response
- CLI: `uv run python src/cli.py --args` → Check output
- Show real output, never claim "should work"

### 5. API E2E Testing (if applicable)
- Create Postman collection in `postman/collections/`
- Run: `newman run postman/collections/feature.json -e postman/environments/dev.json`

### 6. Verification
- Run all tests: `uv run pytest -m unit` then `-m integration`
- Coverage check: `uv run pytest --cov=. --cov-report=term-missing`
- Linting: `uv run ruff check . --fix` then `uv run ruff format .`
- Final diagnostics: `getDiagnostics()` → Must be clean

### 7. Store Learnings
```
ask_cipher("Store: [Feature] - Built X using Y pattern
Key files: [file:line] - [why significant]
Gotchas: [problem] → [solution]")
```


## MCP Servers Available

### Memory & Search
- **Cipher** (`mcp__cipher__ask_cipher`) - Query patterns, store learnings, project memory
- **Claude Context** (`mcp__claude-context__`) - Index & search codebase semantically
  - `index_codebase(path)` - Index for searching
  - `search_code(path, query)` - Semantic search
  - `get_indexing_status(path)` - Check index status

### Development Tools
- **IDE** (`mcp__ide__`) - VS Code integration
  - `getDiagnostics()` - Check errors/warnings
  - `executeCode(code)` - Run Python in Jupyter kernel (notebooks only)
- **Database** (`mcp__dbhub-postgres__execute_sql`) - PostgreSQL queries

### Documentation & Research
- **Ref** (`mcp__Ref__`) - Search web/GitHub docs
  - `ref_search_documentation(query)` - Find docs
  - `ref_read_url(url)` - Read content from URL
- **Context7** (`mcp__context7__`) - Library documentation
  - `resolve-library-id(libraryName)` - Get library ID
  - `get-library-docs(context7CompatibleLibraryID)` - Get docs

### Web Scraping & Search
- **Firecrawl** (`mcp__firecrawl__`) - Web scraping/search
  - `mcp__firecrawl-mcp__firecrawl_scrape(url, formats)` - Scrape single URL
  - `mcp__firecrawl-mcp__firecrawl_search(query, sources)` - Search web
  - `mcp__firecrawl-mcp__firecrawl_extract(urls, schema)` - Extract structured data
  - `mcp__firecrawl-mcp__firecrawl_map(url)` - Map website URLs
  - `mcp__firecrawl-mcp__firecrawl_crawl(url)` - Crawl website

### Tool Discovery
- **MCP Funnel** (`mcp__mcp-funnel__`) - Discover/bridge tools
  - `discover_tools_by_words(words, enable)` - Find tools
  - `get_tool_schema(tool)` - Get tool parameters
  - `bridge_tool_request(tool, arguments)` - Execute discovered tools


## When to Use This vs /plan + /implement

**Use THIS for:**
- Bug fixes (< 5 files)
- Simple feature additions
- Refactoring existing code
- Adding tests to existing features
- Quick API endpoint changes

**Use `/plan` → `/implement` for:**
- New features (> 5 files)
- Architecture changes
- Database schema changes
- Complex integrations
- Multi-step implementations

## Available Skills (Auto-Active)

**Testing:** @testing-test-driven-development | @testing-debugging | @testing-final-verification
**Global:** @global-coding-style | @global-error-handling | @global-validation
**Backend:** @backend-api | @backend-models | @backend-queries | @backend-migrations
**Frontend:** @frontend-accessibility | @frontend-components | @frontend-css | @frontend-responsive
