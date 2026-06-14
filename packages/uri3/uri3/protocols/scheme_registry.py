from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urlparse

from uri3.protocols.schemes import SUPPORTED_SCHEMES


@dataclass(frozen=True)
class QueryOption:
    name: str
    type: str
    aliases: tuple[str, ...] = ()
    default: Any = None
    enum: tuple[str, ...] | None = None
    description: str = ""

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "name": self.name,
            "type": self.type,
            "description": self.description,
        }
        if self.aliases:
            payload["aliases"] = list(self.aliases)
        if self.default is not None:
            payload["default"] = self.default
        if self.enum:
            payload["enum"] = list(self.enum)
        return payload


@dataclass(frozen=True)
class SchemeSpec:
    scheme: str
    description: str
    template: str
    netloc: dict[str, Any] = field(default_factory=dict)
    path: dict[str, Any] = field(default_factory=dict)
    query: tuple[QueryOption, ...] = ()
    constants: dict[str, Any] = field(default_factory=dict)
    actions: tuple[str, ...] = ("resolve",)
    cli: tuple[str, ...] = ()
    python_api: tuple[str, ...] = ()
    examples: tuple[str, ...] = ()
    documented: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "scheme": self.scheme,
            "supported": self.scheme in SUPPORTED_SCHEMES,
            "documented": self.documented,
            "description": self.description,
            "template": self.template,
            "format": {
                "netloc": self.netloc,
                "path": self.path,
                "query": [option.to_dict() for option in self.query],
            },
            "constants": self.constants,
            "actions": list(self.actions),
            "api": {
                "cli": list(self.cli),
                "python": list(self.python_api),
            },
            "examples": list(self.examples),
        }


def _log_spec() -> SchemeSpec:
    from uri3.logs.reader import DEFAULT_STREAM_FILES
    from uri3.resolvers.log_resolver import LOG_LEVELS

    return SchemeSpec(
        scheme="log",
        description="Read and filter repository log files by stream, path, and query filters.",
        template="log://{stream}[/{path}][?{query}]",
        netloc={
            "name": "stream",
            "required": False,
            "default": "hypervisor",
            "description": "Named log stream or the special value `file` for explicit paths.",
            "known_values": {
                key: value for key, value in DEFAULT_STREAM_FILES.items() if key != "default"
            },
        },
        path={
            "required": False,
            "description": "Optional repo-relative log path. Required when stream=file.",
        },
        query=(
            QueryOption(
                "level",
                "enum",
                aliases=("min_level",),
                enum=LOG_LEVELS,
                description="Minimum log level to include.",
            ),
            QueryOption("grep", "string", aliases=("q", "contain"), description="Case-insensitive substring filter."),
            QueryOption("logger", "string", aliases=("component",), description="Filter by logger/component name."),
            QueryOption(
                "since",
                "string",
                aliases=("from",),
                description="Lower time bound: ISO timestamp or relative duration (1h, 30m, 2d).",
            ),
            QueryOption(
                "until",
                "string",
                aliases=("to",),
                description="Upper time bound: ISO timestamp or relative duration.",
            ),
            QueryOption("limit", "integer", default=100, description="Maximum number of entries to return."),
            QueryOption("offset", "integer", default=0, description="Skip this many matched entries."),
            QueryOption(
                "tail",
                "boolean",
                default=False,
                description="When true with limit, return the last N matched entries.",
            ),
            QueryOption(
                "format",
                "string",
                default="auto",
                description="Log line format hint: auto, json, or text.",
            ),
        ),
        constants={"levels": list(LOG_LEVELS), "streams": dict(DEFAULT_STREAM_FILES)},
        actions=("resolve", "read", "summarize", "scan", "call"),
        cli=("uri3 logs", "uri3 scan", "uri3 resolve", "uri3 schema"),
        python_api=(
            "uri3.logs.reader.read_logs",
            "uri3.logs.reader.summarize_logs",
            "uri3.resolvers.log_resolver.parse_log_uri",
            "uri3.resolvers.router.call",
        ),
        examples=(
            "log://hypervisor?level=ERROR&grep=deployment&limit=20",
            "log://hypervisor?since=1h&tail=1&limit=50",
            "log://file/output/logs/hypervisor.log?grep=timeout",
        ),
    )


def _env_spec() -> SchemeSpec:
    return SchemeSpec(
        scheme="env",
        description="Resolve environment variable names to values.",
        template="env://{name}",
        netloc={"name": "name", "required": True, "description": "Environment variable name."},
        path={"name": "name", "required": False, "description": "Alternative location for variable name."},
        actions=("resolve",),
        cli=("uri3 resolve", "uri3 schema"),
        python_api=("uri3.resolvers.env_resolver.resolve_env",),
        examples=("env://OPENROUTER_API_KEY", "env:///PATH"),
    )


