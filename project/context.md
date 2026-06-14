# System Architecture Analysis
<!-- generated in 0.00s -->

## Overview

- **Project**: /home/tom/github/wronai/hypervisor
- **Primary Language**: python
- **Languages**: python: 214, yaml: 40, json: 12, shell: 6, toml: 5
- **Analysis Mode**: static
- **Total Functions**: 556
- **Total Classes**: 63
- **Modules**: 294
- **Entry Points**: 175

## Architecture by Module

### packages.uri3.uri3.cli
- **Functions**: 16
- **File**: `cli.py`

### packages.resource-agent-hypervisor.hypervisor.cli
- **Functions**: 15
- **File**: `cli.py`

### packages.uri3.uri3.protocols.schemes.instance_parser
- **Functions**: 13
- **File**: `instance_parser.py`

### packages.nl2uri.nl2uri.cli
- **Functions**: 13
- **File**: `cli.py`

### packages.nl2uri.nl2uri.graph_planner
- **Functions**: 11
- **File**: `graph_planner.py`

### packages.resource-agent-hypervisor.hypervisor.deployment_registry.status
- **Functions**: 10
- **File**: `status.py`

### hypervisor.config.models
- **Functions**: 9
- **Classes**: 8
- **File**: `models.py`

### packages.uri3.uri3.docker.actions.compose
- **Functions**: 8
- **File**: `compose.py`

### packages.resource-agent-hypervisor.hypervisor.uri.client
- **Functions**: 8
- **Classes**: 1
- **File**: `client.py`

### packages.resource-agent-hypervisor.hypervisor.deployment_registry.runtime_state
- **Functions**: 8
- **File**: `runtime_state.py`

### packages.nl2uri.nl2uri.graph_repair
- **Functions**: 8
- **File**: `graph_repair.py`

### packages.uri3.uri3.logs.filters
- **Functions**: 7
- **File**: `filters.py`

### packages.uri3.uri3.config.ssh_auth
- **Functions**: 7
- **File**: `ssh_auth.py`

### packages.uri3.uri3.resolvers.ssh_resolver
- **Functions**: 7
- **File**: `ssh_resolver.py`

### packages.uri3.uri3.resolvers.docker_resolver
- **Functions**: 7
- **Classes**: 1
- **File**: `docker_resolver.py`

### packages.uri3.uri3.resolvers.env_resolver
- **Functions**: 7
- **Classes**: 1
- **File**: `env_resolver.py`

### meta_agent.api
- **Functions**: 7
- **Classes**: 2
- **File**: `api.py`

### packages.resource-agent-hypervisor.hypervisor.core
- **Functions**: 7
- **Classes**: 1
- **File**: `core.py`

### packages.uri3.uri3.scanner.http_scanner
- **Functions**: 6
- **File**: `http_scanner.py`

### packages.uri3.uri3.scanner.ssh_scanner
- **Functions**: 6
- **File**: `ssh_scanner.py`

## Key Entry Points

Main execution flows into the system:

### hypervisor.config.models.HypervisorConfig.from_dict
- **Calls**: cls, str, str, data.get, bool, str, LLMConfig.from_dict, Uri3Config.from_dict

### packages.resource-agent-hypervisor.meta_agent.cli.main
- **Calls**: argparse.ArgumentParser, parser.add_subparsers, sub.add_parser, plan.add_argument, plan.add_argument, sub.add_parser, validate.add_argument, sub.add_parser

### packages.uri3.uri3.protocols.schemes.spec_registry.build_scheme_registry
- **Calls**: log.spec, env.spec, python.spec, llm.spec, pypi.spec, http.spec, http.spec, a2a.spec

### packages.uri3.uri3.graph.adapters.browser_playwright.PlaywrightBrowserAdapter.execute
- **Calls**: packages.uri3.uri3.graph.adapters.browser_playwright._session_state, state.get, None.execute, urlparse, str, None.start, playwright.chromium.launch, browser.new_page

### packages.uri3.uri3.cli.scan
- **Calls**: app.command, typer.Argument, typer.Option, typer.echo, packages.uri3.uri3.config.cli_shortcuts.scan_shortcuts, typer.echo, typer.echo, typer.echo

