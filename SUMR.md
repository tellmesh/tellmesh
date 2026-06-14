# Resource Agent System v0.6

SUMD - Structured Unified Markdown Descriptor for AI-aware project refactorization

## Contents

- [Metadata](#metadata)
- [Architecture](#architecture)
- [Workflows](#workflows)
- [Dependencies](#dependencies)
- [Call Graph](#call-graph)
- [Test Contracts](#test-contracts)
- [Refactoring Analysis](#refactoring-analysis)
- [Intent](#intent)

## Metadata

- **name**: `resource-agent-system`
- **version**: `0.5.13`
- **python_requires**: `>=3.10`
- **license**: Apache-2.0
- **ai_model**: `openrouter/qwen/qwen3-coder-next`
- **ecosystem**: SUMD + DOQL + testql + taskfile
- **generated_from**: pyproject.toml, Makefile, testql(3), app.doql.less, goal.yaml, .env.example, Dockerfile, docker-compose.yml, project/(5 analysis files)

## Architecture

```
SUMD (description) → DOQL/source (code) → taskfile (automation) → testql (verification)
```

### DOQL Application Declaration (`app.doql.less`)

```less markpact:doql path=app.doql.less
// LESS format — define @variables here as needed

app {
  name: resource-agent-system;
  version: 0.5.13;
}

dependencies {
  runtime: "fastapi>=0.115, httpx>=0.27, jinja2>=3.1, jsonschema>=4.23, pydantic>=2.0, python-dotenv>=1.0.0, pyyaml>=6.0, typer>=0.12";
  dev: "pytest>=7.0, pytest-cov>=4.0, pytest-asyncio>=0.21.0, ruff>=0.1.0, mypy>=1.0, build>=1.0, goal>=2.1.0, costs>=0.1.20, pfix>=0.1.60, rich>=13.0.0";
  browser: playwright>=1.40;
  windows: pywinauto>=0.6;
  server: uvicorn>=0.27;
}

interface[type="api"] {
  type: rest;
  framework: fastapi;
}

interface[type="cli"] {
  framework: argparse;
}
interface[type="cli"] page[name="hypervisor"] {
  entry: hypervisor.cli:main;
}
interface[type="cli"] page[name="uri3"] {
  entry: uri3.cli:main;
}
interface[type="cli"] page[name="uri2ops"] {
  entry: uri2ops.cli:main;
}
interface[type="cli"] page[name="uri2flow"] {
  entry: uri2flow.cli:main;
}
interface[type="cli"] page[name="touri"] {
  entry: touri.cli:main;
}
interface[type="cli"] page[name="nl2uri"] {
  entry: nl2uri.cli:main;
}
interface[type="cli"] page[name="nl2a"] {
  entry: nl2a.cli:main;
}

workflow[name="validate"] {
  trigger: manual;
  step-1: run cmd=python -m generator.validate contracts;
}

workflow[name="generate"] {
  trigger: manual;
  step-1: run cmd=python -m generator.agent_generator contracts/agents/*.yaml;
}

workflow[name="verify"] {
  trigger: manual;
  step-1: run cmd=python -m generator.verify agents/generated;
}

workflow[name="test"] {
  trigger: manual;
  step-1: run cmd=pytest -q;
}

workflow[name="uri2flow-test"] {
  trigger: manual;
  step-1: run cmd=pytest tests/uri2flow -q;
}

workflow[name="uri2flow-validate"] {
  trigger: manual;
  step-1: run cmd=uri2flow validate examples/15_compact_uri_flow/weather.uri.flow.yaml;
}

workflow[name="uri2flow-expand"] {
  trigger: manual;
  step-1: run cmd=mkdir -p output;
  step-2: run cmd=uri2flow expand examples/15_compact_uri_flow/weather.uri.flow.yaml --out output/weather.uri.graph.yaml;
}

workflow[name="uri3-flow-dry-run"] {
  trigger: manual;
  step-1: run cmd=uri3 run-flow examples/17_flow_vs_graph/weather.uri.flow.yaml --dry-run;
}

workflow[name="nl2uri-flow-validate"] {
  trigger: manual;
  step-1: run cmd=nl2uri flow -p "wygeneruj agenta pogodowego, uruchom go lokalnie i sprawdź health w Chrome" --validate;
}

workflow[name="example-18"] {
  trigger: manual;
  step-1: run cmd=bash examples/18_llm_flow_planner/run.sh;
}

workflow[name="touri-test"] {
  trigger: manual;
  step-1: run cmd=pytest tests/touri -q;
}

workflow[name="touri-demo"] {
  trigger: manual;
  step-1: run cmd=touri validate examples/20_touri_capabilities/weather_forecast.uri.capability.yaml;
  step-2: run cmd=touri list examples/20_touri_capabilities;
  step-3: run cmd=touri call weather://forecast/Gdansk/14/html --registry examples/20_touri_capabilities;
  step-4: run cmd=touri call echo://Adam --registry examples/20_touri_capabilities;
}

workflow[name="voice-test"] {
  trigger: manual;
  step-1: run cmd=pytest tests/touri/test_voice_capabilities.py -q;
}

workflow[name="voice-demo"] {
  trigger: manual;
  step-1: run cmd=touri validate examples/21_touri_voice/stt_mock.uri.capability.yaml;
  step-2: run cmd=touri list examples/21_touri_voice;
  step-3: run cmd=touri call stt://mock/transcribe --registry examples/21_touri_voice --payload '{"text":"otwórz Chrome i sprawdź health"}';
  step-4: run cmd=touri call voice://command/from-text --registry examples/21_touri_voice --payload '{"text":"wygeneruj agenta pogodowego, uruchom go lokalnie i sprawdź health w Chrome"}';
  step-5: run cmd=touri call tts://mock/speak --registry examples/21_touri_voice --payload '{"text":"Agent działa poprawnie"}';
}

workflow[name="uri-tree"] {
  trigger: manual;
  step-1: run cmd=python -m nl2uri.cli --no-llm -p "$(WEATHER_PROMPT)" --out domains/weather_map/uri_tree.yaml;
}

workflow[name="graph"] {
  trigger: manual;
  step-1: run cmd=python -m uri3.cli graph domains/weather_map/uri_tree.yaml;
}

workflow[name="nl2a-weather"] {
  trigger: manual;
  step-1: run cmd=python -m nl2a.cli --no-llm -p "$(WEATHER_PROMPT)";
}

workflow[name="run-user-agent"] {
  trigger: manual;
  step-1: run cmd=uvicorn agents.generated.user_agent.main:app --reload --port 8101;
}

workflow[name="run-meta-agent"] {
  trigger: manual;
  step-1: run cmd=uvicorn meta_agent.api:app --reload --port 8200;
}

workflow[name="meta-plan"] {
  trigger: manual;
  step-1: run cmd=python -m meta_agent.cli plan "Stwórz agenta do obsługi zamówień z odczytem zamówienia, historią i tworzeniem zamówienia";
}

workflow[name="meta-pipeline"] {
  trigger: manual;
  step-1: run cmd=python -m meta_agent.cli pipeline "Stwórz agenta do obsługi zamówień z odczytem zamówienia, historią i tworzeniem zamówienia";
}

workflow[name="meta-repair"] {
  trigger: manual;
  step-1: run cmd=python -m meta_agent.cli repair examples/05_meta_repair/broken_agent.yaml --write;
}

workflow[name="docker-ssh-up"] {
  trigger: manual;
  step-1: run cmd=python -m hypervisor.cli call 'docker://stack/ssh-testenv?action=up&build=1';
}

workflow[name="docker-ssh-down"] {
  trigger: manual;
  step-1: run cmd=python -m hypervisor.cli call 'docker://stack/ssh-testenv?action=down&remove_volumes=1';
}

workflow[name="docker-testenv-up"] {
  trigger: manual;
  step-1: depend target=docker-ssh-up;
}

workflow[name="docker-testenv-down"] {
  trigger: manual;
  step-1: depend target=docker-ssh-down;
}

workflow[name="scan-http"] {
  trigger: manual;
  step-1: run cmd=python -m uri3.cli scan http;
}

workflow[name="scan-ssh"] {
  trigger: manual;
  step-1: run cmd=HYPERVISOR_SSH_PASSWORD=$${HYPERVISOR_SSH_PASSWORD:-deploy} python -m uri3.cli scan ssh;
}

workflow[name="scan-all"] {
  trigger: manual;
  step-1: run cmd=HYPERVISOR_SSH_PASSWORD=$${HYPERVISOR_SSH_PASSWORD:-deploy} python -m uri3.cli scan --all;
}

workflow[name="evolution-check"] {
  trigger: manual;
  step-1: run cmd=python -m hypervisor.evolution.cli examples/08_evolution/proposals/add_orders_agent.yaml examples/08_evolution/proposals/add_invoices_agent.yaml;
}

workflow[name="examples"] {
  trigger: manual;
  step-1: run cmd=echo "See examples/README.md for the full catalog (01–09).";
}

workflow[name="run-weather-agent"] {
  trigger: manual;
  step-1: run cmd=python -m hypervisor.cli run-agent weather-map-agent.local;
}

workflow[name="clean"] {
  trigger: manual;
  step-1: run cmd=rm -rf agents/generated/* output/* .pytest_cache;
  step-2: run cmd=find . -type d -name __pycache__ -prune -exec rm -rf {} +;
}

tests {
  import: testql-scenarios/**/*.testql.toon.yaml;
}

env_vars {
  keys: OPENROUTER_API_KEY, LLM_MODEL, LLM_BASE_URL, LLM_TEMPERATURE, LLM_MAX_TOKENS, RESOURCE_RUNTIME_URL, HYPERVISOR_SSH_PASSWORD;
}

deploy {
  target: docker-compose;
  compose_file: docker-compose.yml;
}

environment[name="local"] {
  runtime: docker-compose;
  env_file: .env;
  template_file: .env.example;
  python_version: >=3.10;
  vars: HYPERVISOR_SSH_PASSWORD, LLM_BASE_URL, LLM_MAX_TOKENS, LLM_MODEL, LLM_TEMPERATURE, OPENROUTER_API_KEY, RESOURCE_RUNTIME_URL;
  runtime_llm: OPENROUTER_API_KEY;
}
```

## Workflows

## Dependencies

### Runtime

```text markpact:deps python
fastapi>=0.115
httpx>=0.27
jinja2>=3.1
jsonschema>=4.23
pydantic>=2.0
python-dotenv>=1.0.0
pyyaml>=6.0
typer>=0.12
```

### Development

```text markpact:deps python scope=dev
pytest>=7.0
pytest-cov>=4.0
pytest-asyncio>=0.21.0
ruff>=0.1.0
mypy>=1.0
build>=1.0
goal>=2.1.0
costs>=0.1.20
pfix>=0.1.60
rich>=13.0.0
```

## Call Graph

*395 nodes · 500 edges · 123 modules · CC̄=3.8*

### Hubs (by degree)

| Function | CC | in | out | total |
|----------|----|----|-----|-------|
| `create_app` *(in uri2ops.server.app)* | 1 | 1 | 62 | **63** |
| `register` *(in packages.uri3.uri3.cli.commands.discovery)* | 1 | 0 | 47 | **47** |
| `run_workflow` *(in packages.uri3.uri3.graph.graph_executor)* | 22 ⚠ | 5 | 40 | **45** |
| `print` *(in examples.21_touri_voice.run)* | 0 | 43 | 0 | **43** |
| `service_result` *(in packages.uri3.uri3.results.service_result)* | 3 | 33 | 10 | **43** |
| `list` *(in uri2ops.operation_registry.models.OperationRegistry)* | 1 | 40 | 2 | **42** |
| `resolve_llm_profile` *(in packages.uri3.uri3.config.llm_profiles)* | 10 ⚠ | 4 | 32 | **36** |
| `plan_flow` *(in packages.nl2uri.nl2uri.flow_planner)* | 12 ⚠ | 4 | 29 | **33** |

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/wronai/hypervisor
# generated in 0.21s
# nodes: 395 | edges: 500 | modules: 123
# CC̄=3.8

HUBS[20]:
  uri2ops.server.app.create_app
    CC=1  in:1  out:62  total:63
  packages.uri3.uri3.cli.commands.discovery.register
    CC=1  in:0  out:47  total:47
  packages.uri3.uri3.graph.graph_executor.run_workflow
    CC=22  in:5  out:40  total:45
  examples.21_touri_voice.run.print
    CC=0  in:43  out:0  total:43
  packages.uri3.uri3.results.service_result.service_result
    CC=3  in:33  out:10  total:43
  uri2ops.operation_registry.models.OperationRegistry.list
    CC=1  in:40  out:2  total:42
  packages.uri3.uri3.config.llm_profiles.resolve_llm_profile
    CC=10  in:4  out:32  total:36
  packages.nl2uri.nl2uri.flow_planner.plan_flow
    CC=12  in:4  out:29  total:33
  packages.touri.touri.data_quality.apply_data_quality
    CC=18  in:2  out:31  total:33
  meta_agent.planner.infer_intent
    CC=9  in:1  out:30  total:31
  uri3.graph.uri_graph.build_graph_from_tree
    CC=10  in:2  out:28  total:30
  packages.uri2flow.uri2flow.parser._parse_step
    CC=10  in:1  out:29  total:30
  packages.nl2uri.nl2uri.flow_repair.extract_flow_payload
    CC=20  in:1  out:28  total:29
  packages.uri3.uri3.resolvers.docker_resolver.parse_docker_uri
    CC=12  in:5  out:23  total:28
  packages.touri.touri.backends.python_backend.call_python_backend
    CC=9  in:3  out:25  total:28
  packages.nl2uri.nl2uri.flow_repair._ensure_step_ids
    CC=19  in:1  out:27  total:28
  packages.uri3.uri3.config.repo_root.find_repo_root
    CC=4  in:24  out:4  total:28
  packages.nl2uri.nl2uri.graph_repair.repair_graph_body
    CC=12  in:1  out:25  total:26
  packages.nl2uri.nl2uri.graph_repair.sanitize_node
    CC=16  in:1  out:25  total:26
  generator.model.load_agent_spec
    CC=7  in:2  out:24  total:26

MODULES:
  examples.21_touri_voice.run  [1 funcs]
    print  CC=0  out:0
  generator.hashutil  [1 funcs]
    file_sha256  CC=1  out:4
  generator.model  [1 funcs]
    load_agent_spec  CC=7  out:24
  generator.validate  [3 funcs]
    iter_agent_specs  CC=3  out:6
    main  CC=7  out:9
    validate_agent  CC=11  out:10
  generator.verify  [3 funcs]
    main  CC=9  out:10
    verify_generated  CC=6  out:5
    verify_generated_agent  CC=7  out:10
  hypervisor.contract_registry.registry_builder  [1 funcs]
    write_registry_manifest  CC=2  out:6
  hypervisor.uri2llm.pypi_resolver  [1 funcs]
    resolve_pypi  CC=5  out:6
  meta_agent.api  [4 funcs]
    generate  CC=2  out:6
    proposal_from_prompt  CC=2  out:6
    repair  CC=2  out:5
    validate  CC=2  out:5
  meta_agent.planner  [4 funcs]
    infer_intent  CC=9  out:30
    intent_to_agent_spec  CC=8  out:11
    package_name  CC=3  out:6
    singularize  CC=4  out:3
  meta_agent.repair.pipeline  [1 funcs]
    repair_agent_spec  CC=2  out:12
  nl2a.cli  [1 funcs]
    generate  CC=1  out:5
  nl2uri.writer  [1 funcs]
    write_uri_tree  CC=1  out:4
  packages.nl2uri.nl2uri.cli  [14 funcs]
    _default_use_llm  CC=1  out:2
    _emit  CC=2  out:3
    _plan_command  CC=6  out:7
    _resolve_use_llm  CC=5  out:2
    _validate_flow_payload  CC=2  out:5
    classify  CC=1  out:5
    flow  CC=6  out:17
    generate  CC=4  out:14
    graph  CC=5  out:15
    list_cmd  CC=1  out:5
  packages.nl2uri.nl2uri.domain_planner  [1 funcs]
    plan_from_prompt  CC=7  out:11
  packages.nl2uri.nl2uri.flow_planner  [1 funcs]
    plan_flow  CC=12  out:29
  packages.nl2uri.nl2uri.flow_planner_llm  [3 funcs]
    build_flow_planner_system_prompt  CC=1  out:6
    call_flow_planner_llm  CC=4  out:9
    plan_flow_with_llm  CC=3  out:6
  packages.nl2uri.nl2uri.flow_repair  [11 funcs]
    _ensure_step_ids  CC=19  out:27
    _needs_explicit_ids  CC=4  out:4
    _node_to_compact_step  CC=13  out:16
    _nodes_to_compact_steps  CC=4  out:3
    _normalize_step_raw  CC=10  out:14
    _supported_scheme  CC=2  out:2
    extract_flow_payload  CC=20  out:28
    repair_and_validate_flow  CC=2  out:4
    repair_flow_body  CC=8  out:17
    sanitize_flow_step  CC=18  out:24
  packages.nl2uri.nl2uri.graph_planner  [11 funcs]
    _detect_agent_id  CC=3  out:3
    _detect_health_uri  CC=4  out:6
    _slug  CC=2  out:3
    plan_auto  CC=1  out:2
    plan_by_kind  CC=2  out:3
    plan_list  CC=2  out:4
    plan_single  CC=4  out:6
    plan_task  CC=3  out:7
    plan_tree  CC=9  out:14
    plan_workflow_graph  CC=12  out:15
  packages.nl2uri.nl2uri.graph_planner_llm  [3 funcs]
    build_graph_planner_system_prompt  CC=2  out:5
    call_graph_planner_llm  CC=4  out:9
    plan_graph_with_llm  CC=4  out:7
  packages.nl2uri.nl2uri.graph_repair  [8 funcs]
    _coerce_operation  CC=5  out:6
    _sanitize_nodes  CC=12  out:8
    _slug  CC=2  out:3
    extract_graph_payload  CC=14  out:10
    normalize_to_kind  CC=12  out:14
    repair_and_validate_graph  CC=13  out:12
    repair_graph_body  CC=12  out:25
    sanitize_node  CC=16  out:25
  packages.nl2uri.nl2uri.llm_planner  [1 funcs]
    llm_plan  CC=2  out:4
  packages.nl2uri.nl2uri.output_classifier  [1 funcs]
    classify_output_kind  CC=23  out:16
  packages.nl2uri.nl2uri.pipeline  [4 funcs]
    _append_pipeline_logs  CC=2  out:4
    generate_tree  CC=1  out:1
    run_full_pipeline  CC=3  out:15
    run_generate_pipeline  CC=4  out:13
  packages.nl2uri.nl2uri.planner  [1 funcs]
    rule_based_plan  CC=1  out:2
  packages.nl2uri.nl2uri.planner_llm  [2 funcs]
    call_openrouter  CC=4  out:8
    extract_json  CC=3  out:8
  packages.nl2uri.nl2uri.planner_templates  [5 funcs]
    deterministic_weather_plan  CC=2  out:2
    generic_plan  CC=1  out:3
    is_weather_prompt  CC=1  out:2
    llm_uri_from_env  CC=6  out:7
    slug  CC=2  out:3
  packages.nl2uri.nl2uri.planner_validation  [3 funcs]
    is_structured_uri_tree  CC=10  out:13
    normalize_llm_tree  CC=7  out:12
    validate_tree_data  CC=2  out:6
  packages.resource-agent-factory.generator.agent_generator  [3 funcs]
    expand_paths  CC=4  out:7
    generate_agent  CC=5  out:17
    main  CC=5  out:4
  packages.resource-agent-factory.generator.header  [3 funcs]
    contract_source_ref  CC=3  out:7
    dockerfile_header  CC=1  out:0
    python_file_header  CC=1  out:0
  packages.resource-agent-factory.generator.paths  [1 funcs]
    project_root  CC=1  out:1
  packages.resource-agent-hypervisor.hypervisor.deployment_registry.lifecycle  [2 funcs]
    _repo_root  CC=2  out:3
    agent_status  CC=5  out:10
  packages.resource-agent-hypervisor.hypervisor.deployment_registry.run_plans  [1 funcs]
    build_run_plan  CC=5  out:7
  packages.resource-agent-hypervisor.hypervisor.deployment_registry.selector  [1 funcs]
    resolve_deployment  CC=7  out:9
  packages.resource-agent-hypervisor.hypervisor.deployment_registry.status  [1 funcs]
    sync_from_uri_tree  CC=2  out:4
  packages.resource-agent-hypervisor.hypervisor.domain_pack.generator  [1 funcs]
    generate_domain_pack  CC=1  out:3
  packages.resource-agent-hypervisor.meta_agent.orchestrator  [2 funcs]
    asdict_result  CC=1  out:0
    save_proposal_from_prompt  CC=2  out:6
  packages.touri.touri.backends.mock_backend  [1 funcs]
    call_mock_backend  CC=1  out:1
  packages.touri.touri.backends.python_backend  [2 funcs]
    _split_python_uri  CC=3  out:5
    call_python_backend  CC=9  out:25
  packages.touri.touri.backends.shell_backend  [1 funcs]
    call_shell_backend  CC=1  out:2
  packages.touri.touri.data_quality  [1 funcs]
    apply_data_quality  CC=18  out:31
  packages.touri.touri.loaders.registry_loader  [1 funcs]
    load_registry  CC=2  out:4
  packages.touri.touri.matcher  [3 funcs]
    match_uri  CC=3  out:4
    require_match  CC=2  out:2
    template_to_regex  CC=1  out:3
  packages.touri.touri_examples.validators  [3 funcs]
    always_pass  CC=1  out:1
    low_confidence_backend  CC=1  out:2
    reject_low_confidence  CC=4  out:6
  packages.uri2flow.uri2flow.cli  [5 funcs]
    build_parser  CC=1  out:14
    cmd_expand  CC=3  out:8
    cmd_print  CC=1  out:4
    cmd_validate  CC=2  out:4
    main  CC=1  out:3
  packages.uri2flow.uri2flow.expander  [4 funcs]
    _edges_from_depends  CC=4  out:2
    _node_from_step  CC=11  out:3
    dump_yaml  CC=1  out:1
    expand_flow  CC=6  out:8
  packages.uri2flow.uri2flow.parser  [4 funcs]
    _as_list  CC=5  out:5
    _parse_step  CC=10  out:29
    load_flow  CC=3  out:6
    parse_flow  CC=12  out:16
  packages.uri2flow.uri2flow.resolver  [9 funcs]
    _defaults_from_entry  CC=3  out:7
    _defaults_from_patterns  CC=7  out:7
    _defaults_from_scheme  CC=3  out:5
    _fallback_defaults  CC=4  out:5
    _find_repo_root  CC=7  out:7
    _load_flow_defaults_config  CC=4  out:6
    _match_pattern  CC=2  out:3
    _pattern_to_regex  CC=4  out:8
    default_operation_for_uri  CC=3  out:4
  packages.uri2flow.uri2flow.utils  [4 funcs]
    node_id_from_uri  CC=5  out:7
    path_parts  CC=4  out:4
    scheme_of  CC=1  out:1
    slugify  CC=2  out:4
  packages.uri2flow.uri2flow.validator  [3 funcs]
    validate_expanded_flow  CC=2  out:5
    validate_flow  CC=11  out:5
    validate_flow_document  CC=10  out:9
  packages.uri3.uri3.cli.commands.discovery  [1 funcs]
    register  CC=1  out:47
  packages.uri3.uri3.cli.commands.explain  [2 funcs]
    _render  CC=12  out:25
    register  CC=1  out:7
  packages.uri3.uri3.cli.commands.flow  [3 funcs]
    expand_flow_cmd  CC=3  out:9
    register  CC=1  out:11
    run_flow_cmd  CC=6  out:20
  packages.uri3.uri3.cli.commands.graph  [1 funcs]
    register  CC=1  out:5
  packages.uri3.uri3.cli.commands.resolve  [1 funcs]
    register  CC=1  out:24
  packages.uri3.uri3.cli.commands.workflow  [1 funcs]
    register  CC=1  out:20
  packages.uri3.uri3.cli.helpers  [1 funcs]
    list_payload  CC=2  out:3
  packages.uri3.uri3.config.cli_shortcuts  [5 funcs]
    cli_config_path  CC=1  out:1
    cli_examples  CC=3  out:3
    load_cli_config  CC=2  out:3
    resolve_scan_target  CC=4  out:4
    scan_shortcuts  CC=4  out:6
  packages.uri3.uri3.config.docker_stacks  [4 funcs]
    docker_config_path  CC=1  out:1
    load_docker_config  CC=2  out:3
    resolve_agent_stack  CC=4  out:15
    resolve_stack  CC=5  out:13
  packages.uri3.uri3.config.llm_profile_builder  [4 funcs]
    chosen_profile_name  CC=3  out:2
    normalize_model_name  CC=2  out:2
    parse_llm_query  CC=7  out:6
    resolve_profile_api_key  CC=4  out:4
  packages.uri3.uri3.config.llm_profiles  [3 funcs]
    llm_config_path  CC=1  out:1
    load_llm_config  CC=2  out:3
    resolve_llm_profile  CC=10  out:32
  packages.uri3.uri3.config.repo_root  [4 funcs]
    _walk_up  CC=7  out:6
    config_repo_root  CC=3  out:4
    find_repo_root  CC=4  out:4
    repo_root  CC=1  out:1
  packages.uri3.uri3.config.ssh_auth  [6 funcs]
    _password_from_env_file  CC=5  out:4
    _resolve_password_value  CC=8  out:10
    load_ssh_config  CC=2  out:3
    resolve_ssh_password  CC=12  out:13
    ssh_auth_hint  CC=3  out:2
    ssh_config_path  CC=1  out:1
  packages.uri3.uri3.config.uri_yaml  [3 funcs]
    is_uri  CC=4  out:3
    load_uri_yaml  CC=2  out:5
    resolve_uri_values  CC=15  out:13
  packages.uri3.uri3.docker.actions.compose  [8 funcs]
    _parse_ps_stdout  CC=4  out:5
    compose_base  CC=3  out:2
    control_compose  CC=6  out:6
    control_compose_down  CC=2  out:3
    control_compose_lifecycle  CC=1  out:2
    control_compose_logs  CC=1  out:3
    control_compose_ps  CC=3  out:4
    control_compose_up  CC=9  out:8
  packages.uri3.uri3.docker.actions.container  [3 funcs]
    _container_name  CC=2  out:0
    control_container  CC=8  out:9
    handles_container_action  CC=3  out:1
  packages.uri3.uri3.docker.compose_generator  [2 funcs]
    build_generate_plan  CC=2  out:9
    write_generated_compose  CC=1  out:6
  packages.uri3.uri3.docker.controller  [1 funcs]
    control_docker  CC=11  out:11
  packages.uri3.uri3.docker.runner  [1 funcs]
    run_command  CC=4  out:5
  packages.uri3.uri3.graph.adapters.browser_mock  [2 funcs]
    execute  CC=8  out:7
    json_dumps  CC=1  out:1
  packages.uri3.uri3.graph.adapters.browser_playwright  [3 funcs]
    execute  CC=11  out:23
    _session_state  CC=1  out:1
    close_playwright_session  CC=5  out:8
  packages.uri3.uri3.graph.adapters.browser_router  [4 funcs]
    execute  CC=2  out:4
    _playwright_ready  CC=3  out:5
    cleanup_browser_adapters  CC=2  out:2
    resolve_browser_mode  CC=5  out:3
  packages.uri3.uri3.graph.adapters.registry  [2 funcs]
    execute  CC=11  out:6
    _operator_adapter  CC=2  out:3
  packages.uri3.uri3.graph.adapters.uri2ops_adapter  [8 funcs]
    execute  CC=3  out:13
    _artifact_suffix  CC=9  out:0
    _attach_workflow_artifact  CC=3  out:6
    _registry_operation  CC=1  out:1
    _registry_scheme  CC=2  out:0
    _runtime_context  CC=1  out:3
    _use_legacy_browser_adapter  CC=1  out:2
    resolve_operator_adapter  CC=2  out:1
  packages.uri3.uri3.graph.artifacts  [3 funcs]
    artifact_path  CC=1  out:0
    artifact_uri  CC=1  out:0
    write_artifact  CC=2  out:6
  packages.uri3.uri3.graph.dependency_graph  [3 funcs]
    dependency_summary  CC=8  out:7
    detect_cycles  CC=15  out:7
    topological_sort  CC=13  out:13
  packages.uri3.uri3.graph.event_log  [2 funcs]
    append_workflow_event  CC=1  out:6
    workflow_event_path  CC=1  out:0
  packages.uri3.uri3.graph.execution_models  [1 funcs]
    utc_now_iso  CC=1  out:3
  packages.uri3.uri3.graph.graph_executor  [2 funcs]
    build_execution_plan  CC=3  out:10
    run_workflow  CC=22  out:40
  packages.uri3.uri3.graph.graph_serializer  [3 funcs]
    edges_from_depends_on  CC=4  out:5
    normalize_graph_payload  CC=12  out:24
    task_steps_to_graph  CC=3  out:7
  packages.uri3.uri3.graph.graph_validator  [4 funcs]
    _schema_path  CC=1  out:1
    load_workflow_graph  CC=10  out:11
    validate_workflow_graph  CC=9  out:13
    validate_workflow_schema  CC=2  out:7
  packages.uri3.uri3.graph.models  [1 funcs]
    from_dict  CC=5  out:15
  packages.uri3.uri3.graph.operation_registry  [6 funcs]
    allowed_operations  CC=1  out:2
    effective_kind  CC=2  out:2
    operation_registry_summary  CC=2  out:5
    requires_approval  CC=1  out:1
    scheme_from_uri  CC=2  out:1
    validate_node_operation  CC=2  out:5
  packages.uri3.uri3.graph.policy  [1 funcs]
    can_execute_step  CC=6  out:2
  packages.uri3.uri3.logs.filters  [7 funcs]
    entry_timestamp  CC=4  out:5
    level_rank  CC=3  out:2
    matches_filters  CC=4  out:4
    matches_grep  CC=4  out:5
    matches_level  CC=2  out:3
    matches_logger  CC=3  out:4
    matches_time_window  CC=7  out:1
  packages.uri3.uri3.logs.parsing  [4 funcs]
    empty_entry  CC=1  out:0
    parse_json_entry  CC=14  out:16
    parse_log_line  CC=4  out:5
    parse_text_entry  CC=5  out:8
  packages.uri3.uri3.logs.reader  [5 funcs]
    _parse_since  CC=7  out:14
    read_logs  CC=9  out:10
    read_logs_result  CC=3  out:2
    resolve_log_path  CC=4  out:3
    summarize_logs  CC=6  out:18
  packages.uri3.uri3.logs.writer  [1 funcs]
    append_log  CC=3  out:9
  packages.uri3.uri3.protocols.schemes.analyze  [3 funcs]
    _analyze_query  CC=14  out:10
    analyze_uri  CC=2  out:7
    describe_uri  CC=2  out:3
  packages.uri3.uri3.protocols.schemes.base  [2 funcs]
    to_dict  CC=4  out:2
    to_dict  CC=2  out:5
  packages.uri3.uri3.protocols.schemes.instance_parser  [13 funcs]
    _parse_a2a  CC=1  out:1
    _parse_docker  CC=1  out:1
    _parse_env  CC=1  out:1
    _parse_http  CC=1  out:1
    _parse_llm  CC=1  out:1
    _parse_log  CC=1  out:2
    _parse_mcp  CC=1  out:1
    _parse_pypi  CC=1  out:1
    _parse_python  CC=1  out:1
    _parse_resource  CC=1  out:1
  packages.uri3.uri3.protocols.schemes.spec_registry  [4 funcs]
    get_scheme_schema  CC=3  out:5
    is_concrete_uri  CC=4  out:3
    list_schemes  CC=5  out:5
    query_names  CC=2  out:3
  packages.uri3.uri3.resolvers.dispatch  [2 funcs]
    _resolve_docker  CC=1  out:1
    resolve_target  CC=3  out:4
  packages.uri3.uri3.resolvers.docker_resolver  [6 funcs]
    _bool  CC=3  out:2
    _first  CC=2  out:1
    _int  CC=3  out:2
    parse_docker_uri  CC=12  out:23
    resolve_docker  CC=2  out:4
    resolve_docker_target  CC=1  out:1
  packages.uri3.uri3.resolvers.env_resolver  [6 funcs]
    call  CC=1  out:1
    resolve  CC=1  out:1
    _env_var_name  CC=3  out:3
    _first  CC=2  out:1
    call_env  CC=8  out:17
    resolve_env  CC=1  out:2
  packages.uri3.uri3.resolvers.explain  [7 funcs]
    _find_repo_root  CC=5  out:4
    _match_touri  CC=3  out:3
    _match_uri2ops  CC=5  out:2
    _match_uri3  CC=4  out:0
    default_touri_registry  CC=5  out:6
    explain_uri  CC=14  out:17
    load_touri_config  CC=5  out:6
  packages.uri3.uri3.resolvers.log_query  [6 funcs]
    first  CC=2  out:1
    parse_query  CC=3  out:4
    query_bool  CC=3  out:2
    query_int  CC=3  out:3
    resolve_level  CC=3  out:3
    resolve_path  CC=8  out:5
  packages.uri3.uri3.resolvers.log_resolver  [4 funcs]
    read  CC=2  out:2
    resolve  CC=1  out:1
    parse_log_uri  CC=7  out:16
    resolve_log  CC=1  out:2
  packages.uri3.uri3.resolvers.protocol_resolver  [4 funcs]
    resolve_a2a  CC=2  out:1
    resolve_http_like  CC=1  out:0
    resolve_mcp  CC=2  out:1
    resolve_resource  CC=4  out:4
  packages.uri3.uri3.resolvers.registry  [1 funcs]
    build_resolver_registry  CC=1  out:5
  packages.uri3.uri3.resolvers.resolve_core  [2 funcs]
    call  CC=8  out:8
    resolve  CC=2  out:3
  packages.uri3.uri3.resolvers.router  [1 funcs]
    __init__  CC=1  out:1
  packages.uri3.uri3.resolvers.ssh_resolver  [7 funcs]
    _resolve_ssh_password  CC=1  out:1
    _ssh_options  CC=2  out:3
    build_ssh_command  CC=4  out:4
    parse_ssh_uri  CC=8  out:7
    resolve_ssh  CC=1  out:6
    run_ssh  CC=1  out:2
    ssh_transport_option  CC=4  out:7
  packages.uri3.uri3.results.service_result  [1 funcs]
    service_result  CC=3  out:10
  packages.uri3.uri3.scanner.docker_scanner  [5 funcs]
    _compose_ps  CC=6  out:8
    _inspect_container  CC=5  out:9
    scan_compose_stack  CC=5  out:4
    scan_container  CC=2  out:2
    scan_docker  CC=4  out:4
  packages.uri3.uri3.scanner.http_scanner  [5 funcs]
    _kind_for_path  CC=5  out:3
    _origin  CC=1  out:3
    _probe  CC=3  out:7
    _status_for  CC=5  out:0
    scan_http  CC=7  out:8
  packages.uri3.uri3.scanner.scanner  [2 funcs]
    scan  CC=5  out:5
    scan_log  CC=2  out:5
  packages.uri3.uri3.scanner.ssh_scanner  [6 funcs]
    _connectivity_item  CC=8  out:9
    _invalid_ssh_item  CC=1  out:2
    _remote_item_uri  CC=2  out:2
    _remote_listing_item  CC=4  out:5
    _remote_path_item  CC=5  out:5
    scan_ssh  CC=3  out:6
  packages.uri3.uri3.validators.uri_tree_validator  [2 funcs]
    load_yaml  CC=1  out:2
    validate_uri_tree  CC=2  out:7
  uri2ops.cli  [7 funcs]
    _print  CC=1  out:2
    operations_cmd  CC=6  out:11
    plan_cmd  CC=1  out:3
    registry_cmd  CC=4  out:9
    run_cmd  CC=2  out:4
    serve_cmd  CC=2  out:4
    validate_cmd  CC=2  out:3
  uri2ops.operation_registry.dispatcher  [3 funcs]
    _split_python_uri  CC=3  out:4
    call_handler  CC=2  out:4
    dispatch  CC=1  out:3
  uri2ops.operation_registry.loader  [3 funcs]
    default_registry_path  CC=1  out:2
    load_operation_registry  CC=10  out:13
    registry_schema_path  CC=1  out:2
  uri2ops.operation_registry.models  [2 funcs]
    list  CC=1  out:2
    from_mapping  CC=1  out:15
  uri2ops.operation_registry.validator  [2 funcs]
    validate_operation_registry  CC=14  out:13
    validate_registry_schema  CC=2  out:7
  uri2ops.remote_registry.loader  [8 funcs]
    _load_source  CC=14  out:19
    list_remote_sources  CC=4  out:9
    load_registry_config  CC=3  out:6
    merge_registry_documents  CC=6  out:6
    registry_config_path  CC=2  out:2
    registry_document  CC=4  out:4
    registry_from_document  CC=8  out:9
    resolve_operation_registry  CC=12  out:18
  uri2ops.server.app  [1 funcs]
    create_app  CC=1  out:62
  uri2ops.server.service  [5 funcs]
    list_registry_sources  CC=1  out:1
    plan_task  CC=1  out:2
    registry  CC=1  out:1
    registry_export  CC=1  out:2
    run_task  CC=1  out:3
  uri3.graph.uri_graph  [1 funcs]
    build_graph_from_tree  CC=10  out:28
  uri3.protocols.normalizer  [1 funcs]
    normalize_uri  CC=3  out:4
  uri3.protocols.parser  [1 funcs]
    parse_uri  CC=2  out:4
  uri3.resolvers.http_resolver  [1 funcs]
    resolve  CC=1  out:1
  uri3.resolvers.llm_resolver  [2 funcs]
    resolve  CC=2  out:4
    resolve_llm  CC=5  out:5
  uri3.resolvers.python_resolver  [5 funcs]
    call  CC=2  out:1
    resolve  CC=1  out:1
    _split_python_uri  CC=2  out:4
    call_python  CC=1  out:4
    resolve_python  CC=1  out:1
  uri3.validators.uri_validator  [1 funcs]
    validate_uri  CC=2  out:2

EDGES:
  uri2ops.cli._print → examples.21_touri_voice.run.print
  uri2ops.cli.operations_cmd → uri2ops.remote_registry.loader.resolve_operation_registry
  uri2ops.cli.operations_cmd → uri2ops.cli._print
  uri2ops.cli.operations_cmd → uri2ops.operation_registry.validator.validate_operation_registry
  uri2ops.cli.registry_cmd → uri2ops.cli._print
  uri2ops.cli.registry_cmd → uri2ops.remote_registry.loader.resolve_operation_registry
  uri2ops.cli.registry_cmd → uri2ops.operation_registry.validator.validate_operation_registry
  uri2ops.cli.registry_cmd → uri2ops.remote_registry.loader.list_remote_sources
  uri2ops.cli.validate_cmd → uri2ops.cli._print
  uri2ops.cli.plan_cmd → uri2ops.cli._print
  uri2ops.cli.plan_cmd → uri2ops.server.service.OperatorService.plan_task
  uri2ops.cli.run_cmd → uri2ops.server.service.OperatorService.run_task
  uri2ops.cli.run_cmd → uri2ops.cli._print
  uri2ops.cli.serve_cmd → uri2ops.server.app.create_app
  uri2ops.operation_registry.validator.validate_registry_schema → uri2ops.operation_registry.loader.registry_schema_path
  uri2ops.operation_registry.validator.validate_registry_schema → uri2ops.operation_registry.models.OperationRegistry.list
  uri2ops.operation_registry.loader.load_operation_registry → uri2ops.operation_registry.loader.default_registry_path
  uri2ops.operation_registry.loader.load_operation_registry → uri2ops.operation_registry.validator.validate_registry_schema
  uri2ops.operation_registry.models.OperationSpec.from_mapping → uri2ops.operation_registry.models.OperationRegistry.list
  uri2ops.operation_registry.dispatcher.call_handler → uri2ops.operation_registry.dispatcher._split_python_uri
  uri2ops.operation_registry.dispatcher.dispatch → uri2ops.remote_registry.loader.resolve_operation_registry
  uri2ops.operation_registry.dispatcher.dispatch → uri2ops.operation_registry.dispatcher.call_handler
  uri2ops.server.service.OperatorService.registry → uri2ops.remote_registry.loader.resolve_operation_registry
  uri2ops.server.service.OperatorService.registry_export → uri2ops.remote_registry.loader.registry_document
  uri2ops.server.service.OperatorService.list_registry_sources → uri2ops.remote_registry.loader.list_remote_sources
  uri2ops.remote_registry.loader.load_registry_config → uri2ops.remote_registry.loader.registry_config_path
  uri2ops.remote_registry.loader.load_registry_config → uri2ops.operation_registry.loader.default_registry_path
  uri2ops.remote_registry.loader.registry_from_document → uri2ops.operation_registry.validator.validate_registry_schema
  uri2ops.remote_registry.loader.resolve_operation_registry → uri2ops.remote_registry.loader.load_registry_config
  uri2ops.remote_registry.loader.resolve_operation_registry → uri2ops.remote_registry.loader.merge_registry_documents
  uri2ops.remote_registry.loader.resolve_operation_registry → uri2ops.remote_registry.loader.registry_from_document
  uri2ops.remote_registry.loader.resolve_operation_registry → uri2ops.operation_registry.loader.load_operation_registry
  uri2ops.remote_registry.loader.resolve_operation_registry → uri2ops.remote_registry.loader._load_source
  uri2ops.remote_registry.loader.resolve_operation_registry → uri2ops.operation_registry.loader.default_registry_path
  uri2ops.remote_registry.loader.list_remote_sources → uri2ops.remote_registry.loader.load_registry_config
  packages.uri3.uri3.logs.parsing.parse_log_line → packages.uri3.uri3.logs.parsing.empty_entry
  packages.uri3.uri3.logs.parsing.parse_log_line → packages.uri3.uri3.logs.parsing.parse_json_entry
  packages.uri3.uri3.logs.parsing.parse_log_line → packages.uri3.uri3.logs.parsing.parse_text_entry
  packages.uri3.uri3.logs.filters.matches_level → packages.uri3.uri3.logs.filters.level_rank
  packages.uri3.uri3.logs.filters.matches_time_window → packages.uri3.uri3.logs.filters.entry_timestamp
  packages.uri3.uri3.logs.filters.matches_filters → packages.uri3.uri3.logs.filters.matches_level
  packages.uri3.uri3.logs.filters.matches_filters → packages.uri3.uri3.logs.filters.matches_logger
  packages.uri3.uri3.logs.filters.matches_filters → packages.uri3.uri3.logs.filters.matches_grep
  packages.uri3.uri3.logs.filters.matches_filters → packages.uri3.uri3.logs.filters.matches_time_window
  packages.uri3.uri3.logs.reader.resolve_log_path → packages.uri3.uri3.config.repo_root.find_repo_root
  packages.uri3.uri3.logs.reader.read_logs → packages.uri3.uri3.resolvers.log_resolver.parse_log_uri
  packages.uri3.uri3.logs.reader.read_logs → packages.uri3.uri3.logs.reader.resolve_log_path
  packages.uri3.uri3.logs.reader.read_logs → packages.uri3.uri3.logs.reader._parse_since
  packages.uri3.uri3.logs.reader.read_logs → packages.uri3.uri3.logs.parsing.parse_log_line
  packages.uri3.uri3.logs.reader.read_logs → packages.uri3.uri3.logs.filters.matches_filters
```

## Test Contracts

*Scenarios as contract signatures — what the system guarantees.*

### Api (1)

**`Auto-generated API Smoke Tests`**
- assert `_status < 500`
- assert `_status >= 200`
- detectors: FastAPIDetector, ConfigEndpointDetector

### Cli (1)

**`CLI Command Tests`**

### Integration (1)

**`Auto-generated from Python Tests`**

## Refactoring Analysis

*Pre-refactoring snapshot — use this section to identify targets. Generated from `project/` toon files.*

### Call Graph & Complexity (`project/calls.toon.yaml`)

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/wronai/hypervisor
# generated in 0.21s
# nodes: 395 | edges: 500 | modules: 123
# CC̄=3.8

HUBS[20]:
  uri2ops.server.app.create_app
    CC=1  in:1  out:62  total:63
  packages.uri3.uri3.cli.commands.discovery.register
    CC=1  in:0  out:47  total:47
  packages.uri3.uri3.graph.graph_executor.run_workflow
    CC=22  in:5  out:40  total:45
  examples.21_touri_voice.run.print
    CC=0  in:43  out:0  total:43
  packages.uri3.uri3.results.service_result.service_result
    CC=3  in:33  out:10  total:43
  uri2ops.operation_registry.models.OperationRegistry.list
    CC=1  in:40  out:2  total:42
  packages.uri3.uri3.config.llm_profiles.resolve_llm_profile
    CC=10  in:4  out:32  total:36
  packages.nl2uri.nl2uri.flow_planner.plan_flow
    CC=12  in:4  out:29  total:33
  packages.touri.touri.data_quality.apply_data_quality
    CC=18  in:2  out:31  total:33
  meta_agent.planner.infer_intent
    CC=9  in:1  out:30  total:31
  uri3.graph.uri_graph.build_graph_from_tree
    CC=10  in:2  out:28  total:30
  packages.uri2flow.uri2flow.parser._parse_step
    CC=10  in:1  out:29  total:30
  packages.nl2uri.nl2uri.flow_repair.extract_flow_payload
    CC=20  in:1  out:28  total:29
  packages.uri3.uri3.resolvers.docker_resolver.parse_docker_uri
    CC=12  in:5  out:23  total:28
  packages.touri.touri.backends.python_backend.call_python_backend
    CC=9  in:3  out:25  total:28
  packages.nl2uri.nl2uri.flow_repair._ensure_step_ids
    CC=19  in:1  out:27  total:28
  packages.uri3.uri3.config.repo_root.find_repo_root
    CC=4  in:24  out:4  total:28
  packages.nl2uri.nl2uri.graph_repair.repair_graph_body
    CC=12  in:1  out:25  total:26
  packages.nl2uri.nl2uri.graph_repair.sanitize_node
    CC=16  in:1  out:25  total:26
  generator.model.load_agent_spec
    CC=7  in:2  out:24  total:26

MODULES:
  examples.21_touri_voice.run  [1 funcs]
    print  CC=0  out:0
  generator.hashutil  [1 funcs]
    file_sha256  CC=1  out:4
  generator.model  [1 funcs]
    load_agent_spec  CC=7  out:24
  generator.validate  [3 funcs]
    iter_agent_specs  CC=3  out:6
    main  CC=7  out:9
    validate_agent  CC=11  out:10
  generator.verify  [3 funcs]
    main  CC=9  out:10
    verify_generated  CC=6  out:5
    verify_generated_agent  CC=7  out:10
  hypervisor.contract_registry.registry_builder  [1 funcs]
    write_registry_manifest  CC=2  out:6
  hypervisor.uri2llm.pypi_resolver  [1 funcs]
    resolve_pypi  CC=5  out:6
  meta_agent.api  [4 funcs]
    generate  CC=2  out:6
    proposal_from_prompt  CC=2  out:6
    repair  CC=2  out:5
    validate  CC=2  out:5
  meta_agent.planner  [4 funcs]
    infer_intent  CC=9  out:30
    intent_to_agent_spec  CC=8  out:11
    package_name  CC=3  out:6
    singularize  CC=4  out:3
  meta_agent.repair.pipeline  [1 funcs]
    repair_agent_spec  CC=2  out:12
  nl2a.cli  [1 funcs]
    generate  CC=1  out:5
  nl2uri.writer  [1 funcs]
    write_uri_tree  CC=1  out:4
  packages.nl2uri.nl2uri.cli  [14 funcs]
    _default_use_llm  CC=1  out:2
    _emit  CC=2  out:3
    _plan_command  CC=6  out:7
    _resolve_use_llm  CC=5  out:2
    _validate_flow_payload  CC=2  out:5
    classify  CC=1  out:5
    flow  CC=6  out:17
    generate  CC=4  out:14
    graph  CC=5  out:15
    list_cmd  CC=1  out:5
  packages.nl2uri.nl2uri.domain_planner  [1 funcs]
    plan_from_prompt  CC=7  out:11
  packages.nl2uri.nl2uri.flow_planner  [1 funcs]
    plan_flow  CC=12  out:29
  packages.nl2uri.nl2uri.flow_planner_llm  [3 funcs]
    build_flow_planner_system_prompt  CC=1  out:6
    call_flow_planner_llm  CC=4  out:9
    plan_flow_with_llm  CC=3  out:6
  packages.nl2uri.nl2uri.flow_repair  [11 funcs]
    _ensure_step_ids  CC=19  out:27
    _needs_explicit_ids  CC=4  out:4
    _node_to_compact_step  CC=13  out:16
    _nodes_to_compact_steps  CC=4  out:3
    _normalize_step_raw  CC=10  out:14
    _supported_scheme  CC=2  out:2
    extract_flow_payload  CC=20  out:28
    repair_and_validate_flow  CC=2  out:4
    repair_flow_body  CC=8  out:17
    sanitize_flow_step  CC=18  out:24
  packages.nl2uri.nl2uri.graph_planner  [11 funcs]
    _detect_agent_id  CC=3  out:3
    _detect_health_uri  CC=4  out:6
    _slug  CC=2  out:3
    plan_auto  CC=1  out:2
    plan_by_kind  CC=2  out:3
    plan_list  CC=2  out:4
    plan_single  CC=4  out:6
    plan_task  CC=3  out:7
    plan_tree  CC=9  out:14
    plan_workflow_graph  CC=12  out:15
  packages.nl2uri.nl2uri.graph_planner_llm  [3 funcs]
    build_graph_planner_system_prompt  CC=2  out:5
    call_graph_planner_llm  CC=4  out:9
    plan_graph_with_llm  CC=4  out:7
  packages.nl2uri.nl2uri.graph_repair  [8 funcs]
    _coerce_operation  CC=5  out:6
    _sanitize_nodes  CC=12  out:8
    _slug  CC=2  out:3
    extract_graph_payload  CC=14  out:10
    normalize_to_kind  CC=12  out:14
    repair_and_validate_graph  CC=13  out:12
    repair_graph_body  CC=12  out:25
    sanitize_node  CC=16  out:25
  packages.nl2uri.nl2uri.llm_planner  [1 funcs]
    llm_plan  CC=2  out:4
  packages.nl2uri.nl2uri.output_classifier  [1 funcs]
    classify_output_kind  CC=23  out:16
  packages.nl2uri.nl2uri.pipeline  [4 funcs]
    _append_pipeline_logs  CC=2  out:4
    generate_tree  CC=1  out:1
    run_full_pipeline  CC=3  out:15
    run_generate_pipeline  CC=4  out:13
  packages.nl2uri.nl2uri.planner  [1 funcs]
    rule_based_plan  CC=1  out:2
  packages.nl2uri.nl2uri.planner_llm  [2 funcs]
    call_openrouter  CC=4  out:8
    extract_json  CC=3  out:8
  packages.nl2uri.nl2uri.planner_templates  [5 funcs]
    deterministic_weather_plan  CC=2  out:2
    generic_plan  CC=1  out:3
    is_weather_prompt  CC=1  out:2
    llm_uri_from_env  CC=6  out:7
    slug  CC=2  out:3
  packages.nl2uri.nl2uri.planner_validation  [3 funcs]
    is_structured_uri_tree  CC=10  out:13
    normalize_llm_tree  CC=7  out:12
    validate_tree_data  CC=2  out:6
  packages.resource-agent-factory.generator.agent_generator  [3 funcs]
    expand_paths  CC=4  out:7
    generate_agent  CC=5  out:17
    main  CC=5  out:4
  packages.resource-agent-factory.generator.header  [3 funcs]
    contract_source_ref  CC=3  out:7
    dockerfile_header  CC=1  out:0
    python_file_header  CC=1  out:0
  packages.resource-agent-factory.generator.paths  [1 funcs]
    project_root  CC=1  out:1
  packages.resource-agent-hypervisor.hypervisor.deployment_registry.lifecycle  [2 funcs]
    _repo_root  CC=2  out:3
    agent_status  CC=5  out:10
  packages.resource-agent-hypervisor.hypervisor.deployment_registry.run_plans  [1 funcs]
    build_run_plan  CC=5  out:7
  packages.resource-agent-hypervisor.hypervisor.deployment_registry.selector  [1 funcs]
    resolve_deployment  CC=7  out:9
  packages.resource-agent-hypervisor.hypervisor.deployment_registry.status  [1 funcs]
    sync_from_uri_tree  CC=2  out:4
  packages.resource-agent-hypervisor.hypervisor.domain_pack.generator  [1 funcs]
    generate_domain_pack  CC=1  out:3
  packages.resource-agent-hypervisor.meta_agent.orchestrator  [2 funcs]
    asdict_result  CC=1  out:0
    save_proposal_from_prompt  CC=2  out:6
  packages.touri.touri.backends.mock_backend  [1 funcs]
    call_mock_backend  CC=1  out:1
  packages.touri.touri.backends.python_backend  [2 funcs]
    _split_python_uri  CC=3  out:5
    call_python_backend  CC=9  out:25
  packages.touri.touri.backends.shell_backend  [1 funcs]
    call_shell_backend  CC=1  out:2
  packages.touri.touri.data_quality  [1 funcs]
    apply_data_quality  CC=18  out:31
  packages.touri.touri.loaders.registry_loader  [1 funcs]
    load_registry  CC=2  out:4
  packages.touri.touri.matcher  [3 funcs]
    match_uri  CC=3  out:4
    require_match  CC=2  out:2
    template_to_regex  CC=1  out:3
  packages.touri.touri_examples.validators  [3 funcs]
    always_pass  CC=1  out:1
    low_confidence_backend  CC=1  out:2
    reject_low_confidence  CC=4  out:6
  packages.uri2flow.uri2flow.cli  [5 funcs]
    build_parser  CC=1  out:14
    cmd_expand  CC=3  out:8
    cmd_print  CC=1  out:4
    cmd_validate  CC=2  out:4
    main  CC=1  out:3
  packages.uri2flow.uri2flow.expander  [4 funcs]
    _edges_from_depends  CC=4  out:2
    _node_from_step  CC=11  out:3
    dump_yaml  CC=1  out:1
    expand_flow  CC=6  out:8
  packages.uri2flow.uri2flow.parser  [4 funcs]
    _as_list  CC=5  out:5
    _parse_step  CC=10  out:29
    load_flow  CC=3  out:6
    parse_flow  CC=12  out:16
  packages.uri2flow.uri2flow.resolver  [9 funcs]
    _defaults_from_entry  CC=3  out:7
    _defaults_from_patterns  CC=7  out:7
    _defaults_from_scheme  CC=3  out:5
    _fallback_defaults  CC=4  out:5
    _find_repo_root  CC=7  out:7
    _load_flow_defaults_config  CC=4  out:6
    _match_pattern  CC=2  out:3
    _pattern_to_regex  CC=4  out:8
    default_operation_for_uri  CC=3  out:4
  packages.uri2flow.uri2flow.utils  [4 funcs]
    node_id_from_uri  CC=5  out:7
    path_parts  CC=4  out:4
    scheme_of  CC=1  out:1
    slugify  CC=2  out:4
  packages.uri2flow.uri2flow.validator  [3 funcs]
    validate_expanded_flow  CC=2  out:5
    validate_flow  CC=11  out:5
    validate_flow_document  CC=10  out:9
  packages.uri3.uri3.cli.commands.discovery  [1 funcs]
    register  CC=1  out:47
  packages.uri3.uri3.cli.commands.explain  [2 funcs]
    _render  CC=12  out:25
    register  CC=1  out:7
  packages.uri3.uri3.cli.commands.flow  [3 funcs]
    expand_flow_cmd  CC=3  out:9
    register  CC=1  out:11
    run_flow_cmd  CC=6  out:20
  packages.uri3.uri3.cli.commands.graph  [1 funcs]
    register  CC=1  out:5
  packages.uri3.uri3.cli.commands.resolve  [1 funcs]
    register  CC=1  out:24
  packages.uri3.uri3.cli.commands.workflow  [1 funcs]
    register  CC=1  out:20
  packages.uri3.uri3.cli.helpers  [1 funcs]
    list_payload  CC=2  out:3
  packages.uri3.uri3.config.cli_shortcuts  [5 funcs]
    cli_config_path  CC=1  out:1
    cli_examples  CC=3  out:3
    load_cli_config  CC=2  out:3
    resolve_scan_target  CC=4  out:4
    scan_shortcuts  CC=4  out:6
  packages.uri3.uri3.config.docker_stacks  [4 funcs]
    docker_config_path  CC=1  out:1
    load_docker_config  CC=2  out:3
    resolve_agent_stack  CC=4  out:15
    resolve_stack  CC=5  out:13
  packages.uri3.uri3.config.llm_profile_builder  [4 funcs]
    chosen_profile_name  CC=3  out:2
    normalize_model_name  CC=2  out:2
    parse_llm_query  CC=7  out:6
    resolve_profile_api_key  CC=4  out:4
  packages.uri3.uri3.config.llm_profiles  [3 funcs]
    llm_config_path  CC=1  out:1
    load_llm_config  CC=2  out:3
    resolve_llm_profile  CC=10  out:32
  packages.uri3.uri3.config.repo_root  [4 funcs]
    _walk_up  CC=7  out:6
    config_repo_root  CC=3  out:4
    find_repo_root  CC=4  out:4
    repo_root  CC=1  out:1
  packages.uri3.uri3.config.ssh_auth  [6 funcs]
    _password_from_env_file  CC=5  out:4
    _resolve_password_value  CC=8  out:10
    load_ssh_config  CC=2  out:3
    resolve_ssh_password  CC=12  out:13
    ssh_auth_hint  CC=3  out:2
    ssh_config_path  CC=1  out:1
  packages.uri3.uri3.config.uri_yaml  [3 funcs]
    is_uri  CC=4  out:3
    load_uri_yaml  CC=2  out:5
    resolve_uri_values  CC=15  out:13
  packages.uri3.uri3.docker.actions.compose  [8 funcs]
    _parse_ps_stdout  CC=4  out:5
    compose_base  CC=3  out:2
    control_compose  CC=6  out:6
    control_compose_down  CC=2  out:3
    control_compose_lifecycle  CC=1  out:2
    control_compose_logs  CC=1  out:3
    control_compose_ps  CC=3  out:4
    control_compose_up  CC=9  out:8
  packages.uri3.uri3.docker.actions.container  [3 funcs]
    _container_name  CC=2  out:0
    control_container  CC=8  out:9
    handles_container_action  CC=3  out:1
  packages.uri3.uri3.docker.compose_generator  [2 funcs]
    build_generate_plan  CC=2  out:9
    write_generated_compose  CC=1  out:6
  packages.uri3.uri3.docker.controller  [1 funcs]
    control_docker  CC=11  out:11
  packages.uri3.uri3.docker.runner  [1 funcs]
    run_command  CC=4  out:5
  packages.uri3.uri3.graph.adapters.browser_mock  [2 funcs]
    execute  CC=8  out:7
    json_dumps  CC=1  out:1
  packages.uri3.uri3.graph.adapters.browser_playwright  [3 funcs]
    execute  CC=11  out:23
    _session_state  CC=1  out:1
    close_playwright_session  CC=5  out:8
  packages.uri3.uri3.graph.adapters.browser_router  [4 funcs]
    execute  CC=2  out:4
    _playwright_ready  CC=3  out:5
    cleanup_browser_adapters  CC=2  out:2
    resolve_browser_mode  CC=5  out:3
  packages.uri3.uri3.graph.adapters.registry  [2 funcs]
    execute  CC=11  out:6
    _operator_adapter  CC=2  out:3
  packages.uri3.uri3.graph.adapters.uri2ops_adapter  [8 funcs]
    execute  CC=3  out:13
    _artifact_suffix  CC=9  out:0
    _attach_workflow_artifact  CC=3  out:6
    _registry_operation  CC=1  out:1
    _registry_scheme  CC=2  out:0
    _runtime_context  CC=1  out:3
    _use_legacy_browser_adapter  CC=1  out:2
    resolve_operator_adapter  CC=2  out:1
  packages.uri3.uri3.graph.artifacts  [3 funcs]
    artifact_path  CC=1  out:0
    artifact_uri  CC=1  out:0
    write_artifact  CC=2  out:6
  packages.uri3.uri3.graph.dependency_graph  [3 funcs]
    dependency_summary  CC=8  out:7
    detect_cycles  CC=15  out:7
    topological_sort  CC=13  out:13
  packages.uri3.uri3.graph.event_log  [2 funcs]
    append_workflow_event  CC=1  out:6
    workflow_event_path  CC=1  out:0
  packages.uri3.uri3.graph.execution_models  [1 funcs]
    utc_now_iso  CC=1  out:3
  packages.uri3.uri3.graph.graph_executor  [2 funcs]
    build_execution_plan  CC=3  out:10
    run_workflow  CC=22  out:40
  packages.uri3.uri3.graph.graph_serializer  [3 funcs]
    edges_from_depends_on  CC=4  out:5
    normalize_graph_payload  CC=12  out:24
    task_steps_to_graph  CC=3  out:7
  packages.uri3.uri3.graph.graph_validator  [4 funcs]
    _schema_path  CC=1  out:1
    load_workflow_graph  CC=10  out:11
    validate_workflow_graph  CC=9  out:13
    validate_workflow_schema  CC=2  out:7
  packages.uri3.uri3.graph.models  [1 funcs]
    from_dict  CC=5  out:15
  packages.uri3.uri3.graph.operation_registry  [6 funcs]
    allowed_operations  CC=1  out:2
    effective_kind  CC=2  out:2
    operation_registry_summary  CC=2  out:5
    requires_approval  CC=1  out:1
    scheme_from_uri  CC=2  out:1
    validate_node_operation  CC=2  out:5
  packages.uri3.uri3.graph.policy  [1 funcs]
    can_execute_step  CC=6  out:2
  packages.uri3.uri3.logs.filters  [7 funcs]
    entry_timestamp  CC=4  out:5
    level_rank  CC=3  out:2
    matches_filters  CC=4  out:4
    matches_grep  CC=4  out:5
    matches_level  CC=2  out:3
    matches_logger  CC=3  out:4
    matches_time_window  CC=7  out:1
  packages.uri3.uri3.logs.parsing  [4 funcs]
    empty_entry  CC=1  out:0
    parse_json_entry  CC=14  out:16
    parse_log_line  CC=4  out:5
    parse_text_entry  CC=5  out:8
  packages.uri3.uri3.logs.reader  [5 funcs]
    _parse_since  CC=7  out:14
    read_logs  CC=9  out:10
    read_logs_result  CC=3  out:2
    resolve_log_path  CC=4  out:3
    summarize_logs  CC=6  out:18
  packages.uri3.uri3.logs.writer  [1 funcs]
    append_log  CC=3  out:9
  packages.uri3.uri3.protocols.schemes.analyze  [3 funcs]
    _analyze_query  CC=14  out:10
    analyze_uri  CC=2  out:7
    describe_uri  CC=2  out:3
  packages.uri3.uri3.protocols.schemes.base  [2 funcs]
    to_dict  CC=4  out:2
    to_dict  CC=2  out:5
  packages.uri3.uri3.protocols.schemes.instance_parser  [13 funcs]
    _parse_a2a  CC=1  out:1
    _parse_docker  CC=1  out:1
    _parse_env  CC=1  out:1
    _parse_http  CC=1  out:1
    _parse_llm  CC=1  out:1
    _parse_log  CC=1  out:2
    _parse_mcp  CC=1  out:1
    _parse_pypi  CC=1  out:1
    _parse_python  CC=1  out:1
    _parse_resource  CC=1  out:1
  packages.uri3.uri3.protocols.schemes.spec_registry  [4 funcs]
    get_scheme_schema  CC=3  out:5
    is_concrete_uri  CC=4  out:3
    list_schemes  CC=5  out:5
    query_names  CC=2  out:3
  packages.uri3.uri3.resolvers.dispatch  [2 funcs]
    _resolve_docker  CC=1  out:1
    resolve_target  CC=3  out:4
  packages.uri3.uri3.resolvers.docker_resolver  [6 funcs]
    _bool  CC=3  out:2
    _first  CC=2  out:1
    _int  CC=3  out:2
    parse_docker_uri  CC=12  out:23
    resolve_docker  CC=2  out:4
    resolve_docker_target  CC=1  out:1
  packages.uri3.uri3.resolvers.env_resolver  [6 funcs]
    call  CC=1  out:1
    resolve  CC=1  out:1
    _env_var_name  CC=3  out:3
    _first  CC=2  out:1
    call_env  CC=8  out:17
    resolve_env  CC=1  out:2
  packages.uri3.uri3.resolvers.explain  [7 funcs]
    _find_repo_root  CC=5  out:4
    _match_touri  CC=3  out:3
    _match_uri2ops  CC=5  out:2
    _match_uri3  CC=4  out:0
    default_touri_registry  CC=5  out:6
    explain_uri  CC=14  out:17
    load_touri_config  CC=5  out:6
  packages.uri3.uri3.resolvers.log_query  [6 funcs]
    first  CC=2  out:1
    parse_query  CC=3  out:4
    query_bool  CC=3  out:2
    query_int  CC=3  out:3
    resolve_level  CC=3  out:3
    resolve_path  CC=8  out:5
  packages.uri3.uri3.resolvers.log_resolver  [4 funcs]
    read  CC=2  out:2
    resolve  CC=1  out:1
    parse_log_uri  CC=7  out:16
    resolve_log  CC=1  out:2
  packages.uri3.uri3.resolvers.protocol_resolver  [4 funcs]
    resolve_a2a  CC=2  out:1
    resolve_http_like  CC=1  out:0
    resolve_mcp  CC=2  out:1
    resolve_resource  CC=4  out:4
  packages.uri3.uri3.resolvers.registry  [1 funcs]
    build_resolver_registry  CC=1  out:5
  packages.uri3.uri3.resolvers.resolve_core  [2 funcs]
    call  CC=8  out:8
    resolve  CC=2  out:3
  packages.uri3.uri3.resolvers.router  [1 funcs]
    __init__  CC=1  out:1
  packages.uri3.uri3.resolvers.ssh_resolver  [7 funcs]
    _resolve_ssh_password  CC=1  out:1
    _ssh_options  CC=2  out:3
    build_ssh_command  CC=4  out:4
    parse_ssh_uri  CC=8  out:7
    resolve_ssh  CC=1  out:6
    run_ssh  CC=1  out:2
    ssh_transport_option  CC=4  out:7
  packages.uri3.uri3.results.service_result  [1 funcs]
    service_result  CC=3  out:10
  packages.uri3.uri3.scanner.docker_scanner  [5 funcs]
    _compose_ps  CC=6  out:8
    _inspect_container  CC=5  out:9
    scan_compose_stack  CC=5  out:4
    scan_container  CC=2  out:2
    scan_docker  CC=4  out:4
  packages.uri3.uri3.scanner.http_scanner  [5 funcs]
    _kind_for_path  CC=5  out:3
    _origin  CC=1  out:3
    _probe  CC=3  out:7
    _status_for  CC=5  out:0
    scan_http  CC=7  out:8
  packages.uri3.uri3.scanner.scanner  [2 funcs]
    scan  CC=5  out:5
    scan_log  CC=2  out:5
  packages.uri3.uri3.scanner.ssh_scanner  [6 funcs]
    _connectivity_item  CC=8  out:9
    _invalid_ssh_item  CC=1  out:2
    _remote_item_uri  CC=2  out:2
    _remote_listing_item  CC=4  out:5
    _remote_path_item  CC=5  out:5
    scan_ssh  CC=3  out:6
  packages.uri3.uri3.validators.uri_tree_validator  [2 funcs]
    load_yaml  CC=1  out:2
    validate_uri_tree  CC=2  out:7
  uri2ops.cli  [7 funcs]
    _print  CC=1  out:2
    operations_cmd  CC=6  out:11
    plan_cmd  CC=1  out:3
    registry_cmd  CC=4  out:9
    run_cmd  CC=2  out:4
    serve_cmd  CC=2  out:4
    validate_cmd  CC=2  out:3
  uri2ops.operation_registry.dispatcher  [3 funcs]
    _split_python_uri  CC=3  out:4
    call_handler  CC=2  out:4
    dispatch  CC=1  out:3
  uri2ops.operation_registry.loader  [3 funcs]
    default_registry_path  CC=1  out:2
    load_operation_registry  CC=10  out:13
    registry_schema_path  CC=1  out:2
  uri2ops.operation_registry.models  [2 funcs]
    list  CC=1  out:2
    from_mapping  CC=1  out:15
  uri2ops.operation_registry.validator  [2 funcs]
    validate_operation_registry  CC=14  out:13
    validate_registry_schema  CC=2  out:7
  uri2ops.remote_registry.loader  [8 funcs]
    _load_source  CC=14  out:19
    list_remote_sources  CC=4  out:9
    load_registry_config  CC=3  out:6
    merge_registry_documents  CC=6  out:6
    registry_config_path  CC=2  out:2
    registry_document  CC=4  out:4
    registry_from_document  CC=8  out:9
    resolve_operation_registry  CC=12  out:18
  uri2ops.server.app  [1 funcs]
    create_app  CC=1  out:62
  uri2ops.server.service  [5 funcs]
    list_registry_sources  CC=1  out:1
    plan_task  CC=1  out:2
    registry  CC=1  out:1
    registry_export  CC=1  out:2
    run_task  CC=1  out:3
  uri3.graph.uri_graph  [1 funcs]
    build_graph_from_tree  CC=10  out:28
  uri3.protocols.normalizer  [1 funcs]
    normalize_uri  CC=3  out:4
  uri3.protocols.parser  [1 funcs]
    parse_uri  CC=2  out:4
  uri3.resolvers.http_resolver  [1 funcs]
    resolve  CC=1  out:1
  uri3.resolvers.llm_resolver  [2 funcs]
    resolve  CC=2  out:4
    resolve_llm  CC=5  out:5
  uri3.resolvers.python_resolver  [5 funcs]
    call  CC=2  out:1
    resolve  CC=1  out:1
    _split_python_uri  CC=2  out:4
    call_python  CC=1  out:4
    resolve_python  CC=1  out:1
  uri3.validators.uri_validator  [1 funcs]
    validate_uri  CC=2  out:2

EDGES:
  uri2ops.cli._print → examples.21_touri_voice.run.print
  uri2ops.cli.operations_cmd → uri2ops.remote_registry.loader.resolve_operation_registry
  uri2ops.cli.operations_cmd → uri2ops.cli._print
  uri2ops.cli.operations_cmd → uri2ops.operation_registry.validator.validate_operation_registry
  uri2ops.cli.registry_cmd → uri2ops.cli._print
  uri2ops.cli.registry_cmd → uri2ops.remote_registry.loader.resolve_operation_registry
  uri2ops.cli.registry_cmd → uri2ops.operation_registry.validator.validate_operation_registry
  uri2ops.cli.registry_cmd → uri2ops.remote_registry.loader.list_remote_sources
  uri2ops.cli.validate_cmd → uri2ops.cli._print
  uri2ops.cli.plan_cmd → uri2ops.cli._print
  uri2ops.cli.plan_cmd → uri2ops.server.service.OperatorService.plan_task
  uri2ops.cli.run_cmd → uri2ops.server.service.OperatorService.run_task
  uri2ops.cli.run_cmd → uri2ops.cli._print
  uri2ops.cli.serve_cmd → uri2ops.server.app.create_app
  uri2ops.operation_registry.validator.validate_registry_schema → uri2ops.operation_registry.loader.registry_schema_path
  uri2ops.operation_registry.validator.validate_registry_schema → uri2ops.operation_registry.models.OperationRegistry.list
  uri2ops.operation_registry.loader.load_operation_registry → uri2ops.operation_registry.loader.default_registry_path
  uri2ops.operation_registry.loader.load_operation_registry → uri2ops.operation_registry.validator.validate_registry_schema
  uri2ops.operation_registry.models.OperationSpec.from_mapping → uri2ops.operation_registry.models.OperationRegistry.list
  uri2ops.operation_registry.dispatcher.call_handler → uri2ops.operation_registry.dispatcher._split_python_uri
  uri2ops.operation_registry.dispatcher.dispatch → uri2ops.remote_registry.loader.resolve_operation_registry
  uri2ops.operation_registry.dispatcher.dispatch → uri2ops.operation_registry.dispatcher.call_handler
  uri2ops.server.service.OperatorService.registry → uri2ops.remote_registry.loader.resolve_operation_registry
  uri2ops.server.service.OperatorService.registry_export → uri2ops.remote_registry.loader.registry_document
  uri2ops.server.service.OperatorService.list_registry_sources → uri2ops.remote_registry.loader.list_remote_sources
  uri2ops.remote_registry.loader.load_registry_config → uri2ops.remote_registry.loader.registry_config_path
  uri2ops.remote_registry.loader.load_registry_config → uri2ops.operation_registry.loader.default_registry_path
  uri2ops.remote_registry.loader.registry_from_document → uri2ops.operation_registry.validator.validate_registry_schema
  uri2ops.remote_registry.loader.resolve_operation_registry → uri2ops.remote_registry.loader.load_registry_config
  uri2ops.remote_registry.loader.resolve_operation_registry → uri2ops.remote_registry.loader.merge_registry_documents
  uri2ops.remote_registry.loader.resolve_operation_registry → uri2ops.remote_registry.loader.registry_from_document
  uri2ops.remote_registry.loader.resolve_operation_registry → uri2ops.operation_registry.loader.load_operation_registry
  uri2ops.remote_registry.loader.resolve_operation_registry → uri2ops.remote_registry.loader._load_source
  uri2ops.remote_registry.loader.resolve_operation_registry → uri2ops.operation_registry.loader.default_registry_path
  uri2ops.remote_registry.loader.list_remote_sources → uri2ops.remote_registry.loader.load_registry_config
  packages.uri3.uri3.logs.parsing.parse_log_line → packages.uri3.uri3.logs.parsing.empty_entry
  packages.uri3.uri3.logs.parsing.parse_log_line → packages.uri3.uri3.logs.parsing.parse_json_entry
  packages.uri3.uri3.logs.parsing.parse_log_line → packages.uri3.uri3.logs.parsing.parse_text_entry
  packages.uri3.uri3.logs.filters.matches_level → packages.uri3.uri3.logs.filters.level_rank
  packages.uri3.uri3.logs.filters.matches_time_window → packages.uri3.uri3.logs.filters.entry_timestamp
  packages.uri3.uri3.logs.filters.matches_filters → packages.uri3.uri3.logs.filters.matches_level
  packages.uri3.uri3.logs.filters.matches_filters → packages.uri3.uri3.logs.filters.matches_logger
  packages.uri3.uri3.logs.filters.matches_filters → packages.uri3.uri3.logs.filters.matches_grep
  packages.uri3.uri3.logs.filters.matches_filters → packages.uri3.uri3.logs.filters.matches_time_window
  packages.uri3.uri3.logs.reader.resolve_log_path → packages.uri3.uri3.config.repo_root.find_repo_root
  packages.uri3.uri3.logs.reader.read_logs → packages.uri3.uri3.resolvers.log_resolver.parse_log_uri
  packages.uri3.uri3.logs.reader.read_logs → packages.uri3.uri3.logs.reader.resolve_log_path
  packages.uri3.uri3.logs.reader.read_logs → packages.uri3.uri3.logs.reader._parse_since
  packages.uri3.uri3.logs.reader.read_logs → packages.uri3.uri3.logs.parsing.parse_log_line
  packages.uri3.uri3.logs.reader.read_logs → packages.uri3.uri3.logs.filters.matches_filters
```

### Code Analysis (`project/analysis.toon.yaml`)

```toon markpact:analysis path=project/analysis.toon.yaml
# code2llm | 405f 17704L | python:281,yaml:63,shell:17,json:15,toml:10,txt:4,yml:3,proto:2,mk:2,j2:1 | 2026-06-14
# generated in 0.06s
# CC̅=3.8 | critical:14/760 | dups:0 | cycles:0

HEALTH[14]:
  🟡 CC    detect_cycles CC=15 (limit:15)
  🟡 CC    resolve_uri_values CC=15 (limit:15)
  🟡 CC    apply_data_quality CC=18 (limit:15)
  🟡 CC    sanitize_node CC=16 (limit:15)
  🟡 CC    classify_output_kind CC=23 (limit:15)
  🟡 CC    extract_flow_payload CC=20 (limit:15)
  🟡 CC    sanitize_flow_step CC=18 (limit:15)
  🟡 CC    _ensure_step_ids CC=19 (limit:15)
  🟡 CC    load_manifest_from_dict CC=16 (limit:15)
  🟡 CC    _call_backend CC=18 (limit:15)
  🟡 CC    call_uri2ops_backend CC=17 (limit:15)
  🟡 CC    run_workflow CC=22 (limit:15)
  🟡 CC    workflow_aggregate_statuses CC=15 (limit:15)
  🟡 CC    validate_manifest CC=15 (limit:15)

REFACTOR[1]:
  1. split 14 high-CC methods  (CC>15)

PIPELINES[207]:
  [1] Src [operations_cmd]: operations_cmd → resolve_operation_registry → load_registry_config → registry_config_path
      PURITY: 100% pure
  [2] Src [registry_cmd]: registry_cmd → _print → print
      PURITY: 100% pure
  [3] Src [validate_cmd]: validate_cmd → _print → print
      PURITY: 100% pure
  [4] Src [plan_cmd]: plan_cmd → _print → print
      PURITY: 100% pure
  [5] Src [run_cmd]: run_cmd → run_task
      PURITY: 100% pure
  [6] Src [serve_cmd]: serve_cmd → create_app → build_agent_card
      PURITY: 100% pure
  [7] Src [main]: main
      PURITY: 100% pure
  [8] Src [from_mapping]: from_mapping → list
      PURITY: 100% pure
  [9] Src [get]: get
      PURITY: 100% pure
  [10] Src [require]: require
      PURITY: 100% pure
  [11] Src [__init__]: __init__
      PURITY: 100% pure
  [12] Src [registry]: registry → resolve_operation_registry → load_registry_config → registry_config_path
      PURITY: 100% pure
  [13] Src [registry_export]: registry_export → registry_document
      PURITY: 100% pure
  [14] Src [list_operations]: list_operations
      PURITY: 100% pure
  [15] Src [describe_operation]: describe_operation
      PURITY: 100% pure
  [16] Src [list_registry_sources]: list_registry_sources → list_remote_sources → load_registry_config → registry_config_path
      PURITY: 100% pure
  [17] Src [validate_task]: validate_task
      PURITY: 100% pure
  [18] Src [adjacency]: adjacency
      PURITY: 100% pure
  [19] Src [reverse_adjacency]: reverse_adjacency
      PURITY: 100% pure
  [20] Src [dependency_summary]: dependency_summary → detect_cycles
      PURITY: 100% pure
  [21] Src [add_node]: add_node
      PURITY: 100% pure
  [22] Src [add_edge]: add_edge
      PURITY: 100% pure
  [23] Src [from_dict]: from_dict → list
      PURITY: 100% pure
  [24] Src [to_dict]: to_dict
      PURITY: 100% pure
  [25] Src [execute]: execute → _registry_scheme
      PURITY: 100% pure
  [26] Src [resolve_operator_adapter]: resolve_operator_adapter → _use_legacy_browser_adapter
      PURITY: 100% pure
  [27] Src [execute]: execute → write_artifact → artifact_path
      PURITY: 100% pure
  [28] Src [execute]: execute
      PURITY: 100% pure
  [29] Src [execute]: execute → resolve_deployment → load_deployment_registry → _read_yaml
      PURITY: 100% pure
  [30] Src [execute]: execute
      PURITY: 100% pure
  [31] Src [_operator_adapter]: _operator_adapter → _use_legacy_browser_adapter
      PURITY: 100% pure
  [32] Src [execute]: execute → _session_state
      PURITY: 100% pure
  [33] Src [__init__]: __init__
      PURITY: 100% pure
  [34] Src [execute]: execute → resolve_browser_mode → _playwright_ready
      PURITY: 100% pure
  [35] Src [cleanup_browser_adapters]: cleanup_browser_adapters → close_playwright_session
      PURITY: 100% pure
  [36] Src [register]: register → explain_uri → scheme_from_uri
      PURITY: 100% pure
  [37] Src [register]: register → build_graph_from_tree
      PURITY: 100% pure
  [38] Src [register]: register → validate_uri → parse_uri
      PURITY: 100% pure
  [39] Src [register]: register → validate_workflow_graph → load_workflow_graph → normalize_graph_payload → ...(1 more)
      PURITY: 100% pure
  [40] Src [register]: register → expand_flow_cmd → expand_flow → load_flow → ...(3 more)
      PURITY: 100% pure
  [41] Src [register]: register → list_payload → cli_examples → load_cli_config → ...(4 more)
      PURITY: 100% pure
  [42] Src [scan]: scan → parse_uri
      PURITY: 100% pure
  [43] Src [to_dict]: to_dict
      PURITY: 100% pure
  [44] Src [normalize_uri]: normalize_uri → parse_uri
      PURITY: 100% pure
  [45] Src [spec]: spec → list
      PURITY: 100% pure
  [46] Src [spec]: spec
      PURITY: 100% pure
  [47] Src [to_dict]: to_dict → list
      PURITY: 100% pure
  [48] Src [to_dict]: to_dict → list
      PURITY: 100% pure
  [49] Src [spec]: spec
      PURITY: 100% pure
  [50] Src [spec]: spec
      PURITY: 100% pure

LAYERS:
  generator/                      CC̄=6.0    ←in:14  →out:8  !! split
  │ validate                     0L  0C    3m  CC=11     ←5
  │ hashutil                     0L  0C    1m  CC=1      ←2
  │ verify                       0L  0C    3m  CC=9      ←4
  │ model                        0L  2C    2m  CC=7      ←2
  │ __init__                     0L  0C    0m  CC=0.0    ←0
  │ Dockerfile.j2                0L  0C    0m  CC=0.0    ←0
  │
  packages/                       CC̄=4.0    ←in:0  →out:0
  │ graph_planner              322L  0C   11m  CC=12     ←4
  │ !! graph_executor             290L  0C    6m  CC=22     ←5
  │ cli                        246L  0C   15m  CC=6      ←0
  │ !! flow_repair                229L  0C   13m  CC=20     ←2
  │ !! graph_repair               195L  0C    8m  CC=16     ←2
  │ !! envelope                   175L  0C    8m  CC=15     ←2
  │ lifecycle                  172L  0C    7m  CC=8      ←8
  │ explain                    169L  0C    8m  CC=14     ←2
  │ cli                        166L  0C   16m  CC=5      ←0
  │ replay                     156L  0C    6m  CC=11     ←2
  │ docker_resolver            154L  1C    7m  CC=12     ←5
  │ !! executor                   153L  0C    6m  CC=18     ←1
  │ status                     151L  0C   10m  CC=11     ←5
  │ graph_planner_llm          147L  0C    3m  CC=4      ←1
  │ pipeline                   141L  2C    4m  CC=4      ←1
  │ execution_models           135L  4C    6m  CC=5      ←2
  │ cli_commands               128L  0C    6m  CC=7      ←1
  │ uri2ops_adapter            122L  1C    9m  CC=9      ←2
  │ instance_parser            119L  0C   13m  CC=4      ←2
  │ registry                   113L  3C    5m  CC=11     ←1
  │ flow_planner_llm           112L  0C    3m  CC=4      ←1
  │ ssh_resolver               110L  0C    7m  CC=8      ←6
  │ resolver                   107L  1C   10m  CC=7      ←1
  │ agent_generator            106L  0C    4m  CC=5      ←2
  │ flow_planner               106L  0C    5m  CC=12     ←4
  │ reader                     104L  0C    5m  CC=9      ←5
  │ !! uri2ops_backend            104L  0C    4m  CC=17     ←1
  │ planner_templates          102L  0C    5m  CC=6      ←2
  │ service_result             102L  1C    4m  CC=12     ←8
  │ flow                       100L  0C    3m  CC=6      ←0
  │ compose                     99L  0C    8m  CC=9      ←1
  │ spec_registry               99L  0C    5m  CC=5      ←3
  │ ssh_auth                    96L  0C    7m  CC=12     ←2
  │ loader                      96L  0C    5m  CC=6      ←2
  │ ssh_deploy                  95L  0C    2m  CC=7      ←1
  │ uri_graph_backend           95L  0C    4m  CC=9      ←1
  │ env_resolver                94L  1C    7m  CC=8      ←5
  │ cli                         92L  0C    7m  CC=4      ←0
  │ docker_scanner              91L  0C    5m  CC=6      ←2
  │ ssh_scanner                 90L  0C    6m  CC=8      ←2
  │ parser                      90L  1C    4m  CC=12     ←3
  │ !! uri_yaml                    89L  0C    3m  CC=15     ←7
  │ models                      88L  3C    5m  CC=8      ←0
  │ uri_flow_backend            87L  0C    3m  CC=9      ←1
  │ log_resolver                85L  2C    5m  CC=7      ←3
  │ models                      84L  3C    1m  CC=1      ←0
  │ core                        84L  1C    7m  CC=3      ←0
  │ llm_profiles                83L  1C    4m  CC=10     ←4
  │ !! data_quality                83L  0C    1m  CC=18     ←1
  │ !! dependency_graph            82L  0C    5m  CC=15     ←2
  │ expander                    81L  0C    4m  CC=11     ←5
  │ discovery                   79L  0C    1m  CC=1      ←0
  │ pack_writer                 79L  0C    1m  CC=3      ←1
  │ !! output_classifier           78L  0C    1m  CC=23     ←2
  │ browser_playwright          77L  1C    3m  CC=11     ←1
  │ http_scanner                76L  0C    6m  CC=7      ←3
  │ log                         76L  0C    1m  CC=3      ←0
  │ docker_runner               76L  0C    6m  CC=9      ←3
  │ generator                   75L  0C    2m  CC=2      ←1
  │ local_targets               75L  0C    3m  CC=6      ←1
  │ parsing                     73L  0C    4m  CC=14     ←1
  │ filters                     73L  0C    7m  CC=7      ←1
  │ graph_validator             73L  0C    4m  CC=10     ←8
  │ analyze                     73L  0C    3m  CC=14     ←2
  │ orchestrator                73L  0C    4m  CC=7      ←2
  │ operation_registry          71L  0C    6m  CC=2      ←8
  │ register                    71L  0C    2m  CC=6      ←1
  │ cli_commands                69L  0C    6m  CC=3      ←1
  │ markpact_loader             68L  0C    5m  CC=8      ←1
  │ base                        67L  2C    2m  CC=4      ←0
  │ dispatch                    67L  0C    3m  CC=3      ←1
  │ browser_router              66L  1C    5m  CC=5      ←0
  │ cli                         66L  0C    5m  CC=3      ←1
  │ helpers                     66L  0C    2m  CC=5      ←2
  │ planner_validation          65L  0C    3m  CC=10     ←1
  │ cli_commands                65L  0C    5m  CC=5      ←0
  │ runtime_state               65L  0C    8m  CC=6      ←1
  │ validator                   64L  0C    3m  CC=11     ←2
  │ graph_serializer            63L  0C    4m  CC=12     ←3
  │ defaults                    63L  0C    4m  CC=4      ←1
  │ !! manifest                    63L  0C    3m  CC=16     ←3
  │ agent_card                  63L  0C    0m  CC=0.0    ←0
  │ merge_helpers               61L  0C    3m  CC=6      ←1
  │ planner_llm                 59L  0C    2m  CC=4      ←3
  │ __init__                    59L  0C    0m  CC=0.0    ←0
  │ ssh_run                     58L  0C    1m  CC=7      ←1
  │ docker_stacks               57L  0C    4m  CC=5      ←2
  │ __init__                    57L  0C    0m  CC=0.0    ←0
  │ log_query                   55L  0C    6m  CC=8      ←1
  │ header                      51L  0C    5m  CC=3      ←1
  │ cli                         51L  0C    1m  CC=7      ←0
  │ config_checks               50L  0C    4m  CC=7      ←1
  │ models                      50L  2C    3m  CC=5      ←0
  │ env                         50L  0C    3m  CC=9      ←3
  │ nlp2uri.yaml                50L  0C    0m  CC=0.0    ←0
  │ agent_contract              48L  0C    1m  CC=2      ←1
  │ models                      47L  2C    1m  CC=11     ←0
  │ compose_generator           46L  0C    2m  CC=2      ←2
  │ replay                      46L  0C    2m  CC=9      ←0
  │ workflow                    45L  0C    1m  CC=1      ←0
  │ resolve_core                45L  1C    2m  CC=8      ←0
  │ browser_mock                44L  1C    2m  CC=8      ←1
  │ llm_profile_builder         44L  0C    4m  CC=7      ←1
  │ repo_root                   44L  0C    4m  CC=7      ←22
  │ loader                      44L  0C    4m  CC=5      ←3
  │ docker                      43L  0C    1m  CC=1      ←0
  │ explain                     42L  0C    2m  CC=12     ←0
  │ scanner                     42L  0C    2m  CC=5      ←0
  │ uri_capability.schema.json    42L  0C    0m  CC=0.0    ←0
  │ cli_shortcuts               41L  0C    5m  CC=4      ←2
  │ python_backend              41L  0C    2m  CC=9      ←2
  │ cli                         41L  0C    2m  CC=5      ←0
  │ uri_config                  40L  0C    2m  CC=10     ←1
  │ capabilities                40L  0C    3m  CC=7      ←1
  │ uri_flow.schema.json        40L  0C    0m  CC=0.0    ←0
  │ utils                       38L  0C    4m  CC=5      ←3
  │ client                      38L  1C    8m  CC=2      ←0
  │ ssh_verify                  38L  0C    1m  CC=12     ←1
  │ container                   37L  0C    3m  CC=8      ←1
  │ agent_card                  37L  0C    0m  CC=0.0    ←0
  │ controller                  36L  0C    1m  CC=11     ←2
  │ resolve                     36L  0C    1m  CC=1      ←0
  │ cross_validator             36L  0C    2m  CC=5      ←1
  │ pyproject.toml              36L  0C    0m  CC=0.0    ←0
  │ errors                      35L  1C    2m  CC=10     ←4
  │ matcher                     35L  1C    3m  CC=3      ←2
  │ writer                      34L  0C    1m  CC=3      ←2
  │ artifacts                   33L  0C    3m  CC=2      ←3
  │ domain_planner              33L  0C    1m  CC=7      ←5
  │ validators                  33L  0C    2m  CC=5      ←1
  │ cli                         33L  0C    1m  CC=10     ←0
  │ run_plans                   33L  0C    1m  CC=5      ←3
  │ pyproject.toml              33L  0C    0m  CC=0.0    ←0
  │ capabilities                32L  0C    1m  CC=13     ←1
  │ env_merge                   31L  0C    2m  CC=6      ←1
  │ main                        31L  0C    2m  CC=2      ←0
  │ pyproject.toml              31L  0C    0m  CC=0.0    ←0
  │ __init__                    31L  0C    0m  CC=0.0    ←0
  │ process                     30L  0C    1m  CC=4      ←1
  │ pyproject.toml              30L  0C    0m  CC=0.0    ←0
  │ !! validator                   29L  0C    1m  CC=15     ←2
  │ router                      28L  1C    3m  CC=2      ←0
  │ env_config                  28L  0C    3m  CC=2      ←1
  │ protocol_resolver           27L  0C    4m  CC=4      ←3
  │ registry                    27L  0C    0m  CC=0.0    ←0
  │ constants                   27L  0C    0m  CC=0.0    ←0
  │ merger                      26L  0C    1m  CC=2      ←1
  │ resources                   26L  0C    2m  CC=7      ←1
  │ validators                  25L  0C    3m  CC=4      ←0
  │ model                       25L  1C    1m  CC=1      ←0
  │ selector                    25L  0C    1m  CC=7      ←3
  │ redaction                   25L  0C    2m  CC=7      ←1
  │ pyproject.toml              25L  0C    0m  CC=0.0    ←0
  │ conditions                  24L  0C    1m  CC=7      ←1
  │ resources                   24L  0C    1m  CC=2      ←1
  │ loader                      24L  0C    2m  CC=1      ←0
  │ scheme_registry             24L  0C    0m  CC=0.0    ←0
  │ runner                      24L  0C    0m  CC=0.0    ←0
  │ runner                      23L  0C    1m  CC=4      ←2
  │ graph                       23L  0C    1m  CC=1      ←0
  │ pyproject.toml              23L  0C    0m  CC=0.0    ←0
  │ env                         22L  0C    1m  CC=1      ←0
  │ resources                   22L  0C    1m  CC=6      ←1
  │ statuses                    21L  0C    1m  CC=5      ←2
  │ registry                    21L  0C    1m  CC=1      ←1
  │ policy                      20L  0C    1m  CC=6      ←1
  │ event_log                   20L  0C    2m  CC=1      ←2
  │ uri_tree_validator          20L  0C    2m  CC=2      ←3
  │ python                      18L  0C    1m  CC=1      ←0
  │ commands                    18L  0C    1m  CC=2      ←1
  │ file_loader                 18L  0C    2m  CC=2      ←1
  │ __init__                    18L  0C    0m  CC=0.0    ←0
  │ parser                      17L  0C    2m  CC=1      ←1
  │ views.yaml                  17L  0C    0m  CC=0.0    ←0
  │ pyproject.toml              17L  0C    0m  CC=0.0    ←0
  │ llm                         16L  0C    1m  CC=1      ←0
  │ resource_like               16L  0C    1m  CC=1      ←0
  │ views                       16L  0C    1m  CC=2      ←1
  │ proto_index                 16L  0C    2m  CC=2      ←3
  │ main                        16L  0C    0m  CC=0.0    ←0
  │ main                        16L  0C    0m  CC=0.0    ←0
  │ __init__                    16L  0C    0m  CC=0.0    ←0
  │ mcp                         15L  0C    1m  CC=1      ←0
  │ http                        15L  0C    1m  CC=1      ←0
  │ pypi                        15L  0C    1m  CC=1      ←0
  │ a2a                         15L  0C    1m  CC=1      ←0
  │ shell_backend               15L  0C    1m  CC=1      ←1
  │ resources.yaml              15L  0C    0m  CC=0.0    ←0
  │ remote_runner               15L  0C    0m  CC=0.0    ←0
  │ __init__                    15L  0C    0m  CC=0.0    ←0
  │ weather                     14L  0C    1m  CC=1      ←0
  │ renderers                   14L  0C    1m  CC=3      ←1
  │ ssh_helpers                 14L  0C    2m  CC=2      ←2
  │ registry_loader             14L  0C    1m  CC=2      ←3
  │ planner                     13L  1C    1m  CC=1      ←1
  │ validate                    13L  0C    1m  CC=1      ←2
  │ base                        12L  1C    1m  CC=1      ←0
  │ paths                       12L  0C    1m  CC=1      ←1
  │ __init__                    12L  0C    0m  CC=0.0    ←0
  │ __init__                    12L  0C    0m  CC=0.0    ←0
  │ writer                      11L  0C    1m  CC=1      ←2
  │ handlers                    10L  0C    1m  CC=3      ←1
  │ mock_backend                 9L  0C    1m  CC=1      ←1
  │ Dockerfile                   9L  0C    0m  CC=0.0    ←0
  │ Dockerfile                   9L  0C    0m  CC=0.0    ←0
  │ __init__                     9L  0C    0m  CC=0.0    ←0
  │ llm_planner                  8L  0C    1m  CC=2      ←0
  │ proto                        8L  0C    1m  CC=2      ←1
  │ paths                        5L  0C    0m  CC=0.0    ←0
  │ __init__                     5L  0C    0m  CC=0.0    ←0
  │ paths                        5L  0C    0m  CC=0.0    ←0
  │ __init__                     4L  0C    0m  CC=0.0    ←0
  │ __init__                     4L  0C    0m  CC=0.0    ←0
  │ __init__                     4L  0C    0m  CC=0.0    ←0
  │ .generated.yaml              4L  0C    0m  CC=0.0    ←0
  │ __init__                     4L  0C    0m  CC=0.0    ←0
  │ .generated.yaml              4L  0C    0m  CC=0.0    ←0
  │ __init__                     4L  0C    0m  CC=0.0    ←0
  │ __init__                     3L  0C    0m  CC=0.0    ←0
  │ __init__                     3L  0C    0m  CC=0.0    ←0
  │ __init__                     3L  0C    0m  CC=0.0    ←0
  │
  meta_agent/                     CC̄=3.5    ←in:4  →out:8  !! split
  │ planner                      0L  0C    5m  CC=9      ←2
  │ api                          0L  2C    7m  CC=2      ←0
  │ models                       0L  3C    1m  CC=1      ←0
  │ loader                       0L  0C    2m  CC=2      ←1
  │ pipeline                     0L  0C    1m  CC=2      ←3
  │ rules                        0L  0C    6m  CC=8      ←1
  │ __init__                     0L  0C    0m  CC=0.0    ←0
  │ __init__                     0L  0C    0m  CC=0.0    ←0
  │ domain_pack_generator        0L  0C    0m  CC=0.0    ←0
  │ llm_planner                  0L  0C    0m  CC=0.0    ←0
  │ __init__                     0L  0C    0m  CC=0.0    ←0
  │
  hypervisor/                     CC̄=3.2    ←in:0  →out:0
  │ pypi_resolver                0L  0C    1m  CC=5      ←1
  │ templates                    0L  0C    5m  CC=1      ←0
  │ cli                          0L  0C    1m  CC=5      ←0
  │ capability_tests             0L  0C    1m  CC=4      ←1
  │ gate                         0L  1C    1m  CC=5      ←0
  │ models                       0L  8C    9m  CC=4      ←0
  │ env                          0L  0C    4m  CC=9      ←1
  │ validator                    0L  0C    1m  CC=6      ←1
  │ models                       0L  1C    1m  CC=5      ←1
  │ loader                       0L  0C    2m  CC=9      ←5
  │ registry_exporter            0L  0C    2m  CC=6      ←1
  │ schema_validator             0L  1C    4m  CC=6      ←1
  │ models                       0L  4C    3m  CC=4      ←0
  │ registry_builder             0L  0C    4m  CC=5      ←3
  │ writer                       0L  0C    4m  CC=3      ←1
  │ checker                      0L  0C    2m  CC=8      ←0
  │ _version                     0L  0C    0m  CC=0.0    ←0
  │ __init__                     0L  0C    0m  CC=0.0    ←0
  │ __init__                     0L  0C    0m  CC=0.0    ←0
  │ function_resolver            0L  0C    0m  CC=0.0    ←0
  │ protocol_resolver            0L  0C    0m  CC=0.0    ←0
  │ __init__                     0L  0C    0m  CC=0.0    ←0
  │ llm_resolver                 0L  0C    0m  CC=0.0    ←0
  │ router                       0L  0C    0m  CC=0.0    ←0
  │ env_resolver                 0L  0C    0m  CC=0.0    ←0
  │ __init__                     0L  0C    0m  CC=0.0    ←0
  │
  uri2ops/                        CC̄=3.1    ←in:0  →out:9  !! split
  │ cli                          0L  0C    8m  CC=6      ←0
  │ validator                    0L  0C    2m  CC=14     ←3
  │ loader                       0L  0C    3m  CC=10     ←2
  │ models                       0L  2C    5m  CC=2      ←24
  │ dispatcher                   0L  0C    3m  CC=3      ←3
  │ mcp_wrapper                  0L  0C    2m  CC=2      ←1
  │ app                          0L  2C    1m  CC=1      ←1
  │ a2a_wrapper                  0L  0C    1m  CC=3      ←1
  │ service                      0L  1C    9m  CC=2      ←3
  │ loader                       0L  0C    8m  CC=14     ←5
  │ operation_registry.schema.json     0L  0C    0m  CC=0.0    ←0
  │ operator_task.schema.json     0L  0C    0m  CC=0.0    ←0
  │ registry.yaml                0L  0C    0m  CC=0.0    ←0
  │
  domains/                        CC̄=3.0    ←in:0  →out:0
  │ uri_tree.yaml               85L  0C    0m  CC=0.0    ←0
  │ weather_map.proto           41L  0C    0m  CC=0.0    ←0
  │ generate_weather_map        24L  0C    1m  CC=3      ←0
  │ resources.yaml              23L  0C    0m  CC=0.0    ←0
  │ views.yaml                  11L  0C    0m  CC=0.0    ←0
  │ renderers.yaml              10L  0C    0m  CC=0.0    ←0
  │ domain.yaml                  9L  0C    0m  CC=0.0    ←0
  │ commands.yaml                8L  0C    0m  CC=0.0    ←0
  │ registry.fragment.yaml       2L  0C    0m  CC=0.0    ←0
  │
  uri3/                           CC̄=2.7    ←in:0  →out:0
  │ uri_graph                    0L  3C    3m  CC=10     ←2
  │ uri_validator                0L  0C    1m  CC=2      ←2
  │ normalizer                   0L  0C    1m  CC=3      ←0
  │ parser                       0L  1C    1m  CC=2      ←4
  │ http_resolver                0L  1C    2m  CC=2      ←1
  │ llm_resolver                 0L  2C    2m  CC=5      ←2
  │ python_resolver              0L  1C    5m  CC=2      ←2
  │ base                         0L  1C    0m  CC=0.0    ←0
  │ __init__                     0L  0C    0m  CC=0.0    ←0
  │
  testenv/                        CC̄=2.3    ←in:0  →out:0
  │ mock_agent_server           57L  1C    3m  CC=5      ←0
  │ Dockerfile                  20L  0C    0m  CC=0.0    ←0
  │ docker-compose.ssh.yml      10L  0C    0m  CC=0.0    ←0
  │ entrypoint.sh                7L  0C    0m  CC=0.0    ←0
  │
  examples/                       CC̄=2.2    ←in:0  →out:0
  │ run.sh                      85L  1C    2m  CC=0.0    ←0
  │ run.sh                      67L  0C    2m  CC=0.0    ←11
  │ voice_command               66L  0C    2m  CC=7      ←0
  │ tts                         48L  0C    2m  CC=3      ←0
  │ stt_mock.uri.capability.yaml    43L  0C    0m  CC=0.0    ←0
  │ tts_mock.uri.capability.yaml    43L  0C    0m  CC=0.0    ←0
  │ run.sh                      41L  0C    0m  CC=0.0    ←0
  │ weather_forecast.uri.capability.yaml    40L  0C    0m  CC=0.0    ←0
  │ expanded.expected.uri.graph.yaml    38L  0C    0m  CC=0.0    ←0
  │ run.sh                      38L  0C    0m  CC=0.0    ←0
  │ voice_command.uri.capability.yaml    36L  0C    0m  CC=0.0    ←0
  │ stt                         35L  0C    2m  CC=5      ←0
  │ task.android.yaml           35L  0C    0m  CC=0.0    ←0
  │ run.sh                      31L  0C    0m  CC=0.0    ←0
  │ task_graph.yaml             28L  0C    0m  CC=0.0    ←0
  │ task.health.yaml            28L  0C    0m  CC=0.0    ←0
  │ task.health.yaml            28L  0C    0m  CC=0.0    ←0
  │ task.pcwin.yaml             26L  0C    0m  CC=0.0    ←0
  │ browser_open_mock.uri.capability.yaml    24L  0C    0m  CC=0.0    ←0
  │ branching.uri.flow.yaml     20L  0C    0m  CC=0.0    ←0
  │ run.sh                      20L  0C    0m  CC=0.0    ←0
  │ check_health_graph.uri.capability.yaml    19L  0C    0m  CC=0.0    ←0
  │ weather_flow_dry_run.uri.capability.yaml    19L  0C    0m  CC=0.0    ←0
  │ run.sh                      18L  0C    0m  CC=0.0    ←0
  │ run.sh                      17L  0C    0m  CC=0.0    ←0
  │ run.sh                      17L  0C    0m  CC=0.0    ←0
  │ mock_echo.uri.capability.yaml    12L  0C    0m  CC=0.0    ←0
  │ docker-compose.yml          10L  0C    0m  CC=0.0    ←0
  │ weather.uri.flow.yaml        9L  0C    0m  CC=0.0    ←0
  │ weather.uri.flow.yaml        9L  0C    0m  CC=0.0    ←0
  │ run.sh                       8L  0C    0m  CC=0.0    ←0
  │ run.sh                       8L  0C    0m  CC=0.0    ←0
  │ run.sh                       7L  0C    0m  CC=0.0    ←0
  │ run.sh                       7L  0C    0m  CC=0.0    ←0
  │ run.sh                       7L  0C    0m  CC=0.0    ←0
  │ run.sh                       5L  0C    0m  CC=0.0    ←0
  │ prompt.txt                   1L  0C    0m  CC=0.0    ←0
  │ prompt.txt                   1L  0C    0m  CC=0.0    ←0
  │ create_orders_agent.yaml     0L  0C    0m  CC=0.0    ←0
  │ broken_agent.yaml            0L  0C    0m  CC=0.0    ←0
  │ create_invoices_agent_prompt.txt     0L  0C    0m  CC=0.0    ←0
  │ __init__                     0L  0C    0m  CC=0.0    ←0
  │
  runtime_client/                 CC̄=1.7    ←in:0  →out:0
  │ client                       0L  1C    3m  CC=2      ←0
  │
  nl2uri/                         CC̄=1.0    ←in:3  →out:0
  │ writer                       0L  0C    1m  CC=1      ←2
  │
  nl2a/                           CC̄=1.0    ←in:0  →out:1
  │ cli                          0L  0C    2m  CC=1      ←0
  │
  ./                              CC̄=0.0    ←in:0  →out:0
  │ !! planfile.yaml             1319L  0C    0m  CC=0.0    ←0
  │ !! goal.yaml                  511L  0C    0m  CC=0.0    ←0
  │ tree.txt                   240L  0C    0m  CC=0.0    ←0
  │ pyproject.toml             163L  0C    0m  CC=0.0    ←0
  │ Makefile                   111L  0C    0m  CC=0.0    ←0
  │ prefact.yaml                97L  0C    0m  CC=0.0    ←0
  │ project.sh                  59L  0C    0m  CC=0.0    ←0
  │ manifest.yaml               20L  0C    0m  CC=0.0    ←0
  │ docker-compose.yml          18L  0C    0m  CC=0.0    ←0
  │ Dockerfile                  13L  0C    0m  CC=0.0    ←0
  │ nlp2uri.yaml                 8L  0C    0m  CC=0.0    ←0
  │
  schemas/                        CC̄=0.0    ←in:0  →out:0
  │ contract_registry.schema.json   129L  0C    0m  CC=0.0    ←0
  │ agent_contract.schema.json    79L  0C    0m  CC=0.0    ←0
  │ uri_tree.schema.json        78L  0C    0m  CC=0.0    ←0
  │ workflow_graph.schema.json    69L  0C    0m  CC=0.0    ←0
  │ resources.schema.json       56L  0C    0m  CC=0.0    ←0
  │ views.schema.json           54L  0C    0m  CC=0.0    ←0
  │ evolution_proposal.schema.json    48L  0C    0m  CC=0.0    ←0
  │ command_contract.schema.json    43L  0C    0m  CC=0.0    ←0
  │ renderer_contract.schema.json    35L  0C    0m  CC=0.0    ←0
  │ uri_graph.schema.json       31L  0C    0m  CC=0.0    ←0
  │ domain_pack.schema.json     20L  0C    0m  CC=0.0    ←0
  │
  contracts/                      CC̄=0.0    ←in:0  →out:0
  │ user.proto                  39L  0C    0m  CC=0.0    ←0
  │ user_agent.yaml             38L  0C    0m  CC=0.0    ←0
  │ views.yaml                  34L  0C    0m  CC=0.0    ←0
  │ resources.yaml              29L  0C    0m  CC=0.0    ←0
  │ standards.yaml              28L  0C    0m  CC=0.0    ←0
  │ registry.yaml               28L  0C    0m  CC=0.0    ←0
  │ policy.yaml                 24L  0C    0m  CC=0.0    ←0
  │ weather_map_agent.yaml      22L  0C    0m  CC=0.0    ←0
  │
  evolution/                      CC̄=0.0    ←in:0  →out:0
  │ add_invoices_agent.yaml      0L  0C    0m  CC=0.0    ←0
  │ add_orders_agent.yaml        0L  0C    0m  CC=0.0    ←0
  │
  deployments/                    CC̄=0.0    ←in:0  →out:0
  │ agent_deployments.yaml      29L  0C    0m  CC=0.0    ←0
  │
  testql-scenarios/               CC̄=0.0    ←in:0  →out:0
  │ generated-api-smoke.testql.toon.yaml    35L  0C    0m  CC=0.0    ←0
  │ generated-cli-tests.testql.toon.yaml    20L  0C    0m  CC=0.0    ←0
  │ generated-from-pytests.testql.toon.yaml    14L  0C    0m  CC=0.0    ←0
  │
  config/                         CC̄=0.0    ←in:0  →out:0
  │ flow_defaults.uri.yaml     132L  0C    0m  CC=0.0    ←0
  │ llm.uri.yaml                57L  0C    0m  CC=0.0    ←0
  │ operator_policy.uri.yaml    43L  0C    0m  CC=0.0    ←0
  │ docker.uri.yaml             25L  0C    0m  CC=0.0    ←0
  │ deployments.uri.yaml        18L  0C    0m  CC=0.0    ←0
  │ uri3.uri.yaml               17L  0C    0m  CC=0.0    ←0
  │ ssh.uri.yaml                15L  0C    0m  CC=0.0    ←0
  │ runtime.uri.yaml            12L  0C    0m  CC=0.0    ←0
  │ extra_operator_registry.yaml    11L  0C    0m  CC=0.0    ←0
  │ touri.uri.yaml              11L  0C    0m  CC=0.0    ←0
  │ operator_registry.uri.yaml     9L  0C    0m  CC=0.0    ←0
  │
  agents/                         CC̄=0.0    ←in:0  →out:0
  │ agent_card                  63L  0C    0m  CC=0.0    ←0
  │ agent_card                  40L  0C    0m  CC=0.0    ←0
  │ main                        16L  0C    0m  CC=0.0    ←0
  │ main                        16L  0C    0m  CC=0.0    ←0
  │ Dockerfile                   9L  0C    0m  CC=0.0    ←0
  │ Dockerfile                   9L  0C    0m  CC=0.0    ←0
  │ __init__                     4L  0C    0m  CC=0.0    ←0
  │ .generated.yaml              4L  0C    0m  CC=0.0    ←0
  │ __init__                     4L  0C    0m  CC=0.0    ←0
  │ .generated.yaml              4L  0C    0m  CC=0.0    ←0
  │
  integration/                    CC̄=0.0    ←in:0  →out:0
  │ Makefile.optional.snippet.mk    11L  0C    0m  CC=0.0    ←0
  │ pyproject.optional.snippet.toml    10L  0C    0m  CC=0.0    ←0
  │ Makefile.optional.snippet.mk     9L  0C    0m  CC=0.0    ←0
  │ pyproject.optional.snippet.toml     5L  0C    0m  CC=0.0    ←0
  │
  ── zero ──
     evolution/proposals/add_invoices_agent.yaml  0L
     evolution/proposals/add_orders_agent.yaml  0L
     examples/21_touri_voice/touri_examples_voice/__init__.py  0L
     examples/broken_agent.yaml                0L
     examples/create_invoices_agent_prompt.txt  0L
     examples/create_orders_agent.yaml         0L
     generator/__init__.py                     0L
     generator/hashutil.py                     0L
     generator/model.py                        0L
     generator/templates/Dockerfile.j2         0L
     generator/validate.py                     0L
     generator/verify.py                       0L
     hypervisor/__init__.py                    0L
     hypervisor/_version.py                    0L
     hypervisor/compatibility/checker.py       0L
     hypervisor/config/__init__.py             0L
     hypervisor/config/env.py                  0L
     hypervisor/config/models.py               0L
     hypervisor/contract_registry/loader.py    0L
     hypervisor/contract_registry/models.py    0L
     hypervisor/contract_registry/registry_builder.py  0L
     hypervisor/contract_registry/registry_exporter.py  0L
     hypervisor/contract_registry/schema_validator.py  0L
     hypervisor/deployment_registry/writer.py  0L
     hypervisor/domain_pack/__init__.py        0L
     hypervisor/domain_pack/templates.py       0L
     hypervisor/evolution/models.py            0L
     hypervisor/evolution/validator.py         0L
     hypervisor/policy_gate/gate.py            0L
     hypervisor/uri2llm/__init__.py            0L
     hypervisor/uri2llm/env_resolver.py        0L
     hypervisor/uri2llm/function_resolver.py   0L
     hypervisor/uri2llm/llm_resolver.py        0L
     hypervisor/uri2llm/protocol_resolver.py   0L
     hypervisor/uri2llm/pypi_resolver.py       0L
     hypervisor/uri2llm/router.py              0L
     hypervisor/verifier/capability_tests.py   0L
     hypervisor/verifier/cli.py                0L
     meta_agent/__init__.py                    0L
     meta_agent/api.py                         0L
     meta_agent/domain_planner/__init__.py     0L
     meta_agent/domain_planner/domain_pack_generator.py  0L
     meta_agent/domain_planner/llm_planner.py  0L
     meta_agent/models.py                      0L
     meta_agent/planner.py                     0L
     meta_agent/repair/__init__.py             0L
     meta_agent/repair/loader.py               0L
     meta_agent/repair/pipeline.py             0L
     meta_agent/repair/rules.py                0L
     nl2a/cli.py                               0L
     nl2uri/writer.py                          0L
     runtime_client/client.py                  0L
     uri2ops/cli.py                            0L
     uri2ops/operation_registry/dispatcher.py  0L
     uri2ops/operation_registry/loader.py      0L
     uri2ops/operation_registry/models.py      0L
     uri2ops/operation_registry/registry.yaml  0L
     uri2ops/operation_registry/validator.py   0L
     uri2ops/remote_registry/loader.py         0L
     uri2ops/schemas/operation_registry.schema.json  0L
     uri2ops/schemas/operator_task.schema.json  0L
     uri2ops/server/a2a_wrapper.py             0L
     uri2ops/server/app.py                     0L
     uri2ops/server/mcp_wrapper.py             0L
     uri2ops/server/service.py                 0L
     uri3/graph/uri_graph.py                   0L
     uri3/protocols/normalizer.py              0L
     uri3/protocols/parser.py                  0L
     uri3/resolvers/__init__.py                0L
     uri3/resolvers/http_resolver.py           0L
     uri3/resolvers/llm_resolver.py            0L
     uri3/resolvers/python_resolver.py         0L
     uri3/scanner/base.py                      0L
     uri3/validators/uri_validator.py          0L

COUPLING:
                                                           packages.uri3  packages.resource-agent-hypervisor                      packages.touri                     packages.nl2uri          uri2ops.operation_registry             examples.21_touri_voice                           generator                   packages.uri2flow             uri2ops.remote_registry                          meta_agent        hypervisor.contract_registry     packages.resource-agent-factory                             uri2ops                      uri2ops.server                   meta_agent.repair
                       packages.uri3                                  ──                                  12                                   2                                 ←27                                  21                                                                                                           4                                   2                                                                                                          ←1                                                                                                              hub
  packages.resource-agent-hypervisor                                  46                                  ──                                                                       1                                   3                                  24                                   4                                   1                                                                       3                                   7                                   1                                                                                                           2  hub
                      packages.touri                                  49                                                                      ──                                                                       4                                   1                                                                       1                                                                                                                                                                                                                                                              !! fan-out
                     packages.nl2uri                                  27                                   2                                                                      ──                                   9                                  ←1                                   1                                   5                                                                                                           1                                   1                                                                       1                                      !! fan-out
          uri2ops.operation_registry                                 ←21                                  ←3                                  ←4                                  ←9                                  ──                                                                                                                                               1                                                                                                                                              ←2                                  ←1                                      hub
             examples.21_touri_voice                                                                     ←24                                  ←1                                   1                                                                      ──                                  ←8                                  ←3                                                                                                                                              ←2                                  ←1                                                                          hub
                           generator                                                                      ←4                                                                      ←1                                                                       8                                  ──                                                                                                          ←2                                                                      ←4                                                                                                          ←3  hub
                   packages.uri2flow                                   1                                  ←1                                  ←1                                  ←5                                                                       3                                                                      ──                                                                                                                                                                                                                                                              hub
             uri2ops.remote_registry                                  ←2                                                                                                                                               4                                                                                                                                              ──                                                                                                                                              ←3                                  ←3                                      hub
                          meta_agent                                                                       5                                                                                                                                                                                   2                                                                                                          ──                                                                                                                                                                                   1  !! fan-out
        hypervisor.contract_registry                                                                      ←7                                                                      ←1                                                                                                                                                                                                                                                          ──                                                                                                                                                  hub
     packages.resource-agent-factory                                   1                                  ←1                                                                      ←1                                                                       2                                   4                                                                                                                                                                                  ──                                                                                                            
                             uri2ops                                                                                                                                                                                   2                                   1                                                                                                           3                                                                                                                                              ──                                   3                                      !! fan-out
                      uri2ops.server                                                                                                                                              ←1                                   1                                                                                                                                               3                                                                                                                                              ←3                                  ──                                    
                   meta_agent.repair                                                                      ←2                                                                                                                                                                                   3                                                                                                           1                                                                                                                                                                                  ──
  CYCLES: none
  HUB: hypervisor.contract_registry/ (fan-in=11)
  HUB: uri3.resolvers/ (fan-in=5)
  HUB: uri2ops.operation_registry/ (fan-in=45)
  HUB: examples.21_touri_voice/ (fan-in=43)
  HUB: generator/ (fan-in=14)
  HUB: packages.uri3/ (fan-in=125)
  HUB: uri2ops.remote_registry/ (fan-in=9)
  HUB: packages.uri2flow/ (fan-in=11)
  HUB: packages.resource-agent-hypervisor/ (fan-in=21)
  SMELL: packages.touri/ fan-out=55 → split needed
  SMELL: meta_agent/ fan-out=8 → split needed
  SMELL: uri2ops/ fan-out=9 → split needed
  SMELL: packages.nl2uri/ fan-out=50 → split needed
  SMELL: generator/ fan-out=8 → split needed
  SMELL: packages.uri3/ fan-out=51 → split needed
  SMELL: packages.resource-agent-hypervisor/ fan-out=98 → split needed

EXTERNAL:
  validation: run `vallm batch .` → validation.toon
  duplication: run `redup scan .` → duplication.toon
```

### Duplication (`project/duplication.toon.yaml`)

```toon markpact:analysis path=project/duplication.toon.yaml
# redup/duplication | 25 groups | 325f 15735L | 2026-06-14

SUMMARY:
  files_scanned: 325
  total_lines:   15735
  dup_groups:    25
  dup_fragments: 65
  saved_lines:   360
  scan_ms:       2861

HOTSPOTS[7] (files with most duplication):
  packages/touri/touri/backends/uri_graph_backend.py  dup=78L  groups=4  frags=4  (0.5%)
  packages/resource-agent-hypervisor/hypervisor/domain_pack/templates.py  dup=76L  groups=1  frags=3  (0.5%)
  packages/touri/touri/backends/uri_flow_backend.py  dup=73L  groups=3  frags=3  (0.5%)
  packages/nl2uri/nl2uri/cli.py  dup=50L  groups=2  frags=4  (0.3%)
  packages/uri3/uri3/protocols/schemes/instance_parser.py  dup=40L  groups=1  frags=10  (0.3%)
  domains/weather_map/handlers/generate_weather_map.py  dup=18L  groups=1  frags=1  (0.1%)
  packages/uri3/domains/weather_map/handlers/generate_weather_map.py  dup=18L  groups=1  frags=1  (0.1%)

DUPLICATES[25] (ranked by impact):
  [49d1d03e6ce392a1] ! STRU  weather_proto  L=43 N=3 saved=86 sim=1.00
      packages/resource-agent-hypervisor/hypervisor/domain_pack/templates.py:36-78  (weather_proto)
      packages/resource-agent-hypervisor/hypervisor/domain_pack/templates.py:81-106  (weather_handler)
      packages/resource-agent-hypervisor/hypervisor/domain_pack/templates.py:109-115  (generic_handler)
  [fffd82ea9b5a9412] ! STRU  call_uri_flow_backend  L=57 N=2 saved=57 sim=1.00
      packages/touri/touri/backends/uri_flow_backend.py:31-87  (call_uri_flow_backend)
      packages/touri/touri/backends/uri_graph_backend.py:39-95  (call_uri_graph_backend)
  [5ec23e21699e8ab6] ! STRU  _parse_env  L=4 N=10 saved=36 sim=1.00
      packages/uri3/uri3/protocols/schemes/instance_parser.py:27-30  (_parse_env)
      packages/uri3/uri3/protocols/schemes/instance_parser.py:33-36  (_parse_python)
      packages/uri3/uri3/protocols/schemes/instance_parser.py:39-42  (_parse_llm)
      packages/uri3/uri3/protocols/schemes/instance_parser.py:45-48  (_parse_pypi)
      packages/uri3/uri3/protocols/schemes/instance_parser.py:51-54  (_parse_http)
      packages/uri3/uri3/protocols/schemes/instance_parser.py:57-60  (_parse_a2a)
      packages/uri3/uri3/protocols/schemes/instance_parser.py:63-66  (_parse_mcp)
      packages/uri3/uri3/protocols/schemes/instance_parser.py:69-72  (_parse_docker)
      packages/uri3/uri3/protocols/schemes/instance_parser.py:75-78  (_parse_ssh)
      packages/uri3/uri3/protocols/schemes/instance_parser.py:81-84  (_parse_resource)
  [3923fa783ad8b9c2]   STRU  task  L=19 N=2 saved=19 sim=1.00
      packages/nl2uri/nl2uri/cli.py:176-194  (task)
      packages/nl2uri/nl2uri/cli.py:198-216  (graph)
  [1b86825b8b7cb469]   EXAC  handler  L=18 N=2 saved=18 sim=1.00
      domains/weather_map/handlers/generate_weather_map.py:7-24  (handler)
      packages/uri3/domains/weather_map/handlers/generate_weather_map.py:7-24  (handler)
  [16b912bffbd4a264]   EXAC  _playwright_ready  L=17 N=2 saved=17 sim=1.00
      packages/uri2ops/uri2ops/operator/adapters/browser_router.py:12-28  (_playwright_ready)
      packages/uri3/uri3/graph/adapters/browser_router.py:15-31  (_playwright_ready)
  [70c693fa623a6ad1]   EXAC  _task_context  L=3 N=5 saved=12 sim=1.00
      packages/uri2ops/uri2ops/operator/adapters/android_adb.py:16-18  (_task_context)
      packages/uri2ops/uri2ops/operator/adapters/android_mock.py:10-12  (_task_context)
      packages/uri2ops/uri2ops/operator/adapters/browser_playwright.py:20-22  (_task_context)
      packages/uri2ops/uri2ops/operator/adapters/pcwin_mock.py:10-12  (_task_context)
      packages/uri2ops/uri2ops/operator/adapters/pcwin_uia.py:11-13  (_task_context)
  [f69df3cd4d46eb5f]   STRU  _slug  L=4 N=4 saved=12 sim=1.00
      packages/nl2uri/nl2uri/flow_repair.py:11-14  (_slug)
      packages/nl2uri/nl2uri/graph_planner.py:15-18  (_slug)
      packages/nl2uri/nl2uri/graph_repair.py:30-33  (_slug)
      packages/nl2uri/nl2uri/planner_templates.py:10-13  (slug)
  [277a3a34943f29ee]   STRU  python_file_header  L=6 N=3 saved=12 sim=1.00
      packages/resource-agent-factory/generator/header.py:21-26  (python_file_header)
      packages/resource-agent-factory/generator/header.py:29-34  (dockerfile_header)
      packages/resource-agent-factory/generator/header.py:37-42  (markdown_generated_banner)
  [71dc3d2f70a63bf5]   STRU  spec  L=12 N=2 saved=12 sim=1.00
      packages/uri3/uri3/protocols/schemes/a2a.py:4-15  (spec)
      packages/uri3/uri3/protocols/schemes/mcp.py:4-15  (spec)
  [f7665e0d5298a930]   EXAC  _resolve_path  L=10 N=2 saved=10 sim=1.00
      packages/touri/touri/backends/uri_flow_backend.py:11-20  (_resolve_path)
      packages/touri/touri/backends/uri_graph_backend.py:12-21  (_resolve_path)
  [0e9dc2bdedc9fb73]   STRU  window_id_from_payload  L=7 N=2 saved=7 sim=1.00
      packages/uri2ops/uri2ops/operator/adapters/pcwin_uri.py:32-38  (window_id_from_payload)
      packages/uri2ops/uri2ops/operator/adapters/pcwin_uri.py:41-47  (automation_id_from_payload)
  [57ca7801c3faf7f6]   EXAC  _execution_options  L=6 N=2 saved=6 sim=1.00
      packages/touri/touri/backends/uri_flow_backend.py:23-28  (_execution_options)
      packages/touri/touri/backends/uri_graph_backend.py:24-29  (_execution_options)
  [c3b5ea290d7363ba]   STRU  single  L=6 N=2 saved=6 sim=1.00
      packages/nl2uri/nl2uri/cli.py:108-113  (single)
      packages/nl2uri/nl2uri/cli.py:117-122  (list_cmd)
  [fdc7786ef049b370]   STRU  deploy_agent_cmd  L=6 N=2 saved=6 sim=1.00
      packages/resource-agent-hypervisor/hypervisor/cli.py:111-116  (deploy_agent_cmd)
      packages/resource-agent-hypervisor/hypervisor/cli.py:129-134  (docker_cmd)
  [25db8c6fcea03672]   STRU  adjacency  L=6 N=2 saved=6 sim=1.00
      packages/uri3/uri3/graph/dependency_graph.py:9-14  (adjacency)
      packages/uri3/uri3/graph/dependency_graph.py:17-22  (reverse_adjacency)
  [c65ebbaef9c567e1]   EXAC  _artifact_dir  L=5 N=2 saved=5 sim=1.00
      examples/21_touri_voice/touri_examples_voice/tts.py:9-13  (_artifact_dir)
      examples/21_touri_voice/touri_examples_voice/voice_command.py:9-13  (_artifact_dir)
  [fe6e01c31980976b]   STRU  _load_graph  L=5 N=2 saved=5 sim=1.00
      packages/touri/touri/backends/uri_graph_backend.py:32-36  (_load_graph)
      packages/touri/touri/manifest.py:11-15  (_read_yaml)
  [9a928c6cb43e19ba]   STRU  _first  L=5 N=2 saved=5 sim=1.00
      packages/uri3/uri3/resolvers/docker_resolver.py:61-65  (_first)
      packages/uri3/uri3/resolvers/log_query.py:7-11  (first)
  [06621f22a60e830d]   STRU  _bool  L=5 N=2 saved=5 sim=1.00
      packages/uri3/uri3/resolvers/docker_resolver.py:68-72  (_bool)
      packages/uri3/uri3/resolvers/log_query.py:24-28  (query_bool)
  [ce21e3511c8ea01e]   EXAC  _registry_scheme  L=4 N=2 saved=4 sim=1.00
      packages/touri/touri/backends/uri2ops_backend.py:27-30  (_registry_scheme)
      packages/uri3/uri3/graph/adapters/uri2ops_adapter.py:37-40  (_registry_scheme)
  [9fb5c83bb992966d]   STRU  validate_flow_document  L=4 N=2 saved=4 sim=1.00
      packages/nl2uri/nl2uri/flow_repair.py:207-210  (validate_flow_document)
      packages/nl2uri/nl2uri/flow_repair.py:213-216  (validate_expanded_flow)
  [060fe645d32f78c5]   STRU  run_build_command  L=4 N=2 saved=4 sim=1.00
      packages/resource-agent-hypervisor/hypervisor/contract_registry/cli_commands.py:33-36  (run_build_command)
      packages/resource-agent-hypervisor/hypervisor/contract_registry/cli_commands.py:39-42  (run_export_md_command)
  [e9d49a2572194471]   STRU  policy_config_path  L=3 N=2 saved=3 sim=1.00
      packages/uri2ops/uri2ops/operator/policy_loader.py:60-62  (policy_config_path)
      packages/uri2ops/uri2ops/remote_registry/loader.py:17-19  (registry_config_path)
  [bc6d855bfb035b8b]   STRU  resolve_a2a  L=3 N=2 saved=3 sim=1.00
      packages/uri3/uri3/resolvers/protocol_resolver.py:10-12  (resolve_a2a)
      packages/uri3/uri3/resolvers/protocol_resolver.py:15-17  (resolve_mcp)

REFACTOR[25] (ranked by priority):
  [1] ○ extract_function   → packages/resource-agent-hypervisor/hypervisor/domain_pack/utils/weather_proto.py
      WHY: 3 occurrences of 43-line block across 1 files — saves 86 lines
      FILES: packages/resource-agent-hypervisor/hypervisor/domain_pack/templates.py
  [2] ◐ extract_module     → packages/touri/touri/backends/utils/call_uri_flow_backend.py
      WHY: 2 occurrences of 57-line block across 2 files — saves 57 lines
      FILES: packages/touri/touri/backends/uri_flow_backend.py, packages/touri/touri/backends/uri_graph_backend.py
  [3] ○ extract_function   → packages/uri3/uri3/protocols/schemes/utils/_parse_env.py
      WHY: 10 occurrences of 4-line block across 1 files — saves 36 lines
      FILES: packages/uri3/uri3/protocols/schemes/instance_parser.py
  [4] ○ extract_function   → packages/nl2uri/nl2uri/utils/task.py
      WHY: 2 occurrences of 19-line block across 1 files — saves 19 lines
      FILES: packages/nl2uri/nl2uri/cli.py
  [5] ○ extract_function   → utils/handler.py
      WHY: 2 occurrences of 18-line block across 2 files — saves 18 lines
      FILES: domains/weather_map/handlers/generate_weather_map.py, packages/uri3/domains/weather_map/handlers/generate_weather_map.py
  [6] ○ extract_function   → packages/utils/_playwright_ready.py
      WHY: 2 occurrences of 17-line block across 2 files — saves 17 lines
      FILES: packages/uri2ops/uri2ops/operator/adapters/browser_router.py, packages/uri3/uri3/graph/adapters/browser_router.py
  [7] ○ extract_function   → packages/uri2ops/uri2ops/operator/adapters/utils/_task_context.py
      WHY: 5 occurrences of 3-line block across 5 files — saves 12 lines
      FILES: packages/uri2ops/uri2ops/operator/adapters/android_adb.py, packages/uri2ops/uri2ops/operator/adapters/android_mock.py, packages/uri2ops/uri2ops/operator/adapters/browser_playwright.py, packages/uri2ops/uri2ops/operator/adapters/pcwin_mock.py, packages/uri2ops/uri2ops/operator/adapters/pcwin_uia.py
  [8] ○ extract_function   → packages/nl2uri/nl2uri/utils/_slug.py
      WHY: 4 occurrences of 4-line block across 4 files — saves 12 lines
      FILES: packages/nl2uri/nl2uri/flow_repair.py, packages/nl2uri/nl2uri/graph_planner.py, packages/nl2uri/nl2uri/graph_repair.py, packages/nl2uri/nl2uri/planner_templates.py
  [9] ○ extract_function   → packages/resource-agent-factory/generator/utils/python_file_header.py
      WHY: 3 occurrences of 6-line block across 1 files — saves 12 lines
      FILES: packages/resource-agent-factory/generator/header.py
  [10] ○ extract_function   → packages/uri3/uri3/protocols/schemes/utils/spec.py
      WHY: 2 occurrences of 12-line block across 2 files — saves 12 lines
      FILES: packages/uri3/uri3/protocols/schemes/a2a.py, packages/uri3/uri3/protocols/schemes/mcp.py
  [11] ○ extract_function   → packages/touri/touri/backends/utils/_resolve_path.py
      WHY: 2 occurrences of 10-line block across 2 files — saves 10 lines
      FILES: packages/touri/touri/backends/uri_flow_backend.py, packages/touri/touri/backends/uri_graph_backend.py
  [12] ○ extract_function   → packages/uri2ops/uri2ops/operator/adapters/utils/window_id_from_payload.py
      WHY: 2 occurrences of 7-line block across 1 files — saves 7 lines
      FILES: packages/uri2ops/uri2ops/operator/adapters/pcwin_uri.py
  [13] ○ extract_function   → packages/touri/touri/backends/utils/_execution_options.py
      WHY: 2 occurrences of 6-line block across 2 files — saves 6 lines
      FILES: packages/touri/touri/backends/uri_flow_backend.py, packages/touri/touri/backends/uri_graph_backend.py
  [14] ○ extract_function   → packages/nl2uri/nl2uri/utils/single.py
      WHY: 2 occurrences of 6-line block across 1 files — saves 6 lines
      FILES: packages/nl2uri/nl2uri/cli.py
  [15] ○ extract_function   → packages/resource-agent-hypervisor/hypervisor/utils/deploy_agent_cmd.py
      WHY: 2 occurrences of 6-line block across 1 files — saves 6 lines
      FILES: packages/resource-agent-hypervisor/hypervisor/cli.py
  [16] ○ extract_function   → packages/uri3/uri3/graph/utils/adjacency.py
      WHY: 2 occurrences of 6-line block across 1 files — saves 6 lines
      FILES: packages/uri3/uri3/graph/dependency_graph.py
  [17] ○ extract_function   → examples/21_touri_voice/touri_examples_voice/utils/_artifact_dir.py
      WHY: 2 occurrences of 5-line block across 2 files — saves 5 lines
      FILES: examples/21_touri_voice/touri_examples_voice/tts.py, examples/21_touri_voice/touri_examples_voice/voice_command.py
  [18] ○ extract_function   → packages/touri/touri/utils/_load_graph.py
      WHY: 2 occurrences of 5-line block across 2 files — saves 5 lines
      FILES: packages/touri/touri/backends/uri_graph_backend.py, packages/touri/touri/manifest.py
  [19] ○ extract_function   → packages/uri3/uri3/resolvers/utils/_first.py
      WHY: 2 occurrences of 5-line block across 2 files — saves 5 lines
      FILES: packages/uri3/uri3/resolvers/docker_resolver.py, packages/uri3/uri3/resolvers/log_query.py
  [20] ○ extract_function   → packages/uri3/uri3/resolvers/utils/_bool.py
      WHY: 2 occurrences of 5-line block across 2 files — saves 5 lines
      FILES: packages/uri3/uri3/resolvers/docker_resolver.py, packages/uri3/uri3/resolvers/log_query.py
  [21] ○ extract_function   → packages/utils/_registry_scheme.py
      WHY: 2 occurrences of 4-line block across 2 files — saves 4 lines
      FILES: packages/touri/touri/backends/uri2ops_backend.py, packages/uri3/uri3/graph/adapters/uri2ops_adapter.py
  [22] ○ extract_function   → packages/nl2uri/nl2uri/utils/validate_flow_document.py
      WHY: 2 occurrences of 4-line block across 1 files — saves 4 lines
      FILES: packages/nl2uri/nl2uri/flow_repair.py
  [23] ○ extract_function   → packages/resource-agent-hypervisor/hypervisor/contract_registry/utils/run_build_command.py
      WHY: 2 occurrences of 4-line block across 1 files — saves 4 lines
      FILES: packages/resource-agent-hypervisor/hypervisor/contract_registry/cli_commands.py
  [24] ○ extract_function   → packages/uri2ops/uri2ops/utils/policy_config_path.py
      WHY: 2 occurrences of 3-line block across 2 files — saves 3 lines
      FILES: packages/uri2ops/uri2ops/operator/policy_loader.py, packages/uri2ops/uri2ops/remote_registry/loader.py
  [25] ○ extract_function   → packages/uri3/uri3/resolvers/utils/resolve_a2a.py
      WHY: 2 occurrences of 3-line block across 1 files — saves 3 lines
      FILES: packages/uri3/uri3/resolvers/protocol_resolver.py

QUICK_WINS[15] (low risk, high savings — do first):
  [1] extract_function   saved=86L  → packages/resource-agent-hypervisor/hypervisor/domain_pack/utils/weather_proto.py
      FILES: templates.py
  [3] extract_function   saved=36L  → packages/uri3/uri3/protocols/schemes/utils/_parse_env.py
      FILES: instance_parser.py
  [4] extract_function   saved=19L  → packages/nl2uri/nl2uri/utils/task.py
      FILES: cli.py
  [5] extract_function   saved=18L  → utils/handler.py
      FILES: generate_weather_map.py, generate_weather_map.py
  [6] extract_function   saved=17L  → packages/utils/_playwright_ready.py
      FILES: browser_router.py, browser_router.py
  [7] extract_function   saved=12L  → packages/uri2ops/uri2ops/operator/adapters/utils/_task_context.py
      FILES: android_adb.py, android_mock.py, browser_playwright.py +2
  [8] extract_function   saved=12L  → packages/nl2uri/nl2uri/utils/_slug.py
      FILES: flow_repair.py, graph_planner.py, graph_repair.py +1
  [9] extract_function   saved=12L  → packages/resource-agent-factory/generator/utils/python_file_header.py
      FILES: header.py
  [10] extract_function   saved=12L  → packages/uri3/uri3/protocols/schemes/utils/spec.py
      FILES: a2a.py, mcp.py
  [11] extract_function   saved=10L  → packages/touri/touri/backends/utils/_resolve_path.py
      FILES: uri_flow_backend.py, uri_graph_backend.py

DEPENDENCY_RISK[1] (duplicates spanning multiple packages):
  handler  packages=2  files=2
      domains/weather_map/handlers/generate_weather_map.py
      packages/uri3/domains/weather_map/handlers/generate_weather_map.py

EFFORT_ESTIMATE (total ≈ 15.0h):
  hard   weather_proto                       saved=86L  ~258min
  hard   call_uri_flow_backend               saved=57L  ~171min
  medium _parse_env                          saved=36L  ~72min
  medium task                                saved=19L  ~38min
  medium handler                             saved=18L  ~72min
  medium _playwright_ready                   saved=17L  ~34min
  easy   _task_context                       saved=12L  ~24min
  easy   _slug                               saved=12L  ~24min
  easy   python_file_header                  saved=12L  ~24min
  easy   spec                                saved=12L  ~24min
  ... +15 more (~158min)

METRICS-TARGET:
  dup_groups:  25 → 0
  saved_lines: 360 lines recoverable
```

### Evolution / Churn (`project/evolution.toon.yaml`)

```toon markpact:analysis path=project/evolution.toon.yaml
# code2llm/evolution | 750 func | 224f | 2026-06-14
# generated in 0.00s

NEXT[10] (ranked by impact):
  [1] !  SPLIT-FUNC      run_workflow  CC=22  fan=25
      WHY: CC=22 exceeds 15
      EFFORT: ~1h  IMPACT: 550

  [2] !  SPLIT-FUNC      call_uri2ops_backend  CC=17  fan=19
      WHY: CC=17 exceeds 15
      EFFORT: ~1h  IMPACT: 323

  [3] !  SPLIT-FUNC      classify_output_kind  CC=23  fan=11
      WHY: CC=23 exceeds 15
      EFFORT: ~1h  IMPACT: 253

  [4] !  SPLIT-FUNC      _ensure_step_ids  CC=19  fan=13
      WHY: CC=19 exceeds 15
      EFFORT: ~1h  IMPACT: 247

  [5] !  SPLIT-FUNC      apply_data_quality  CC=18  fan=13
      WHY: CC=18 exceeds 15
      EFFORT: ~1h  IMPACT: 234

  [6] !  SPLIT-FUNC      extract_flow_payload  CC=20  fan=10
      WHY: CC=20 exceeds 15
      EFFORT: ~1h  IMPACT: 200

  [7] !  SPLIT-FUNC      _call_backend  CC=18  fan=10
      WHY: CC=18 exceeds 15
      EFFORT: ~1h  IMPACT: 180

  [8] !  SPLIT-FUNC      load_manifest_from_dict  CC=16  fan=11
      WHY: CC=16 exceeds 15
      EFFORT: ~1h  IMPACT: 176

  [9] !  SPLIT-FUNC      sanitize_flow_step  CC=18  fan=9
      WHY: CC=18 exceeds 15
      EFFORT: ~1h  IMPACT: 162

  [10] !  SPLIT-FUNC      sanitize_node  CC=16  fan=10
      WHY: CC=16 exceeds 15
      EFFORT: ~1h  IMPACT: 160


RISKS[2]:
  ⚠ Splitting planfile.yaml may break 0 import paths
  ⚠ Splitting goal.yaml may break 0 import paths

METRICS-TARGET:
  CC̄:          3.8 → ≤2.7
  max-CC:      23 → ≤11
  god-modules: 2 → 0
  high-CC(≥15): 14 → ≤7
  hub-types:   0 → ≤0

PATTERNS (language parser shared logic):
  _extract_declarations() in base.py — unified extraction for:
    - TypeScript: interfaces, types, classes, functions, arrow funcs
    - PHP: namespaces, traits, classes, functions, includes
    - Ruby: modules, classes, methods, requires
    - C++: classes, structs, functions, #includes
    - C#: classes, interfaces, methods, usings
    - Java: classes, interfaces, methods, imports
    - Go: packages, functions, structs
    - Rust: modules, functions, traits, use statements

  Shared regex patterns per language:
    - import: language-specific import/require/using patterns
    - class: class/struct/trait declarations with inheritance
    - function: function/method signatures with visibility
    - brace_tracking: for C-family languages ({ })
    - end_keyword_tracking: for Ruby (module/class/def...end)

  Benefits:
    - Consistent extraction logic across all languages
    - Reduced code duplication (~70% reduction in parser LOC)
    - Easier maintenance: fix once, apply everywhere
    - Standardized FunctionInfo/ClassInfo models

HISTORY:
  prev CC̄=3.7 → now CC̄=3.8
```

## Intent

WronAI resource agent monorepo — uri3, nl2uri, uri2flow, uri2ops, touri, hypervisor, agent factory