def _python_spec() -> SchemeSpec:
    return SchemeSpec(
        scheme="python",
        description="Reference a Python callable as module:function.",
        template="python://{module}:{function}",
        netloc={"name": "target", "required": True, "description": "Module path before colon."},
        path={"name": "function", "required": True, "description": "Function name after colon."},
        actions=("resolve", "call"),
        cli=("uri3 resolve", "uri3 schema"),
        python_api=(
            "uri3.resolvers.python_resolver.resolve_python",
            "uri3.resolvers.python_resolver.call_python",
        ),
        examples=("python://hypervisor.core:Hypervisor",),
    )


def _llm_spec() -> SchemeSpec:
    return SchemeSpec(
        scheme="llm",
        description="Reference an LLM provider and model.",
        template="llm://{provider}/{model}",
        netloc={"name": "provider", "required": True, "description": "LLM provider, e.g. openrouter."},
        path={"name": "model", "required": True, "description": "Model identifier without provider prefix."},
        constants={"providers": ["openrouter"], "api_key_env": {"openrouter": "OPENROUTER_API_KEY"}},
        actions=("resolve",),
        cli=("uri3 resolve", "uri3 schema"),
        python_api=("uri3.resolvers.llm_resolver.resolve_llm",),
        examples=("llm://openrouter/anthropic/claude-3.5-sonnet",),
    )


def _pypi_spec() -> SchemeSpec:
    return SchemeSpec(
        scheme="pypi",
        description="Reference a PyPI package and optional version.",
        template="pypi://{package}[/{version}]",
        netloc={"name": "package", "required": True, "description": "PyPI distribution name."},
        path={"name": "version", "required": False, "description": "Package version; defaults to latest."},
        actions=("resolve",),
        cli=("uri3 resolve", "uri3 schema"),
        python_api=("uri3.resolvers.pypi_resolver.resolve_pypi",),
        examples=("pypi://requests", "pypi://pydantic/2.8.0"),
    )


def _http_spec(scheme: str) -> SchemeSpec:
    return SchemeSpec(
        scheme=scheme,
        description=f"HTTP endpoint reference via {scheme}://.",
        template=f"{scheme}://{{host}}[{{path}}][?{{query}}]",
        netloc={"name": "host", "required": True, "description": "Host and optional port."},
        path={"name": "path", "required": False, "description": "Request path."},
        actions=("resolve", "scan"),
        cli=("uri3 scan", "uri3 resolve", "uri3 schema"),
        python_api=("uri3.scanner.http_scanner.scan_http",),
        examples=(f"{scheme}://localhost:8101/.well-known/agent-card.json",),
    )


def _a2a_spec() -> SchemeSpec:
    return SchemeSpec(
        scheme="a2a",
        description="Agent-to-agent endpoint reference.",
        template="a2a://{agent}[/{path}]",
        netloc={"name": "agent", "required": True, "description": "Agent identifier or host."},
        path={"name": "path", "required": False, "default": "/", "description": "Agent sub-path."},
        actions=("resolve",),
        cli=("uri3 resolve", "uri3 schema"),
        python_api=("uri3.resolvers.protocol_resolver.resolve_a2a",),
        examples=("a2a://weather-map-agent/tasks",),
    )


def _mcp_spec() -> SchemeSpec:
    return SchemeSpec(
        scheme="mcp",
        description="Model Context Protocol server reference.",
        template="mcp://{server}[/{path}]",
        netloc={"name": "server", "required": True, "description": "MCP server identifier or host."},
        path={"name": "path", "required": False, "default": "/", "description": "Server sub-path."},
        actions=("resolve",),
        cli=("uri3 resolve", "uri3 schema"),
        python_api=("uri3.resolvers.protocol_resolver.resolve_mcp",),
        examples=("mcp://filesystem/tools",),
    )


def _resource_like_spec(scheme: str, description: str) -> SchemeSpec:
    return SchemeSpec(
        scheme=scheme,
        description=description,
        template=f"{scheme}://{{namespace}}/{{path}}",
        netloc={"name": "namespace", "required": False, "description": "Logical namespace or host."},
        path={"name": "path", "required": False, "description": "Resource path within namespace."},
        actions=("resolve",),
        cli=("uri3 resolve", "uri3 schema"),
        python_api=("uri3.resolvers.protocol_resolver.resolve_resource",),
        documented=False,
        examples=(f"{scheme}://example/resource",),
    )


def _build_registry() -> dict[str, SchemeSpec]:
    specs = [
        _log_spec(),
        _env_spec(),
        _python_spec(),
        _llm_spec(),
        _pypi_spec(),
        _http_spec("http"),
        _http_spec("https"),
        _a2a_spec(),
        _mcp_spec(),
        _resource_like_spec("resource", "Generic in-repo or logical resource reference."),
        _resource_like_spec("artifact", "Build or generation artifact reference."),
        _resource_like_spec("domain", "Domain pack or bounded context reference."),
        _resource_like_spec("agent", "Generated or deployed agent reference."),
        _resource_like_spec("local", "Local filesystem resource reference."),
        _resource_like_spec("input", "Pipeline input reference."),
        _resource_like_spec("command", "Command or action reference."),
        _resource_like_spec("event", "Event source or channel reference."),
        _resource_like_spec("ssh", "Remote host path accessed over SSH."),
        _resource_like_spec("docker", "Docker container or image reference."),
        _resource_like_spec("git", "Git repository reference."),
    ]
    return {spec.scheme: spec for spec in specs}