### packages.uri3.uri3.graph.adapters.registry.AssertionAdapter.execute
- **Calls**: payload.get, payload.get, payload.get, context.resolve_ref, node.uri.endswith, payload.get, payload.get, bool

### packages.nl2uri.nl2uri.cli.task
- **Calls**: app.command, typer.Option, typer.Option, typer.Option, typer.Option, typer.Option, typer.Option, packages.nl2uri.nl2uri.graph_planner.plan_task

### packages.nl2uri.nl2uri.cli.graph
- **Calls**: app.command, typer.Option, typer.Option, typer.Option, typer.Option, typer.Option, typer.Option, packages.nl2uri.nl2uri.graph_planner.plan_workflow_graph

### packages.uri3.uri3.graph.models.GraphNode.from_dict
- **Calls**: cls, str, str, str, data.get, data.get, dict, list

### packages.nl2uri.nl2uri.cli.tree
- **Calls**: app.command, typer.Option, typer.Option, typer.Option, typer.Option, packages.nl2uri.nl2uri.graph_planner.plan_tree, packages.nl2uri.nl2uri.cli._emit, nl2uri.writer.write_uri_tree

### packages.nl2uri.nl2uri.cli.generate
> Backward-compatible URI Tree generation.
- **Calls**: app.command, typer.Option, typer.Option, typer.Option, typer.Option, packages.nl2uri.nl2uri.domain_planner.plan_from_prompt, packages.nl2uri.nl2uri.cli._emit, nl2uri.writer.write_uri_tree

### packages.uri3.uri3.protocols.schemes.log.spec
- **Calls**: SchemeSpec, QueryOption, QueryOption, QueryOption, QueryOption, QueryOption, QueryOption, QueryOption

### packages.resource-agent-hypervisor.hypervisor.contract_registry.cli_commands.run_check_command
- **Calls**: hypervisor.contract_registry.schema_validator.validate_contract_files, hypervisor.contract_registry.loader.load_contract_registry, packages.resource-agent-hypervisor.hypervisor.contract_registry.validate.validate_registry, packages.resource-agent-hypervisor.hypervisor.contract_registry.cross_validator.validate_root, hypervisor.contract_registry.registry_builder.write_registry_manifest, print, print, len

### packages.nl2uri.nl2uri.cli.plan
> Classify prompt and generate the best matching URI plan.
- **Calls**: app.command, typer.Option, typer.Option, typer.Option, typer.Option, typer.Option, packages.nl2uri.nl2uri.graph_planner.plan_auto, packages.nl2uri.nl2uri.cli._emit

### hypervisor.config.models.HypervisorSettings.from_dict
- **Calls**: data.get, cls, str, int, str, bool, str, data.get

### packages.resource-agent-hypervisor.hypervisor.evolution.cli.main
- **Calls**: print, print, sorted, hypervisor.evolution.models.load_proposal, hypervisor.evolution.validator.validate_proposal, print, None.glob, Path

### hypervisor.compatibility.checker.classify_registry_change
- **Calls**: Path, Path, hypervisor.contract_registry.loader.load_contract_registry, hypervisor.contract_registry.loader.load_contract_registry, sorted, sorted, sorted, sorted

### domains.weather_map.handlers.generate_weather_map.handler
- **Calls**: payload.get, int, None.hexdigest, payload.get, payload.get, payload.get, None.isoformat, hashlib.sha256

### generator.verify.main
- **Calls**: Path, generator.verify.verify_generated, print, root.exists, print, print, print, root.iterdir

### packages.uri3.uri3.cli.list_cmd
> List schemes, scan shortcuts, and common examples.
- **Calls**: app.command, typer.Option, typer.Option, packages.uri3.uri3.cli._list_payload, typer.echo, typer.echo, packages.uri3.uri3.cli._quick_reference, json.dumps

### packages.uri3.uri3.cli.run_workflow_cmd
- **Calls**: app.command, typer.Option, typer.Option, typer.Option, packages.uri3.uri3.graph.graph_executor.run_workflow, typer.echo, packages.uri3.uri3.graph.graph_validator.load_workflow_graph, json.dumps

### generator.validate.main
- **Calls**: Path, generator.validate.iter_agent_specs, print, print, all_errors.extend, print, generator.validate.validate_agent, print

