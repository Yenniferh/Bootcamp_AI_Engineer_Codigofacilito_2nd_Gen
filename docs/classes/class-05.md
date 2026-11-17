# Class 05 — Tools, Actions & MCP

## Overview

Class 05 introduces the design and execution of tools with explicit policies, permission controls, structured errors, and integration through the Model Context Protocol (MCP).

The Agente Operador extends its existing tool-calling capabilities with a `ToolRunner` responsible for validating requests, enforcing execution policies, and controlling access to read and write operations.

The class also introduces an MCP server and client, allowing the agent to discover and execute tools through a standardized protocol rather than relying exclusively on local tool registration.

### Concepts

- Tool contracts and argument validation.
- Structured tool errors and error classification.
- Idempotent operations and safe retries.
- Tool execution policies and role-based permissions.
- Timeouts, retry limits, and execution logging.
- MCP architecture: host, client, and server.
- MCP tools, schemas, and annotations.
- Communication through the stdio transport.

## Starter Code

**Upstream commit:** [`3cdaecd`](https://github.com/RamsesCamas/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen/commit/3cdaecd27578a170b370f7a6e41cb5a68ca229d3) + [`5728d7c`](https://github.com/RamsesCamas/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen/commit/5728d7c6e0c494ee180fb57da4c8a29aa65069cc)

**Starter branch:** `chore/class-05-starter`

**Starter PR:** [PR #11 - Class 05 starter components](https://github.com/Yenniferh/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen/pull/11)

The Class 05 starter was selectively integrated from the instructor's repository while preserving the personal implementations developed in previous classes.

The integration introduces tool execution policies, role-based permissions, MCP communication, and additional agent capabilities.

### Components

| Component | Responsibility |
|---|---|
| `agents/tools.py` | Tool execution policies, permissions, timeouts, retries, and logging. |
| `contracts/tool_schemas.py` | Tool specifications, argument contracts, and structured errors. |
| `tools/tickets.py` | Ticket retrieval and state updates. |
| `operador_mcp/server.py` | MCP server exposing tools through stdio. |
| `operador_mcp/client.py` | MCP client that discovers and invokes remote tools. |
| `main.py` | CLI integration for MCP and role selection. |
| `agents/react_agent.py` | Integration with the tool execution layer. |
| `agents/planner.py` | Integration with the tool execution layer. |
| `agents/verifier.py` | Instructor-provided response verifier from the previous class challenge. |
| `prompts/verifier/` | Prompt for checking responses against trace observations. |
| `prompts/reviser/` | Prompt for revising responses that fail verification. |
| `tests/test_tool_runner.py` | Tests for tool execution policies. |
| `tests/test_mcp.py` | Tests for MCP integration. |
| `tests/test_actualizar_estado.py` | Tests for ticket state updates. |

### ToolRunner

`ToolRunner` provides a controlled execution layer between the agent and the tool handlers.

Each tool can define a `ToolPolicy` containing:

- Permission level: `lectura`, `escritura`, or `peligrosa`.
- Execution timeout.
- Idempotency configuration.
- Maximum number of calls per execution.

The execution layer validates permissions, call limits, and arguments before invoking a handler.

Transient failures may be retried when the operation is idempotent.

Tools without an explicit policy are treated as dangerous and denied by default.

### Structured Tool Errors

The starter introduces a standardized error structure through `tool_error()`.

| Error Type | Meaning |
|---|---|
| `validacion` | Invalid arguments or unknown tool. |
| `negocio` | Business rule violation or unavailable entity. |
| `transitorio` | Temporary failure that may permit retrying. |
| `permanente` | Unexpected execution failure. |
| `permiso` | Operation not permitted for the current role. |
| `limite` | Maximum number of calls exceeded. |

Structured errors allow the agent to interpret failures without exposing internal tracebacks.

### Idempotent State Updates

The starter introduces `actualizar_estado`, a tool that sets a ticket's state.

Repeated requests to set the same state do not create additional changes.

Updates are stored in `var/tickets_estado.json`, while the original `data/tickets_db.json` remains unchanged.

### MCP Integration

The project implements an MCP server and client using the Python MCP SDK.

The server exposes tools through stdio, and the client discovers them dynamically through the MCP protocol.

The MCP server delegates tool execution to `ToolRunner`, preserving permission checks, argument validation, and execution policies.

Tool annotations describe properties such as read-only behavior, destructive operations, and idempotency.

### Instructor-Provided Verifier

The starter also includes the instructor's solution to the Class 04 independent challenge.

This includes:

- The `Verificacion` Pydantic contract.
- Verification against the agent's trace observations.
- A single revision when verification fails.
- The verifier and reviser prompts.

These components were incorporated from upstream and are not recorded as a personal implementation of the Class 04 challenge.

## Activity

Class 05 includes a guided practice and an independent challenge.

### Guided Practice: List Tickets by Provider

The guided practice focuses on extending the agent with a read-only tool that retrieves tickets associated with a provider.

#### Requirements

1. Implement `listar_tickets_por_proveedor` in `tools/tickets.py`.
2. Return at most 10 tickets, including their IDs, subjects, and states, along with the total number of matching tickets.
3. Create `ListarTicketsPorProveedorArgs` and `LISTAR_TICKETS_POR_PROVEEDOR` in `contracts/tool_schemas.py`.
4. Register the tool with a read-only `ToolPolicy`.
5. Expose the tool through the MCP server with `readOnlyHint`.
6. Validate its behavior without an LLM and subsequently through the agent.

#### Expected Behavior

```bash
uv run main.py --agent react --mcp "¿Qué tickets tiene PagosRed?"
```

The agent should retrieve tickets associated with the specified provider through MCP.

### Independent Challenge: Idempotent Ticket Creation

The independent challenge is to implement `crear_ticket`, a write operation exposed through MCP.

#### Requirements

1. Create `CrearTicketArgs` with `asunto`, `descripcion`, and `prioridad`.
2. Generate an `idempotency_key` in application code, rather than requesting it from the model.
3. Register the tool with a write policy and idempotent behavior.
4. Expose the tool through MCP with the appropriate annotations.
5. Verify that repeated calls with the same request identity do not create duplicate tickets.

#### Expected Behavior

Two equivalent requests using the same `request_id` should result in a single persisted ticket.

The tool should support safe retries without producing duplicate records.

## Personal Implementation

**Branch:** `feat/class-05`

**Status:** Pending

### Guided Practice

Pending implementation.

### Independent Challenge

Pending implementation.

Implementation details, design decisions, and related pull requests will be documented after completing each activity.

## Validation & Results

**Status:** Starter validation completed partially; activity validation pending.

### Project Checks

```bash
just check
```

### Local Agent

```bash
uv run main.py --agent react "¿Cómo va el T-1042?"
```

### MCP Agent

```bash
uv run main.py --agent react --mcp "¿Cómo va el T-1042?"
```

### MCP Server

```bash
uv run python -m operador_mcp.server
```

The server communicates through stdio and is normally launched automatically by the MCP client.

### MCP Inspector

```bash
npx @modelcontextprotocol/inspector uv run python -m operador_mcp.server
```

The Inspector requires Node.js and npm in the development environment.

### Initial MCP Validation

The following behavior was observed during manual testing:

- MCP tool discovery succeeded.
- Direct tool invocation through `MCPToolset` returned the expected ticket information.
- The agent produced a correct response using the MCP-enabled execution path.
- The MCP connection could be opened and closed without error when no tool was invoked.

### Known Issue: JSON-RPC Warning During Shutdown

During manual testing, the following warning was observed:

```text
Failed to parse JSONRPC message from server
```

The warning occurred when closing an MCP connection after a successful tool invocation.

Additional testing showed that:

- Tool discovery completed successfully.
- Tool execution returned the expected result.
- The warning did not appear while the connection remained open.
- Closing a connection without invoking a tool did not reproduce the warning.

The underlying cause has not been identified.

Because tool discovery and execution were functional, the issue was considered non-blocking for the starter integration. No changes were made to the MCP implementation solely to suppress the warning.

### Activity Results

Pending completion of the guided practice and independent challenge.

## Milestone

**Tag:** `class-05` - Pending

**Starter PR:** [#11](https://github.com/Yenniferh/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen/pull/11)

**Activity PR:** Pending

The `class-05` tag will be created after integrating the completed Class 05 activities into `develop`.