SCHEME_REGISTRY: dict[str, SchemeSpec] = _build_registry()


def normalize_scheme(value: str) -> str:
    raw = value.strip()
    if not raw:
        raise ValueError("Scheme or URI is required")
    if "://" in raw:
        scheme = urlparse(raw).scheme
        if scheme:
            return scheme.lower()
    return raw.rstrip(":/").lower()


def is_concrete_uri(value: str) -> bool:
    if "://" not in value:
        return False
    parsed = urlparse(value)
    return bool(parsed.netloc or parsed.path.strip("/") or parsed.query)


def get_scheme_schema(scheme_or_uri: str) -> dict[str, Any]:
    scheme = normalize_scheme(scheme_or_uri)
    if scheme not in SUPPORTED_SCHEMES:
        raise ValueError(f"Unsupported URI scheme: {scheme}")
    spec = SCHEME_REGISTRY.get(scheme)
    if spec is None:
        spec = _resource_like_spec(scheme, f"Supported scheme `{scheme}` without detailed schema yet.")
    return spec.to_dict()


def list_schemes(*, documented_only: bool = False) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for scheme in sorted(SUPPORTED_SCHEMES):
        spec = SCHEME_REGISTRY.get(scheme)
        if spec is None:
            items.append(
                {
                    "scheme": scheme,
                    "supported": True,
                    "documented": False,
                    "description": f"Supported scheme `{scheme}` without detailed schema yet.",
                    "template": f"{scheme}://{{target}}",
                }
            )
            continue
        if documented_only and not spec.documented:
            continue
        items.append(
            {
                "scheme": spec.scheme,
                "supported": True,
                "documented": spec.documented,
                "description": spec.description,
                "template": spec.template,
                "actions": list(spec.actions),
            }
        )
    return items


def _query_names(spec: SchemeSpec) -> set[str]:
    names: set[str] = set()
    for option in spec.query:
        names.add(option.name)
        names.update(option.aliases)
    return names


def _parse_instance(scheme: str, uri: str) -> dict[str, Any]:
    if scheme == "log":
        from uri3.resolvers.log_resolver import parse_log_uri

        ref = parse_log_uri(uri)
        return ref.to_dict()
    if scheme == "env":
        from uri3.resolvers.env_resolver import resolve_env

        return resolve_env(uri)
    if scheme == "python":
        from uri3.resolvers.python_resolver import resolve_python

        return resolve_python(uri)
    if scheme == "llm":
        from uri3.resolvers.llm_resolver import resolve_llm

        return resolve_llm(uri)
    if scheme == "pypi":
        from uri3.resolvers.pypi_resolver import resolve_pypi

        return resolve_pypi(uri)
    if scheme in {"http", "https"}:
        from uri3.resolvers.protocol_resolver import resolve_http_like

        return resolve_http_like(uri)
    if scheme == "a2a":
        from uri3.resolvers.protocol_resolver import resolve_a2a

        return resolve_a2a(uri)
    if scheme == "mcp":
        from uri3.resolvers.protocol_resolver import resolve_mcp

        return resolve_mcp(uri)
    if scheme in {
        "resource",
        "artifact",
        "domain",
        "agent",
        "local",
        "input",
        "command",
        "event",
        "ssh",
        "docker",
        "git",
    }:
        from uri3.resolvers.protocol_resolver import resolve_resource

        return resolve_resource(uri)
    raise ValueError(f"No parser available for scheme: {scheme}")


def analyze_uri(uri: str) -> dict[str, Any]:
    scheme = normalize_scheme(uri)
    schema = get_scheme_schema(scheme)
    spec = SCHEME_REGISTRY.get(scheme)
    parsed = urlparse(uri)
    query_keys = set(parsed.query.split("&")) if parsed.query else set()
    query_keys = {key.split("=", 1)[0] for key in query_keys if key}

    result: dict[str, Any] = {
        "uri": uri,
        "scheme": scheme,
        "schema": schema,
        "components": {
            "netloc": parsed.netloc,
            "path": parsed.path,
            "query": parsed.query,
        },
    }

    try:
        result["parsed"] = _parse_instance(scheme, uri)
        result["valid"] = True
        result["errors"] = []
    except ValueError as exc:
        result["parsed"] = None
        result["valid"] = False
        result["errors"] = [str(exc)]

    if spec and spec.query:
        known = _query_names(spec)
        canonical = {option.name for option in spec.query}
        used = sorted(key for key in query_keys if key in known)
        unknown = sorted(key for key in query_keys if key not in known)
        available = sorted(name for name in canonical if name not in used)
        result["query"] = {
            "used": used,
            "unknown": unknown,
            "available": available,
            "options": [option.to_dict() for option in spec.query],
        }
    else:
        result["query"] = {
            "used": sorted(query_keys),
            "unknown": [],
            "available": [],
            "options": [],
        }

    return result


def describe_uri(value: str) -> dict[str, Any]:
    if is_concrete_uri(value):
        return analyze_uri(value)
    return get_scheme_schema(value)