### hypervisor.policy_gate.gate.evaluate_change
- **Calls**: bool, change_report.get, change_report.get, bool, GateDecision, change_report.get, reasons.append, reasons.append

### testenv.ssh_agent_host.mock_agent_server.Handler._json
- **Calls**: None.encode, self.send_response, self.send_header, self.send_header, self.end_headers, self.wfile.write, str, json.dumps

### packages.uri3.uri3.cli.schema
> Describe URI format, options, and API for a scheme or concrete URI.
- **Calls**: app.command, typer.Argument, typer.Option, typer.Option, typer.echo, json.dumps, packages.uri3.uri3.protocols.schemes.spec_registry.list_schemes, packages.uri3.uri3.protocols.schemes.analyze.analyze_uri

### packages.uri3.uri3.resolvers.resolve_core.call
- **Calls**: urlparse, ValueError, uri3.resolvers.python_resolver.call_python, packages.uri3.uri3.resolvers.env_resolver.call_env, packages.uri3.uri3.docker.controller.control_docker, options.get, packages.uri3.uri3.logs.reader.read_logs, packages.uri3.uri3.logs.reader.summarize_logs

### packages.resource-agent-hypervisor.hypervisor.cli.run_agent_cmd
> Start a local agent or print an SSH remote start plan with --dry-run.
- **Calls**: app.command, typer.Argument, typer.Option, typer.Option, typer.Option, typer.Option, typer.Option, packages.resource-agent-hypervisor.hypervisor.cli_commands.run_local_agent

### packages.resource-agent-hypervisor.hypervisor.cli.restart_agent_cmd
> Restart a local agent (stop then start).
- **Calls**: app.command, typer.Argument, typer.Option, typer.Option, typer.Option, typer.Option, packages.resource-agent-hypervisor.hypervisor.cli_commands.echo_json, packages.resource-agent-hypervisor.hypervisor.deployment_registry.lifecycle.restart_agent

### hypervisor.verifier.cli.main
- **Calls**: Path, hypervisor.contract_registry.loader.load_contract_registry, packages.resource-agent-hypervisor.hypervisor.contract_registry.validate.validate_registry, hypervisor.verifier.capability_tests.build_capability_test_plan, print, print, json.dumps, print

### testenv.ssh_agent_host.mock_agent_server.Handler.do_GET
- **Calls**: urlparse, self._json, self._json, self._json, self._json, parse_qs, self._json, qs.get

## Process Flows

Key execution flows identified:

### Flow 1: from_dict
```
from_dict [hypervisor.config.models.HypervisorConfig]
```

### Flow 2: main
```
main [packages.resource-agent-hypervisor.meta_agent.cli]
```

### Flow 3: build_scheme_registry
```
build_scheme_registry [packages.uri3.uri3.protocols.schemes.spec_registry]
```

### Flow 4: execute
```
execute [packages.uri3.uri3.graph.adapters.browser_playwright.PlaywrightBrowserAdapter]
  └─ →> _session_state
```

### Flow 5: scan
```
scan [packages.uri3.uri3.cli]
  └─ →> scan_shortcuts
      └─> load_cli_config
          └─> cli_config_path
          └─ →> load_uri_yaml
```

### Flow 6: task
```
task [packages.nl2uri.nl2uri.cli]
```

### Flow 7: graph
```
graph [packages.nl2uri.nl2uri.cli]
```

### Flow 8: tree
```
tree [packages.nl2uri.nl2uri.cli]
```

### Flow 9: generate
```
generate [packages.nl2uri.nl2uri.cli]
```

### Flow 10: spec
```
spec [packages.uri3.uri3.protocols.schemes.log]
```

## Key Classes

