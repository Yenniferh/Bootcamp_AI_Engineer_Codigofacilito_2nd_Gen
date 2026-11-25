# Class 05 — Tools, Actions & MCP

## Overview

Class 05 introduces tool execution policies, structured errors, idempotent actions, and integration through the Model Context Protocol (MCP). The Agente Operador extends its tool-calling capabilities with a controlled execution layer and a client/server architecture.

### Concepts

- Tool contracts and argument validation.
- Structured tool errors and error classification.
- Idempotency, persistence, and safe retries.
- Role-based permissions, timeouts, and call limits.
- MCP host, client, server, tool discovery, schemas, and annotations.
- Communication through stdio.

## Starter Code

**Upstream commits:** [`3cdaecd`](https://github.com/RamsesCamas/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen/commit/3cdaecd27578a170b370f7a6e41cb5a68ca229d3) + [`5728d7c`](https://github.com/RamsesCamas/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen/commit/5728d7c6e0c494ee180fb57da4c8a29aa65069cc)

**Starter branch:** `chore/class-05-starter`

**Starter PR:** [#11](https://github.com/Yenniferh/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen/pull/11)

The starter was selectively integrated from upstream while preserving personal implementations from previous classes.

### Components

| Component | Responsibility |
|---|---|
| `agents/tools.py` | Tool policies, permissions, timeouts, retries, and logging. |
| `contracts/tool_schemas.py` | Tool specifications, argument contracts, and structured errors. |
| `tools/tickets.py` | Ticket retrieval and state updates. |
| `operador_mcp/server.py` | MCP server exposing tools through stdio. |
| `operador_mcp/client.py` | MCP tool discovery and invocation. |
| `main.py` | CLI integration for MCP and role selection. |
| `agents/react_agent.py`, `agents/planner.py` | Integration with the tool execution layer. |
| `agents/verifier.py`, `prompts/verifier/`, `prompts/reviser/` | Instructor-provided solution to the Class 04 challenge. |
| `tests/test_tool_runner.py`, `tests/test_mcp.py`, `tests/test_actualizar_estado.py` | Execution policy, MCP, and state-update tests. |

### ToolRunner

`ToolRunner` validates permissions, call limits, and arguments before executing handlers with a timeout. Transient failures may be retried for idempotent tools. `ToolPolicy` defines permission level (`lectura`, `escritura`, or `peligrosa`), timeout, idempotency, and maximum calls. Tools without explicit policies are denied by default.

### Structured Tool Errors

| Error Type | Meaning |
|---|---|
| `validacion` | Invalid arguments or unknown tool. |
| `negocio` | Business rule violation or unavailable entity. |
| `transitorio` | Temporary failure. |
| `permanente` | Unexpected execution failure. |
| `permiso` | Operation not permitted for the role. |
| `limite` | Maximum calls exceeded. |

### Idempotent State Updates

`actualizar_estado` sets a ticket state rather than toggling it. Updates are stored in `var/tickets_estado.json`, leaving the original dataset unchanged.

### MCP Integration

The Python MCP client launches the server through stdio, discovers tools dynamically, and invokes them through the protocol. The server delegates execution to `ToolRunner`. MCP annotations describe tool behavior; permission enforcement remains the runner's responsibility.

### Instructor-Provided Verifier

The Class 04 verifier challenge solution was incorporated from upstream, including the `Verificacion` contract, verification against trace observations, and at most one revision. It is not a personal implementation of the Class 04 challenge.

## Activity

### Guided Practice: List Tickets by Provider

Implement `listar_tickets_por_proveedor`, a read-only tool that returns up to 10 tickets with their IDs, subjects, states, and total matching count. Define its argument contract, register its policy, expose it through MCP with `readOnlyHint`, and validate it without and with an LLM.

### Independent Challenge: Idempotent Ticket Creation

Implement `crear_ticket` with `CrearTicketArgs(asunto, descripcion, prioridad)`, an application-generated idempotency key, an idempotent write policy, and MCP exposure. The reference requirements call for a stable request-derived key and a test demonstrating that repeated calls with the same key create only one ticket.

## Personal Implementation

**Branch:** `feat/class-05`

**Status:** Both activities implemented; integration pending.

**Activity PR:** [#12 - Add tools listar tickets por proveedor and crear ticket](https://github.com/Yenniferh/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen/pull/12)

### Guided Practice: Provider Ticket Listing

Implemented `ListarTicketsPorProveedorArgs`, `LISTAR_TICKETS_POR_PROVEEDOR`, and `listar_tickets_por_proveedor()`. The handler reuses `normalize_provider_name()` from Class 03 to match provider names against the original ticket dataset. It returns a structured business error when no matching tickets exist.

The optional `tope` argument defaults to 10 in the handler and accepts values from 1 to 20. The result contains the normalized provider name and matching ticket records up to that limit. The tool is registered with a read-only policy and a two-second timeout, and exposed through MCP.

### Independent Challenge: Ticket Creation

Implemented `CrearTicketArgs`, `CREAR_TICKET`, and `crear_ticket()`. The public argument contract validates subject and description (minimum five characters each) and priority (`baja`, `media`, or `alta`). The idempotency key is stored in a Pydantic `PrivateAttr`, keeping it outside the model-facing schema.

#### Idempotency and Retry Flow

1. `ToolRunner` validates the arguments and generates a UUID using `uuid.uuid4().hex` before entering its retry loop.
2. The key is assigned to `args._idempotency_key` and reused across retries of that execution.
3. The handler checks persisted tickets for the key before creating a record.
4. If the key already exists, the handler returns the existing ticket instead of creating another.
5. If no key is supplied, the handler returns a permanent error without writing a ticket.

This design protects against duplicate creation when a transient failure occurs after persistence but before the response reaches the runner. The key is generated by application code, not the LLM.

#### Persistence and Integration

New tickets are stored in `var/tickets_nuevos.json` with their internal idempotency keys. IDs are assigned by incrementing the highest existing numeric ticket ID across both sources. New records start in `abierto` with an empty history and no assigned team or provider.

Writes use a temporary file and `os.replace()` to avoid partially written JSON. `buscar_ticket` and `actualizar_estado` now access both the original dataset and newly persisted tickets. State overlays remain separate.

Both new tools are registered in the CLI and exposed by the MCP server. `crear_ticket` uses a write policy with idempotency enabled by default, and its description requires an explicit user request to create a ticket.

## Validation & Results

### Automated Tests

| Test file | Coverage added |
|---|---|
| `tests/test_crear_ticket.py` | Persistence, same-key deduplication, different keys, missing key, retrieval of new and existing tickets. |
| `tests/test_tool_runner.py` | Simulated lost response after persistence; retry reuses the key, returns the same ticket, and leaves one persisted record. |
| `tests/test_tool_schemas.py` | Tool schemas, provider listing and not-found behavior, subject/description length, priority validation, missing key. |
| `tests/test_mcp.py` | Discovery of both new tools, policy annotations, private key excluded from the public schema, and rejection of creation by the read-only role. |

Persistence tests use temporary paths and `monkeypatch` to avoid modifying the real runtime data. The retry test asserts two attempts, identical keys and results, one persisted ticket, and the expected backoff.

### Validation Commands

```bash
uv run pytest tests/test_crear_ticket.py tests/test_tool_runner.py tests/test_tool_schemas.py tests/test_mcp.py -q
just check
```

Manual validation commands:

```bash
uv run main.py --agent react --mcp "¿Qué tickets tiene PagosRed?"
uv run main.py --agent react --mcp --rol operador "Crea un ticket por caída del portal de pagos con prioridad alta"
```

The second command writes runtime data if the agent executes the creation tool. MCP Inspector can also be launched with:

```bash
npx @modelcontextprotocol/inspector uv run python -m operador_mcp.server
```

The Inspector requires Node.js and npm; the Python server itself does not.

### Known Issue: JSON-RPC Warning During Shutdown

During starter validation, tool discovery and direct MCP invocation succeeded, but `Failed to parse JSONRPC message from server` appeared when closing a connection after a tool call. Closing without invoking a tool did not reproduce the warning. The cause remains unconfirmed; no changes were made solely to suppress it. This was considered non-blocking for the starter. Its status after the activity has not been independently revalidated.

### Limitations and Differences from the Reference Requirements

- The UUID is stable within one runner execution and its internal retries, not across separate tool invocations. A caller-provided `request_id` and deterministic request-derived key are not implemented; repeated independent calls may create duplicates.
- The listing tool returns full original dataset records and omits the total matching count. Its maximum is 20 rather than the reference limit of 10, and it does not apply state overlays to listed records.
- The MCP listing wrapper accepts nullable `tope` but has no Python default, so omission may not behave as it does in the local argument contract.
- Ticket IDs increment from the highest existing ID rather than explicitly starting in the `T-2xxx` range.
- Atomic file replacement prevents partial writes but does not guarantee concurrency-safe ID allocation or deduplication across simultaneous requests.
- The legacy `--tools` execution path does not inject the private key through `ToolRunner`; ticket creation is intended for the runner-backed agent/MCP path.

The automated coverage above is based on the PR diff. Test execution results, CI status, and manual end-to-end activity results have not been independently verified.

## Milestone

**Tag:** `class-05` — Pending merge

**Starter PR:** [#11](https://github.com/Yenniferh/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen/pull/11)

**Activity PR:** [#12](https://github.com/Yenniferh/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen/pull/12)

Both activities have been implemented in `feat/class-05`. The milestone tag will be created after the activity PR is integrated into `develop`.