### packages.resource-agent-hypervisor.hypervisor.uri.client.Uri3Client
> Thin hypervisor adapter over uri3 routing, scanning and graph utilities.
- **Methods**: 8
- **Key Methods**: packages.resource-agent-hypervisor.hypervisor.uri.client.Uri3Client.__init__, packages.resource-agent-hypervisor.hypervisor.uri.client.Uri3Client.resolve, packages.resource-agent-hypervisor.hypervisor.uri.client.Uri3Client.call, packages.resource-agent-hypervisor.hypervisor.uri.client.Uri3Client.scan, packages.resource-agent-hypervisor.hypervisor.uri.client.Uri3Client.logs, packages.resource-agent-hypervisor.hypervisor.uri.client.Uri3Client.schema, packages.resource-agent-hypervisor.hypervisor.uri.client.Uri3Client.graph, packages.resource-agent-hypervisor.hypervisor.uri.client.Uri3Client.nl2uri

### packages.resource-agent-hypervisor.hypervisor.core.Hypervisor
> Main Hypervisor controller.

Example:
    from hypervisor import Hypervisor
    hv = Hypervisor()
  
- **Methods**: 7
- **Key Methods**: packages.resource-agent-hypervisor.hypervisor.core.Hypervisor.__post_init__, packages.resource-agent-hypervisor.hypervisor.core.Hypervisor.from_config, packages.resource-agent-hypervisor.hypervisor.core.Hypervisor.start, packages.resource-agent-hypervisor.hypervisor.core.Hypervisor.stop, packages.resource-agent-hypervisor.hypervisor.core.Hypervisor.register_agent, packages.resource-agent-hypervisor.hypervisor.core.Hypervisor.status, packages.resource-agent-hypervisor.hypervisor.core.Hypervisor.__repr__

### packages.uri3.uri3.resolvers.router.Uri3Router
- **Methods**: 3
- **Key Methods**: packages.uri3.uri3.resolvers.router.Uri3Router.__init__, packages.uri3.uri3.resolvers.router.Uri3Router.resolve, packages.uri3.uri3.resolvers.router.Uri3Router.call

### hypervisor.contract_registry.models.ContractRegistry
- **Methods**: 3
- **Key Methods**: hypervisor.contract_registry.models.ContractRegistry.resource_by_uri, hypervisor.contract_registry.models.ContractRegistry.view_by_name, hypervisor.contract_registry.models.ContractRegistry.capability_by_name

### runtime_client.client.ResourceRuntimeClient
> Small HTTP client used by generated thin agents.

Expected runtime API:
- GET  /resources/read?uri=r
- **Methods**: 3
- **Key Methods**: runtime_client.client.ResourceRuntimeClient.__init__, runtime_client.client.ResourceRuntimeClient.read_resource, runtime_client.client.ResourceRuntimeClient.dispatch_command

### testenv.ssh_agent_host.mock_agent_server.Handler
- **Methods**: 3
- **Key Methods**: testenv.ssh_agent_host.mock_agent_server.Handler._json, testenv.ssh_agent_host.mock_agent_server.Handler.do_GET, testenv.ssh_agent_host.mock_agent_server.Handler.log_message
- **Inherits**: BaseHTTPRequestHandler

### uri3.graph.uri_graph.UriGraph
- **Methods**: 2
- **Key Methods**: uri3.graph.uri_graph.UriGraph.add_node, uri3.graph.uri_graph.UriGraph.add_edge

### uri3.resolvers.http_resolver.HttpResolver
- **Methods**: 2
- **Key Methods**: uri3.resolvers.http_resolver.HttpResolver.resolve, uri3.resolvers.http_resolver.HttpResolver.fetch

### packages.uri3.uri3.resolvers.env_resolver.EnvResolver
- **Methods**: 2
- **Key Methods**: packages.uri3.uri3.resolvers.env_resolver.EnvResolver.resolve, packages.uri3.uri3.resolvers.env_resolver.EnvResolver.call

### uri3.resolvers.python_resolver.PythonResolver
- **Methods**: 2
- **Key Methods**: uri3.resolvers.python_resolver.PythonResolver.resolve, uri3.resolvers.python_resolver.PythonResolver.call

### packages.uri3.uri3.resolvers.log_resolver.LogResolver
- **Methods**: 2
- **Key Methods**: packages.uri3.uri3.resolvers.log_resolver.LogResolver.resolve, packages.uri3.uri3.resolvers.log_resolver.LogResolver.read

### hypervisor.config.models.HypervisorConfig
- **Methods**: 2
- **Key Methods**: hypervisor.config.models.HypervisorConfig.from_dict, hypervisor.config.models.HypervisorConfig.to_dict

### packages.resource-agent-hypervisor.hypervisor.deployment_registry.models.DeploymentRegistry
- **Methods**: 2
- **Key Methods**: packages.resource-agent-hypervisor.hypervisor.deployment_registry.models.DeploymentRegistry.by_id, packages.resource-agent-hypervisor.hypervisor.deployment_registry.models.DeploymentRegistry.by_agent_ref

### packages.uri3.uri3.graph.adapters.browser_router.BrowserRouterAdapter
- **Methods**: 2
- **Key Methods**: packages.uri3.uri3.graph.adapters.browser_router.BrowserRouterAdapter.__init__, packages.uri3.uri3.graph.adapters.browser_router.BrowserRouterAdapter.execute

### packages.uri3.uri3.graph.models.GraphNode
- **Methods**: 2
- **Key Methods**: packages.uri3.uri3.graph.models.GraphNode.from_dict, packages.uri3.uri3.graph.models.GraphNode.to_dict

### packages.uri3.uri3.graph.models.WorkflowGraph
- **Methods**: 2
- **Key Methods**: packages.uri3.uri3.graph.models.WorkflowGraph.add_node, packages.uri3.uri3.graph.models.WorkflowGraph.to_dict

### packages.uri3.uri3.protocols.schemes.base.QueryOption
- **Methods**: 1
- **Key Methods**: packages.uri3.uri3.protocols.schemes.base.QueryOption.to_dict

### packages.uri3.uri3.protocols.schemes.base.SchemeSpec
- **Methods**: 1
- **Key Methods**: packages.uri3.uri3.protocols.schemes.base.SchemeSpec.to_dict

### packages.uri3.uri3.config.llm_profiles.LlmProfile
- **Methods**: 1
- **Key Methods**: packages.uri3.uri3.config.llm_profiles.LlmProfile.to_dict

### packages.uri3.uri3.resolvers.docker_resolver.DockerRef
- **Methods**: 1
- **Key Methods**: packages.uri3.uri3.resolvers.docker_resolver.DockerRef.to_dict

## Data Transformation Functions

Key functions that process and transform data:

### packages.uri3.uri3.logs.parsing.parse_json_entry
- **Output to**: line.strip, json.loads, isinstance, None.upper, data.get

### packages.uri3.uri3.logs.parsing.parse_text_entry
- **Output to**: line.strip, _TEXT_LOG_RE.match, match.groupdict, groups.get, None.upper

### packages.uri3.uri3.logs.parsing.parse_log_line
- **Output to**: line.strip, packages.uri3.uri3.logs.parsing.empty_entry, packages.uri3.uri3.logs.parsing.parse_json_entry, packages.uri3.uri3.logs.parsing.parse_text_entry, line.strip

### packages.uri3.uri3.logs.reader._parse_since
- **Output to**: value.strip, datetime.now, value.endswith, value.endswith, value.endswith

### uri3.validators.uri_validator.validate_uri
- **Output to**: uri3.protocols.parser.parse_uri, ValueError

### packages.uri3.uri3.validators.uri_tree_validator.validate_uri_tree
- **Output to**: packages.uri3.uri3.validators.uri_tree_validator.load_yaml, json.loads, Draft202012Validator, sorted, SCHEMA_PATH.read_text

### packages.uri3.uri3.docker.actions.compose._parse_ps_stdout
- **Output to**: stdout.splitlines, line.strip, parsed.append, json.loads, parsed.append

### uri3.protocols.parser.parse_uri
- **Output to**: urlparse, ParsedURI, ValueError, parse_qs

### packages.uri3.uri3.protocols.schemes.instance_parser._parse_log
- **Output to**: None.to_dict, packages.uri3.uri3.resolvers.log_resolver.parse_log_uri

### packages.uri3.uri3.protocols.schemes.instance_parser._parse_env
- **Output to**: packages.uri3.uri3.resolvers.env_resolver.resolve_env

### packages.uri3.uri3.protocols.schemes.instance_parser._parse_python
- **Output to**: uri3.resolvers.python_resolver.resolve_python

### packages.uri3.uri3.protocols.schemes.instance_parser._parse_llm
- **Output to**: uri3.resolvers.llm_resolver.resolve_llm

### packages.uri3.uri3.protocols.schemes.instance_parser._parse_pypi
- **Output to**: hypervisor.uri2llm.pypi_resolver.resolve_pypi

### packages.uri3.uri3.protocols.schemes.instance_parser._parse_http
- **Output to**: packages.uri3.uri3.resolvers.protocol_resolver.resolve_http_like

### packages.uri3.uri3.protocols.schemes.instance_parser._parse_a2a
- **Output to**: packages.uri3.uri3.resolvers.protocol_resolver.resolve_a2a

### packages.uri3.uri3.protocols.schemes.instance_parser._parse_mcp
- **Output to**: packages.uri3.uri3.resolvers.protocol_resolver.resolve_mcp

### packages.uri3.uri3.protocols.schemes.instance_parser._parse_docker
- **Output to**: packages.uri3.uri3.resolvers.docker_resolver.resolve_docker

### packages.uri3.uri3.protocols.schemes.instance_parser._parse_ssh
- **Output to**: packages.uri3.uri3.resolvers.ssh_resolver.resolve_ssh

### packages.uri3.uri3.protocols.schemes.instance_parser._parse_resource
- **Output to**: packages.uri3.uri3.resolvers.protocol_resolver.resolve_resource

### packages.uri3.uri3.protocols.schemes.instance_parser.parse_instance
- **Output to**: _SCHEME_PARSERS.get, ValueError, parser, packages.uri3.uri3.protocols.schemes.instance_parser._parse_resource

### packages.uri3.uri3.config.llm_profile_builder.parse_llm_query
- **Output to**: urlparse, parse_qs, float, int, query.get

### packages.uri3.uri3.resolvers.ssh_resolver.parse_ssh_uri
- **Output to**: urlparse, ValueError, ValueError, netloc.rsplit, host_port.rsplit

### packages.uri3.uri3.resolvers.docker_resolver.parse_docker_uri
- **Output to**: urlparse, parsed.path.lstrip, parse_qs, DockerRef, ValueError

### packages.uri3.uri3.resolvers.log_query.parse_query
- **Output to**: urlparse, ValueError, packages.uri3.uri3.resolvers.log_query.resolve_path, parse_qs

### packages.uri3.uri3.resolvers.log_resolver.parse_log_uri
- **Output to**: packages.uri3.uri3.resolvers.log_query.parse_query, LogRef, packages.uri3.uri3.resolvers.log_query.resolve_level, packages.uri3.uri3.resolvers.log_query.query_int, packages.uri3.uri3.resolvers.log_query.query_int

## Behavioral Patterns

### recursion_resolve
- **Type**: recursion
- **Confidence**: 0.90
- **Functions**: packages.uri3.uri3.resolvers.router.Uri3Router.resolve

### recursion_call
- **Type**: recursion
- **Confidence**: 0.90
- **Functions**: packages.uri3.uri3.resolvers.router.Uri3Router.call

### recursion_scan
- **Type**: recursion
- **Confidence**: 0.90
- **Functions**: packages.resource-agent-hypervisor.hypervisor.uri.client.Uri3Client.scan

### recursion_resolve_uri_values
- **Type**: recursion
- **Confidence**: 0.90
- **Functions**: packages.uri3.uri3.config.uri_yaml.resolve_uri_values

## Public API Surface

Functions exposed as public API (no underscore prefix):

- `packages.uri3.uri3.graph.graph_executor.run_workflow` - 39 calls
- `hypervisor.contract_registry.loader.load_contract_registry` - 33 calls
- `packages.uri3.uri3.config.llm_profiles.resolve_llm_profile` - 32 calls
- `meta_agent.planner.infer_intent` - 30 calls
- `packages.resource-agent-hypervisor.hypervisor.domain_pack.pack_writer.write_domain_pack` - 30 calls
- `uri3.graph.uri_graph.build_graph_from_tree` - 28 calls
- `hypervisor.config.models.HypervisorConfig.from_dict` - 26 calls
- `packages.resource-agent-hypervisor.meta_agent.cli.main` - 25 calls
- `packages.uri3.uri3.protocols.schemes.spec_registry.build_scheme_registry` - 25 calls
- `packages.nl2uri.nl2uri.graph_repair.sanitize_node` - 25 calls
- `packages.nl2uri.nl2uri.graph_repair.repair_graph_body` - 25 calls
- `generator.model.load_agent_spec` - 24 calls
- `packages.uri3.uri3.graph.graph_serializer.normalize_graph_payload` - 24 calls
- `packages.uri3.uri3.resolvers.docker_resolver.parse_docker_uri` - 23 calls
- `packages.uri3.uri3.graph.adapters.browser_playwright.PlaywrightBrowserAdapter.execute` - 23 calls
- `packages.uri3.uri3.cli.scan` - 21 calls
- `packages.uri3.uri3.logs.reader.summarize_logs` - 18 calls
- `packages.uri3.uri3.graph.adapters.registry.AssertionAdapter.execute` - 18 calls
- `packages.uri3.uri3.resolvers.env_resolver.call_env` - 17 calls
- `packages.resource-agent-factory.generator.agent_generator.generate_agent` - 17 calls
- `packages.resource-agent-hypervisor.hypervisor.config.defaults.apply_builtin_defaults` - 17 calls
- `hypervisor.config.env.apply_structured_env_overrides` - 17 calls
- `packages.resource-agent-hypervisor.hypervisor.deployment_registry.lifecycle.stop_agent` - 17 calls
- `packages.resource-agent-hypervisor.hypervisor.deployment_registry.status.deployment_from_uri_tree` - 17 calls
- `packages.uri3.uri3.logs.parsing.parse_json_entry` - 16 calls
- `packages.uri3.uri3.resolvers.log_resolver.parse_log_uri` - 16 calls
- `packages.resource-agent-hypervisor.meta_agent.orchestrator.validate_repair_generate` - 16 calls
- `packages.resource-agent-hypervisor.hypervisor.cli_commands.deploy_agent` - 16 calls
- `packages.uri3.uri3.config.docker_stacks.resolve_agent_stack` - 15 calls
- `packages.nl2uri.nl2uri.pipeline.run_full_pipeline` - 15 calls
- `packages.resource-agent-hypervisor.hypervisor.cli_commands.run_local_agent` - 15 calls
- `packages.resource-agent-hypervisor.hypervisor.contract_registry.merge_helpers.merge_views_contract` - 15 calls
- `packages.resource-agent-hypervisor.hypervisor.deployment_registry.lifecycle.run_agent` - 15 calls
- `packages.resource-agent-hypervisor.hypervisor.deployment_registry.env.build_deployment_env_map` - 15 calls
- `packages.uri3.uri3.graph.conditions.evaluate_condition` - 15 calls
- `packages.nl2uri.nl2uri.cli.task` - 15 calls
- `packages.nl2uri.nl2uri.cli.graph` - 15 calls
- `packages.nl2uri.nl2uri.graph_planner.plan_workflow_graph` - 15 calls
- `packages.uri3.uri3.graph.models.GraphNode.from_dict` - 15 calls
- `meta_agent.repair.rules.repair_resource_read_capability` - 14 calls

## System Interactions

How components interact:

```mermaid
graph TD
    from_dict --> cls
    from_dict --> str
    from_dict --> get
    from_dict --> bool
    main --> ArgumentParser
    main --> add_subparsers
    main --> add_parser
    main --> add_argument
    build_scheme_registr --> spec
    execute --> _session_state
    execute --> get
    execute --> execute
    execute --> urlparse
    execute --> str
    scan --> command
    scan --> Argument
    scan --> Option
    scan --> echo
    scan --> scan_shortcuts
    execute --> resolve_ref
    execute --> endswith
    task --> command
    task --> Option
    graph --> command
    graph --> Option
    tree --> command
    tree --> Option
    generate --> command
    generate --> Option
    spec --> SchemeSpec
```

## Reverse Engineering Guidelines

1. **Entry Points**: Start analysis from the entry points listed above
2. **Core Logic**: Focus on classes with many methods
3. **Data Flow**: Follow data transformation functions
4. **Process Flows**: Use the flow diagrams for execution paths
5. **API Surface**: Public API functions reveal the interface

## Context for LLM

Maintain the identified architectural patterns and public API surface when suggesting changes.