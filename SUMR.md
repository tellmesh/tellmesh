# Resource Agent System v0.5.7

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
- **version**: `0.5.9`
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
  version: 0.5.9;
}

dependencies {
  runtime: "fastapi>=0.115, httpx>=0.27, jinja2>=3.1, jsonschema>=4.23, pydantic>=2.0, python-dotenv>=1.0.0, pyyaml>=6.0, typer>=0.12";
  dev: "pytest>=7.0, pytest-cov>=4.0, pytest-asyncio>=0.21.0, ruff>=0.1.0, mypy>=1.0, build>=1.0, goal>=2.1.0, costs>=0.1.20, pfix>=0.1.60, rich>=13.0.0";
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

*374 nodes · 494 edges · 114 modules · CC̄=3.4*

### Hubs (by degree)

| Function | CC | in | out | total |
|----------|----|----|-----|-------|
| `load_contract_registry` *(in hypervisor.contract_registry.loader)* | 9 | 6 | 33 | **39** |
| `resolve_llm_profile` *(in packages.uri3.uri3.config.llm_profiles)* | 10 ⚠ | 2 | 32 | **34** |
| `merge_main_contracts` *(in hypervisor.contract_registry.merger)* | 12 ⚠ | 1 | 31 | **32** |
| `write_domain_pack` *(in packages.resource-agent-hypervisor.hypervisor.domain_pack.pack_writer)* | 3 | 1 | 30 | **31** |
| `infer_intent` *(in meta_agent.planner)* | 9 | 1 | 30 | **31** |
| `build_graph_from_tree` *(in uri3.graph.uri_graph)* | 10 ⚠ | 2 | 28 | **30** |
| `parse_docker_uri` *(in packages.uri3.uri3.resolvers.docker_resolver)* | 12 ⚠ | 5 | 23 | **28** |
| `load_agent_spec` *(in generator.model)* | 7 | 2 | 24 | **26** |

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/wronai/hypervisor
# generated in 0.20s
# nodes: 374 | edges: 494 | modules: 114
# CC̄=3.4

HUBS[20]:
  hypervisor.contract_registry.loader.load_contract_registry
    CC=9  in:6  out:33  total:39
  packages.uri3.uri3.config.llm_profiles.resolve_llm_profile
    CC=10  in:2  out:32  total:34
  hypervisor.contract_registry.merger.merge_main_contracts
    CC=12  in:1  out:31  total:32
  packages.resource-agent-hypervisor.hypervisor.domain_pack.pack_writer.write_domain_pack
    CC=3  in:1  out:30  total:31
  meta_agent.planner.infer_intent
    CC=9  in:1  out:30  total:31
  uri3.graph.uri_graph.build_graph_from_tree
    CC=10  in:2  out:28  total:30
  packages.uri3.uri3.resolvers.docker_resolver.parse_docker_uri
    CC=12  in:5  out:23  total:28
  generator.model.load_agent_spec
    CC=7  in:2  out:24  total:26
  hypervisor.contract_registry.cli.main
    CC=20  in:0  out:26  total:26
  packages.uri3.uri3.paths.find_repo_root
    CC=6  in:19  out:6  total:25
  packages.uri3.uri3.logs.reader.summarize_logs
    CC=6  in:6  out:18  total:24
  packages.uri3.uri3.resolvers.log_resolver.parse_log_uri
    CC=7  in:5  out:16  total:21
  packages.resource-agent-hypervisor.hypervisor.deployment_registry.runner.stop_agent
    CC=8  in:2  out:19  total:21
  packages.resource-agent-hypervisor.hypervisor.deployment_registry.runner.build_run_plan
    CC=10  in:3  out:18  total:21
  packages.resource-agent-hypervisor.hypervisor.cli_commands.echo_json
    CC=2  in:16  out:5  total:21
  packages.uri3.uri3.cli.scan
    CC=8  in:0  out:21  total:21
  packages.resource-agent-factory.generator.agent_generator.generate_agent
    CC=5  in:3  out:17  total:20
  packages.uri3.uri3.resolvers.env_resolver.call_env
    CC=8  in:2  out:17  total:19
  packages.resource-agent-hypervisor.hypervisor.deployment_registry.runner.run_agent
    CC=9  in:2  out:17  total:19
  packages.resource-agent-hypervisor.meta_agent.orchestrator.validate_repair_generate
    CC=7  in:3  out:16  total:19

MODULES:
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
  hypervisor.compatibility.checker  [1 funcs]
    classify_registry_change  CC=8  out:11
  hypervisor.config.env  [4 funcs]
    _parse_bool  CC=1  out:1
    apply_env_overrides  CC=1  out:2
    apply_legacy_env_overrides  CC=6  out:4
    apply_structured_env_overrides  CC=9  out:17
  hypervisor.contract_registry.cli  [1 funcs]
    main  CC=20  out:26
  hypervisor.contract_registry.loader  [2 funcs]
    _read_yaml  CC=3  out:4
    load_contract_registry  CC=9  out:33
  hypervisor.contract_registry.merger  [1 funcs]
    merge_main_contracts  CC=12  out:31
  hypervisor.contract_registry.registry_builder  [3 funcs]
    _contract_hash  CC=3  out:13
    build_registry_manifest  CC=5  out:9
    write_registry_manifest  CC=2  out:6
  hypervisor.contract_registry.registry_exporter  [2 funcs]
    export_json  CC=1  out:1
    export_markdown  CC=6  out:13
  hypervisor.contract_registry.schema_validator  [4 funcs]
    _read_json  CC=1  out:2
    _read_yaml  CC=2  out:2
    validate_contract_files  CC=6  out:13
    validate_file  CC=3  out:8
  hypervisor.deployment_registry.writer  [3 funcs]
    save_deployment_registry  CC=2  out:4
    upsert_deployment  CC=3  out:2
    write_deployment_registry  CC=1  out:2
  hypervisor.domain_pack.templates  [2 funcs]
    generic_proto  CC=1  out:1
    package_name  CC=1  out:0
  hypervisor.evolution.models  [1 funcs]
    load_proposal  CC=5  out:11
  hypervisor.evolution.validator  [1 funcs]
    validate_proposal  CC=6  out:6
  hypervisor.uri2llm.pypi_resolver  [1 funcs]
    resolve_pypi  CC=5  out:6
  hypervisor.verifier.capability_tests  [1 funcs]
    build_capability_test_plan  CC=4  out:2
  hypervisor.verifier.cli  [1 funcs]
    main  CC=5  out:8
  meta_agent.api  [6 funcs]
    generate  CC=2  out:6
    pipeline  CC=2  out:4
    proposal_from_prompt  CC=2  out:6
    repair  CC=2  out:5
    validate  CC=2  out:5
    verify  CC=1  out:2
  meta_agent.planner  [4 funcs]
    infer_intent  CC=9  out:30
    intent_to_agent_spec  CC=8  out:11
    package_name  CC=3  out:6
    singularize  CC=4  out:3
  meta_agent.repair.loader  [2 funcs]
    load_spec  CC=2  out:3
    write_spec  CC=1  out:2
  meta_agent.repair.pipeline  [1 funcs]
    repair_agent_spec  CC=2  out:12
  meta_agent.repair.rules  [6 funcs]
    repair_agent_block  CC=6  out:12
    repair_capabilities  CC=6  out:8
    repair_command_capability  CC=4  out:10
    repair_duplicate_capability_names  CC=5  out:5
    repair_missing_capability_type  CC=3  out:4
    repair_resource_read_capability  CC=8  out:14
  nl2a.cli  [1 funcs]
    generate  CC=1  out:5
  nl2uri.writer  [1 funcs]
    write_uri_tree  CC=1  out:4
  packages.nl2uri.nl2uri.cli  [1 funcs]
    generate  CC=5  out:16
  packages.nl2uri.nl2uri.domain_planner  [11 funcs]
    _call_openrouter  CC=4  out:8
    _deterministic_weather_plan  CC=2  out:2
    _extract_json  CC=3  out:8
    _generic_plan  CC=1  out:3
    _is_structured_uri_tree  CC=10  out:13
    _is_weather_prompt  CC=1  out:2
    _llm_uri_from_env  CC=6  out:7
    _normalize_llm_tree  CC=7  out:12
    _slug  CC=2  out:3
    _validate_tree_data  CC=2  out:6
  packages.nl2uri.nl2uri.llm_planner  [1 funcs]
    llm_plan  CC=2  out:4
  packages.nl2uri.nl2uri.pipeline  [4 funcs]
    _append_pipeline_logs  CC=2  out:4
    generate_tree  CC=1  out:1
    run_full_pipeline  CC=3  out:15
    run_generate_pipeline  CC=4  out:13
  packages.nl2uri.nl2uri.planner  [1 funcs]
    rule_based_plan  CC=1  out:2
  packages.resource-agent-factory.generator.agent_generator  [3 funcs]
    expand_paths  CC=4  out:7
    generate_agent  CC=5  out:17
    main  CC=5  out:4
  packages.resource-agent-factory.generator.header  [3 funcs]
    contract_source_ref  CC=3  out:7
    dockerfile_header  CC=1  out:0
    python_file_header  CC=1  out:0
  packages.resource-agent-factory.generator.paths  [2 funcs]
    find_repo_root  CC=6  out:6
    project_root  CC=1  out:1
  packages.resource-agent-hypervisor.hypervisor.cli  [13 funcs]
    agent_status_cmd  CC=1  out:5
    call  CC=1  out:4
    config_cmd  CC=2  out:7
    deploy_agent_cmd  CC=1  out:4
    deployments_list  CC=1  out:4
    docker_cmd  CC=1  out:4
    logs_cmd  CC=1  out:4
    resolve  CC=1  out:4
    restart_agent_cmd  CC=1  out:8
    run_agent_cmd  CC=1  out:8
  packages.resource-agent-hypervisor.hypervisor.cli_commands  [6 funcs]
    call_docker  CC=5  out:6
    deploy_agent  CC=7  out:16
    echo_json  CC=2  out:5
    read_agent_logs  CC=3  out:4
    run_local_agent  CC=6  out:15
    verify_agent  CC=4  out:8
  packages.resource-agent-hypervisor.hypervisor.config.config_checks  [4 funcs]
    validate_hypervisor  CC=7  out:7
    validate_llm  CC=4  out:4
    validate_path_sections  CC=5  out:5
    validate_uri3  CC=4  out:3
  packages.resource-agent-hypervisor.hypervisor.config.defaults  [4 funcs]
    apply_builtin_defaults  CC=1  out:17
    embedded_defaults_raw  CC=1  out:1
    get_default_config  CC=1  out:3
    load_yaml_file  CC=4  out:4
  packages.resource-agent-hypervisor.hypervisor.config.loader  [5 funcs]
    config_search_paths  CC=6  out:11
    get_config  CC=1  out:1
    load_config  CC=3  out:9
    load_hypervisor_config  CC=1  out:2
    resolve_config_path  CC=3  out:2
  packages.resource-agent-hypervisor.hypervisor.config.uri_config  [2 funcs]
    _repo_config_dir  CC=2  out:2
    apply_uri_yaml_configs  CC=10  out:14
  packages.resource-agent-hypervisor.hypervisor.config.validators  [2 funcs]
    merge_config  CC=5  out:5
    validate_config  CC=1  out:4
  packages.resource-agent-hypervisor.hypervisor.contract_registry.cross_checks.capabilities  [1 funcs]
    validate_capability_cross_refs  CC=13  out:6
  packages.resource-agent-hypervisor.hypervisor.contract_registry.cross_checks.proto_index  [2 funcs]
    load_proto_text  CC=2  out:5
    schema_exists  CC=1  out:3
  packages.resource-agent-hypervisor.hypervisor.contract_registry.cross_checks.resources  [1 funcs]
    validate_resource_cross_refs  CC=6  out:4
  packages.resource-agent-hypervisor.hypervisor.contract_registry.cross_validator  [2 funcs]
    validate_cross_references  CC=5  out:3
    validate_root  CC=1  out:2
  packages.resource-agent-hypervisor.hypervisor.contract_registry.registry_checks.capabilities  [3 funcs]
    validate_capabilities  CC=4  out:5
    validate_command_capability  CC=3  out:2
    validate_resource_read_capability  CC=7  out:3
  packages.resource-agent-hypervisor.hypervisor.contract_registry.registry_checks.resources  [2 funcs]
    validate_resources  CC=7  out:9
    validate_views  CC=3  out:2
  packages.resource-agent-hypervisor.hypervisor.contract_registry.validate  [1 funcs]
    validate_registry  CC=1  out:3
  packages.resource-agent-hypervisor.hypervisor.core  [1 funcs]
    from_config  CC=1  out:2
  packages.resource-agent-hypervisor.hypervisor.deployment_registry.docker_runner  [6 funcs]
    apply_docker_deploy  CC=3  out:6
    build_docker_control_plan  CC=2  out:3
    build_docker_deploy_plan  CC=4  out:6
    docker_uri_for_deployment  CC=2  out:2
    stop_docker_deployment  CC=4  out:2
    verify_docker_deployment  CC=9  out:5
  packages.resource-agent-hypervisor.hypervisor.deployment_registry.env  [3 funcs]
    build_deployment_env_map  CC=9  out:15
    default_log_uri  CC=5  out:7
    resolve_deployment_env  CC=1  out:2
  packages.resource-agent-hypervisor.hypervisor.deployment_registry.env_config  [3 funcs]
    load_deployments_uri_config  CC=2  out:3
    load_runtime_uri_config  CC=2  out:3
    repo_config_dir  CC=2  out:2
  packages.resource-agent-hypervisor.hypervisor.deployment_registry.env_merge  [2 funcs]
    materialize_env_values  CC=6  out:8
    merge_runtime_defaults  CC=3  out:4
  packages.resource-agent-hypervisor.hypervisor.deployment_registry.loader  [4 funcs]
    _parse_deployment  CC=3  out:12
    _read_yaml  CC=3  out:4
    default_registry_path  CC=1  out:1
    load_deployment_registry  CC=5  out:8
  packages.resource-agent-hypervisor.hypervisor.deployment_registry.remote_runner  [6 funcs]
    apply_ssh_deploy_plan  CC=7  out:6
    build_ssh_deploy_plan  CC=3  out:10
    build_ssh_run_plan  CC=7  out:13
    generated_agent_dir  CC=1  out:2
    remote_module_for  CC=2  out:2
    verify_remote_deployment  CC=12  out:6
  packages.resource-agent-hypervisor.hypervisor.deployment_registry.runner  [10 funcs]
    _start_process  CC=4  out:6
    agent_logs_uri  CC=5  out:9
    agent_status  CC=6  out:11
    build_run_plan  CC=10  out:18
    local_target_to_module  CC=4  out:3
    local_target_to_relative_path  CC=3  out:6
    resolve_deployment  CC=7  out:9
    restart_agent  CC=1  out:2
    run_agent  CC=9  out:17
    stop_agent  CC=8  out:19
  packages.resource-agent-hypervisor.hypervisor.deployment_registry.runtime_state  [7 funcs]
    clear_runtime_state  CC=2  out:3
    is_process_alive  CC=4  out:1
    load_runtime_state  CC=3  out:5
    runtime_root  CC=2  out:2
    runtime_status  CC=6  out:7
    save_runtime_state  CC=1  out:4
    state_path  CC=1  out:1
  packages.resource-agent-hypervisor.hypervisor.deployment_registry.status  [7 funcs]
    deployment_from_uri_tree  CC=8  out:17
    get_deployment_for_agent  CC=3  out:2
    infer_port  CC=3  out:3
    list_deployments  CC=2  out:2
    registry_summary  CC=4  out:2
    resolve_status  CC=11  out:7
    sync_from_uri_tree  CC=2  out:4
  packages.resource-agent-hypervisor.hypervisor.domain_pack.artifact_generators.agent_contract  [1 funcs]
    generate_agent_contract  CC=2  out:3
  packages.resource-agent-hypervisor.hypervisor.domain_pack.artifact_generators.commands  [1 funcs]
    generate_commands  CC=2  out:6
  packages.resource-agent-hypervisor.hypervisor.domain_pack.artifact_generators.handlers  [1 funcs]
    generate_handlers  CC=3  out:2
  packages.resource-agent-hypervisor.hypervisor.domain_pack.artifact_generators.proto  [1 funcs]
    generate_proto  CC=2  out:2
  packages.resource-agent-hypervisor.hypervisor.domain_pack.artifact_generators.renderers  [1 funcs]
    generate_renderers  CC=3  out:5
  packages.resource-agent-hypervisor.hypervisor.domain_pack.artifact_generators.resources  [1 funcs]
    generate_resources  CC=2  out:5
  packages.resource-agent-hypervisor.hypervisor.domain_pack.artifact_generators.views  [1 funcs]
    generate_views  CC=2  out:1
  packages.resource-agent-hypervisor.hypervisor.domain_pack.generator  [2 funcs]
    generate_domain_pack  CC=1  out:3
    generate_domain_pack_from_tree  CC=2  out:11
  packages.resource-agent-hypervisor.hypervisor.domain_pack.pack_writer  [1 funcs]
    write_domain_pack  CC=3  out:30
  packages.resource-agent-hypervisor.hypervisor.domain_pack.parser  [2 funcs]
    derive_domain_model  CC=1  out:2
    parse_uri_tree  CC=1  out:3
  packages.resource-agent-hypervisor.hypervisor.domain_pack.writer  [1 funcs]
    write_file  CC=1  out:3
  packages.resource-agent-hypervisor.hypervisor.evolution.cli  [1 funcs]
    main  CC=10  out:11
  packages.resource-agent-hypervisor.hypervisor.paths  [2 funcs]
    find_repo_root  CC=6  out:6
    repo_root  CC=1  out:1
  packages.resource-agent-hypervisor.hypervisor.uri.client  [4 funcs]
    graph  CC=1  out:1
    logs  CC=2  out:2
    nl2uri  CC=1  out:1
    schema  CC=1  out:1
  packages.resource-agent-hypervisor.meta_agent.cli_commands  [6 funcs]
    cmd_generate  CC=2  out:5
    cmd_pipeline  CC=3  out:5
    cmd_plan  CC=2  out:5
    cmd_repair  CC=2  out:4
    cmd_validate  CC=3  out:5
    cmd_verify  CC=3  out:4
  packages.resource-agent-hypervisor.meta_agent.orchestrator  [4 funcs]
    asdict_result  CC=1  out:0
    pipeline_from_prompt  CC=1  out:2
    save_proposal_from_prompt  CC=2  out:6
    validate_repair_generate  CC=7  out:16
  packages.uri3.uri3.cli  [10 funcs]
    _list_payload  CC=2  out:3
    _quick_reference  CC=5  out:5
    graph  CC=3  out:5
    list_cmd  CC=4  out:10
    logs  CC=2  out:6
    resolve  CC=2  out:8
    scan  CC=8  out:21
    schema  CC=4  out:9
    validate  CC=1  out:3
    validate_tree  CC=3  out:5
  packages.uri3.uri3.config.cli_shortcuts  [6 funcs]
    _repo_root  CC=5  out:6
    cli_config_path  CC=1  out:1
    cli_examples  CC=3  out:3
    load_cli_config  CC=2  out:3
    resolve_scan_target  CC=4  out:4
    scan_shortcuts  CC=4  out:6
  packages.uri3.uri3.config.docker_stacks  [5 funcs]
    _repo_root  CC=5  out:6
    docker_config_path  CC=1  out:1
    load_docker_config  CC=2  out:3
    resolve_agent_stack  CC=4  out:15
    resolve_stack  CC=5  out:13
  packages.uri3.uri3.config.llm_profile_builder  [4 funcs]
    chosen_profile_name  CC=3  out:2
    normalize_model_name  CC=2  out:2
    parse_llm_query  CC=7  out:6
    resolve_profile_api_key  CC=4  out:4
  packages.uri3.uri3.config.llm_profiles  [4 funcs]
    _repo_root  CC=4  out:5
    llm_config_path  CC=1  out:1
    load_llm_config  CC=2  out:3
    resolve_llm_profile  CC=10  out:32
  packages.uri3.uri3.config.ssh_auth  [7 funcs]
    _password_from_env_file  CC=5  out:4
    _repo_root  CC=5  out:6
    _resolve_password_value  CC=5  out:5
    load_ssh_config  CC=2  out:3
    resolve_ssh_password  CC=12  out:13
    ssh_auth_hint  CC=3  out:2
    ssh_config_path  CC=1  out:1
  packages.uri3.uri3.config.uri_yaml  [3 funcs]
    is_uri  CC=4  out:3
    load_uri_yaml  CC=2  out:5
    resolve_uri_values  CC=13  out:11
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
  packages.uri3.uri3.paths  [2 funcs]
    find_repo_root  CC=6  out:6
    repo_root  CC=1  out:1
  packages.uri3.uri3.protocols.schemes.analyze  [3 funcs]
    _analyze_query  CC=14  out:10
    analyze_uri  CC=2  out:7
    describe_uri  CC=2  out:3
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
  packages.uri3.uri3.resolvers.dispatch  [3 funcs]
    _resolve_docker  CC=1  out:1
    resolve_target  CC=3  out:4
    scheme_from_uri  CC=2  out:2
  packages.uri3.uri3.resolvers.docker_resolver  [6 funcs]
    _bool  CC=3  out:2
    _first  CC=2  out:1
    _int  CC=3  out:2
    parse_docker_uri  CC=12  out:23
    resolve_docker  CC=2  out:4
    resolve_docker_target  CC=1  out:1
  packages.uri3.uri3.resolvers.env_resolver  [7 funcs]
    call  CC=1  out:1
    resolve  CC=1  out:1
    _env_var_name  CC=3  out:3
    _first  CC=2  out:1
    _repo_root  CC=5  out:6
    call_env  CC=8  out:17
    resolve_env  CC=1  out:2
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
  packages.uri3.uri3.resolvers.router  [2 funcs]
    call  CC=8  out:8
    resolve  CC=2  out:3
  packages.uri3.uri3.resolvers.ssh_resolver  [6 funcs]
    _ssh_options  CC=2  out:3
    build_ssh_command  CC=4  out:4
    parse_ssh_uri  CC=8  out:7
    resolve_ssh  CC=1  out:6
    run_ssh  CC=1  out:2
    ssh_transport_option  CC=4  out:7
  packages.uri3.uri3.scanner.docker_scanner  [5 funcs]
    _compose_ps  CC=6  out:8
    _inspect_container  CC=5  out:9
    scan_compose_stack  CC=5  out:4
    scan_container  CC=2  out:2
    scan_docker  CC=4  out:4
  packages.uri3.uri3.scanner.http_scanner  [6 funcs]
    _kind_for_path  CC=5  out:3
    _origin  CC=1  out:3
    _probe  CC=3  out:7
    _status_for  CC=5  out:0
    health_scan_ok  CC=6  out:3
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
  packages.uri3.uri3.cli._quick_reference → packages.uri3.uri3.config.cli_shortcuts.scan_shortcuts
  packages.uri3.uri3.cli._quick_reference → packages.uri3.uri3.config.cli_shortcuts.cli_examples
  packages.uri3.uri3.cli._list_payload → packages.uri3.uri3.config.cli_shortcuts.cli_examples
  packages.uri3.uri3.cli._list_payload → packages.uri3.uri3.protocols.schemes.spec_registry.list_schemes
  packages.uri3.uri3.cli._list_payload → packages.uri3.uri3.config.cli_shortcuts.scan_shortcuts
  packages.uri3.uri3.cli.list_cmd → packages.uri3.uri3.cli._list_payload
  packages.uri3.uri3.cli.list_cmd → packages.uri3.uri3.cli._quick_reference
  packages.uri3.uri3.cli.validate → uri3.validators.uri_validator.validate_uri
  packages.uri3.uri3.cli.validate_tree → packages.uri3.uri3.validators.uri_tree_validator.validate_uri_tree
  packages.uri3.uri3.cli.graph → uri3.graph.uri_graph.build_graph_from_tree
  packages.uri3.uri3.cli.scan → packages.uri3.uri3.config.cli_shortcuts.scan_shortcuts
  packages.uri3.uri3.cli.scan → packages.uri3.uri3.config.cli_shortcuts.resolve_scan_target
  packages.uri3.uri3.cli.logs → packages.uri3.uri3.logs.reader.summarize_logs
  packages.uri3.uri3.cli.logs → packages.uri3.uri3.logs.reader.read_logs_result
  packages.uri3.uri3.cli.schema → packages.uri3.uri3.protocols.schemes.spec_registry.list_schemes
  packages.uri3.uri3.cli.schema → packages.uri3.uri3.protocols.schemes.analyze.analyze_uri
  packages.uri3.uri3.cli.schema → packages.uri3.uri3.protocols.schemes.analyze.describe_uri
  packages.uri3.uri3.paths.repo_root → packages.uri3.uri3.paths.find_repo_root
  packages.uri3.uri3.logs.parsing.parse_log_line → packages.uri3.uri3.logs.parsing.empty_entry
  packages.uri3.uri3.logs.parsing.parse_log_line → packages.uri3.uri3.logs.parsing.parse_json_entry
  packages.uri3.uri3.logs.parsing.parse_log_line → packages.uri3.uri3.logs.parsing.parse_text_entry
  packages.uri3.uri3.logs.filters.matches_level → packages.uri3.uri3.logs.filters.level_rank
  packages.uri3.uri3.logs.filters.matches_time_window → packages.uri3.uri3.logs.filters.entry_timestamp
  packages.uri3.uri3.logs.filters.matches_filters → packages.uri3.uri3.logs.filters.matches_level
  packages.uri3.uri3.logs.filters.matches_filters → packages.uri3.uri3.logs.filters.matches_logger
  packages.uri3.uri3.logs.filters.matches_filters → packages.uri3.uri3.logs.filters.matches_grep
  packages.uri3.uri3.logs.filters.matches_filters → packages.uri3.uri3.logs.filters.matches_time_window
  packages.uri3.uri3.logs.reader.resolve_log_path → packages.uri3.uri3.paths.find_repo_root
  packages.uri3.uri3.logs.reader.read_logs → packages.uri3.uri3.resolvers.log_resolver.parse_log_uri
  packages.uri3.uri3.logs.reader.read_logs → packages.uri3.uri3.logs.reader.resolve_log_path
  packages.uri3.uri3.logs.reader.read_logs → packages.uri3.uri3.logs.reader._parse_since
  packages.uri3.uri3.logs.reader.read_logs → packages.uri3.uri3.logs.parsing.parse_log_line
  packages.uri3.uri3.logs.reader.read_logs → packages.uri3.uri3.logs.filters.matches_filters
  packages.uri3.uri3.logs.reader.read_logs_result → packages.uri3.uri3.logs.reader.summarize_logs
  packages.uri3.uri3.logs.reader.read_logs_result → packages.uri3.uri3.logs.reader.read_logs
  packages.uri3.uri3.logs.reader.summarize_logs → packages.uri3.uri3.resolvers.log_resolver.parse_log_uri
  packages.uri3.uri3.logs.reader.summarize_logs → packages.uri3.uri3.logs.reader.resolve_log_path
  packages.uri3.uri3.logs.reader.summarize_logs → packages.uri3.uri3.logs.reader.read_logs
  packages.uri3.uri3.logs.writer.append_log → packages.uri3.uri3.paths.find_repo_root
  uri3.validators.uri_validator.validate_uri → uri3.protocols.parser.parse_uri
  packages.uri3.uri3.validators.uri_tree_validator.validate_uri_tree → packages.uri3.uri3.validators.uri_tree_validator.load_yaml
  packages.uri3.uri3.docker.controller.control_docker → packages.uri3.uri3.resolvers.docker_resolver.parse_docker_uri
  packages.uri3.uri3.docker.controller.control_docker → packages.uri3.uri3.docker.actions.container.handles_container_action
  packages.uri3.uri3.docker.controller.control_docker → packages.uri3.uri3.docker.compose_generator.write_generated_compose
  packages.uri3.uri3.docker.controller.control_docker → packages.uri3.uri3.docker.actions.container.control_container
  packages.uri3.uri3.docker.controller.control_docker → packages.uri3.uri3.docker.actions.compose.control_compose
  packages.uri3.uri3.docker.compose_generator.build_generate_plan → packages.uri3.uri3.config.docker_stacks.resolve_agent_stack
  packages.uri3.uri3.docker.compose_generator.write_generated_compose → packages.uri3.uri3.docker.compose_generator.build_generate_plan
  packages.uri3.uri3.docker.actions.container.control_container → packages.uri3.uri3.docker.actions.container._container_name
  packages.uri3.uri3.docker.actions.container.control_container → packages.uri3.uri3.docker.runner.run_command
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
# generated in 0.20s
# nodes: 374 | edges: 494 | modules: 114
# CC̄=3.4

HUBS[20]:
  hypervisor.contract_registry.loader.load_contract_registry
    CC=9  in:6  out:33  total:39
  packages.uri3.uri3.config.llm_profiles.resolve_llm_profile
    CC=10  in:2  out:32  total:34
  hypervisor.contract_registry.merger.merge_main_contracts
    CC=12  in:1  out:31  total:32
  packages.resource-agent-hypervisor.hypervisor.domain_pack.pack_writer.write_domain_pack
    CC=3  in:1  out:30  total:31
  meta_agent.planner.infer_intent
    CC=9  in:1  out:30  total:31
  uri3.graph.uri_graph.build_graph_from_tree
    CC=10  in:2  out:28  total:30
  packages.uri3.uri3.resolvers.docker_resolver.parse_docker_uri
    CC=12  in:5  out:23  total:28
  generator.model.load_agent_spec
    CC=7  in:2  out:24  total:26
  hypervisor.contract_registry.cli.main
    CC=20  in:0  out:26  total:26
  packages.uri3.uri3.paths.find_repo_root
    CC=6  in:19  out:6  total:25
  packages.uri3.uri3.logs.reader.summarize_logs
    CC=6  in:6  out:18  total:24
  packages.uri3.uri3.resolvers.log_resolver.parse_log_uri
    CC=7  in:5  out:16  total:21
  packages.resource-agent-hypervisor.hypervisor.deployment_registry.runner.stop_agent
    CC=8  in:2  out:19  total:21
  packages.resource-agent-hypervisor.hypervisor.deployment_registry.runner.build_run_plan
    CC=10  in:3  out:18  total:21
  packages.resource-agent-hypervisor.hypervisor.cli_commands.echo_json
    CC=2  in:16  out:5  total:21
  packages.uri3.uri3.cli.scan
    CC=8  in:0  out:21  total:21
  packages.resource-agent-factory.generator.agent_generator.generate_agent
    CC=5  in:3  out:17  total:20
  packages.uri3.uri3.resolvers.env_resolver.call_env
    CC=8  in:2  out:17  total:19
  packages.resource-agent-hypervisor.hypervisor.deployment_registry.runner.run_agent
    CC=9  in:2  out:17  total:19
  packages.resource-agent-hypervisor.meta_agent.orchestrator.validate_repair_generate
    CC=7  in:3  out:16  total:19

MODULES:
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
  hypervisor.compatibility.checker  [1 funcs]
    classify_registry_change  CC=8  out:11
  hypervisor.config.env  [4 funcs]
    _parse_bool  CC=1  out:1
    apply_env_overrides  CC=1  out:2
    apply_legacy_env_overrides  CC=6  out:4
    apply_structured_env_overrides  CC=9  out:17
  hypervisor.contract_registry.cli  [1 funcs]
    main  CC=20  out:26
  hypervisor.contract_registry.loader  [2 funcs]
    _read_yaml  CC=3  out:4
    load_contract_registry  CC=9  out:33
  hypervisor.contract_registry.merger  [1 funcs]
    merge_main_contracts  CC=12  out:31
  hypervisor.contract_registry.registry_builder  [3 funcs]
    _contract_hash  CC=3  out:13
    build_registry_manifest  CC=5  out:9
    write_registry_manifest  CC=2  out:6
  hypervisor.contract_registry.registry_exporter  [2 funcs]
    export_json  CC=1  out:1
    export_markdown  CC=6  out:13
  hypervisor.contract_registry.schema_validator  [4 funcs]
    _read_json  CC=1  out:2
    _read_yaml  CC=2  out:2
    validate_contract_files  CC=6  out:13
    validate_file  CC=3  out:8
  hypervisor.deployment_registry.writer  [3 funcs]
    save_deployment_registry  CC=2  out:4
    upsert_deployment  CC=3  out:2
    write_deployment_registry  CC=1  out:2
  hypervisor.domain_pack.templates  [2 funcs]
    generic_proto  CC=1  out:1
    package_name  CC=1  out:0
  hypervisor.evolution.models  [1 funcs]
    load_proposal  CC=5  out:11
  hypervisor.evolution.validator  [1 funcs]
    validate_proposal  CC=6  out:6
  hypervisor.uri2llm.pypi_resolver  [1 funcs]
    resolve_pypi  CC=5  out:6
  hypervisor.verifier.capability_tests  [1 funcs]
    build_capability_test_plan  CC=4  out:2
  hypervisor.verifier.cli  [1 funcs]
    main  CC=5  out:8
  meta_agent.api  [6 funcs]
    generate  CC=2  out:6
    pipeline  CC=2  out:4
    proposal_from_prompt  CC=2  out:6
    repair  CC=2  out:5
    validate  CC=2  out:5
    verify  CC=1  out:2
  meta_agent.planner  [4 funcs]
    infer_intent  CC=9  out:30
    intent_to_agent_spec  CC=8  out:11
    package_name  CC=3  out:6
    singularize  CC=4  out:3
  meta_agent.repair.loader  [2 funcs]
    load_spec  CC=2  out:3
    write_spec  CC=1  out:2
  meta_agent.repair.pipeline  [1 funcs]
    repair_agent_spec  CC=2  out:12
  meta_agent.repair.rules  [6 funcs]
    repair_agent_block  CC=6  out:12
    repair_capabilities  CC=6  out:8
    repair_command_capability  CC=4  out:10
    repair_duplicate_capability_names  CC=5  out:5
    repair_missing_capability_type  CC=3  out:4
    repair_resource_read_capability  CC=8  out:14
  nl2a.cli  [1 funcs]
    generate  CC=1  out:5
  nl2uri.writer  [1 funcs]
    write_uri_tree  CC=1  out:4
  packages.nl2uri.nl2uri.cli  [1 funcs]
    generate  CC=5  out:16
  packages.nl2uri.nl2uri.domain_planner  [11 funcs]
    _call_openrouter  CC=4  out:8
    _deterministic_weather_plan  CC=2  out:2
    _extract_json  CC=3  out:8
    _generic_plan  CC=1  out:3
    _is_structured_uri_tree  CC=10  out:13
    _is_weather_prompt  CC=1  out:2
    _llm_uri_from_env  CC=6  out:7
    _normalize_llm_tree  CC=7  out:12
    _slug  CC=2  out:3
    _validate_tree_data  CC=2  out:6
  packages.nl2uri.nl2uri.llm_planner  [1 funcs]
    llm_plan  CC=2  out:4
  packages.nl2uri.nl2uri.pipeline  [4 funcs]
    _append_pipeline_logs  CC=2  out:4
    generate_tree  CC=1  out:1
    run_full_pipeline  CC=3  out:15
    run_generate_pipeline  CC=4  out:13
  packages.nl2uri.nl2uri.planner  [1 funcs]
    rule_based_plan  CC=1  out:2
  packages.resource-agent-factory.generator.agent_generator  [3 funcs]
    expand_paths  CC=4  out:7
    generate_agent  CC=5  out:17
    main  CC=5  out:4
  packages.resource-agent-factory.generator.header  [3 funcs]
    contract_source_ref  CC=3  out:7
    dockerfile_header  CC=1  out:0
    python_file_header  CC=1  out:0
  packages.resource-agent-factory.generator.paths  [2 funcs]
    find_repo_root  CC=6  out:6
    project_root  CC=1  out:1
  packages.resource-agent-hypervisor.hypervisor.cli  [13 funcs]
    agent_status_cmd  CC=1  out:5
    call  CC=1  out:4
    config_cmd  CC=2  out:7
    deploy_agent_cmd  CC=1  out:4
    deployments_list  CC=1  out:4
    docker_cmd  CC=1  out:4
    logs_cmd  CC=1  out:4
    resolve  CC=1  out:4
    restart_agent_cmd  CC=1  out:8
    run_agent_cmd  CC=1  out:8
  packages.resource-agent-hypervisor.hypervisor.cli_commands  [6 funcs]
    call_docker  CC=5  out:6
    deploy_agent  CC=7  out:16
    echo_json  CC=2  out:5
    read_agent_logs  CC=3  out:4
    run_local_agent  CC=6  out:15
    verify_agent  CC=4  out:8
  packages.resource-agent-hypervisor.hypervisor.config.config_checks  [4 funcs]
    validate_hypervisor  CC=7  out:7
    validate_llm  CC=4  out:4
    validate_path_sections  CC=5  out:5
    validate_uri3  CC=4  out:3
  packages.resource-agent-hypervisor.hypervisor.config.defaults  [4 funcs]
    apply_builtin_defaults  CC=1  out:17
    embedded_defaults_raw  CC=1  out:1
    get_default_config  CC=1  out:3
    load_yaml_file  CC=4  out:4
  packages.resource-agent-hypervisor.hypervisor.config.loader  [5 funcs]
    config_search_paths  CC=6  out:11
    get_config  CC=1  out:1
    load_config  CC=3  out:9
    load_hypervisor_config  CC=1  out:2
    resolve_config_path  CC=3  out:2
  packages.resource-agent-hypervisor.hypervisor.config.uri_config  [2 funcs]
    _repo_config_dir  CC=2  out:2
    apply_uri_yaml_configs  CC=10  out:14
  packages.resource-agent-hypervisor.hypervisor.config.validators  [2 funcs]
    merge_config  CC=5  out:5
    validate_config  CC=1  out:4
  packages.resource-agent-hypervisor.hypervisor.contract_registry.cross_checks.capabilities  [1 funcs]
    validate_capability_cross_refs  CC=13  out:6
  packages.resource-agent-hypervisor.hypervisor.contract_registry.cross_checks.proto_index  [2 funcs]
    load_proto_text  CC=2  out:5
    schema_exists  CC=1  out:3
  packages.resource-agent-hypervisor.hypervisor.contract_registry.cross_checks.resources  [1 funcs]
    validate_resource_cross_refs  CC=6  out:4
  packages.resource-agent-hypervisor.hypervisor.contract_registry.cross_validator  [2 funcs]
    validate_cross_references  CC=5  out:3
    validate_root  CC=1  out:2
  packages.resource-agent-hypervisor.hypervisor.contract_registry.registry_checks.capabilities  [3 funcs]
    validate_capabilities  CC=4  out:5
    validate_command_capability  CC=3  out:2
    validate_resource_read_capability  CC=7  out:3
  packages.resource-agent-hypervisor.hypervisor.contract_registry.registry_checks.resources  [2 funcs]
    validate_resources  CC=7  out:9
    validate_views  CC=3  out:2
  packages.resource-agent-hypervisor.hypervisor.contract_registry.validate  [1 funcs]
    validate_registry  CC=1  out:3
  packages.resource-agent-hypervisor.hypervisor.core  [1 funcs]
    from_config  CC=1  out:2
  packages.resource-agent-hypervisor.hypervisor.deployment_registry.docker_runner  [6 funcs]
    apply_docker_deploy  CC=3  out:6
    build_docker_control_plan  CC=2  out:3
    build_docker_deploy_plan  CC=4  out:6
    docker_uri_for_deployment  CC=2  out:2
    stop_docker_deployment  CC=4  out:2
    verify_docker_deployment  CC=9  out:5
  packages.resource-agent-hypervisor.hypervisor.deployment_registry.env  [3 funcs]
    build_deployment_env_map  CC=9  out:15
    default_log_uri  CC=5  out:7
    resolve_deployment_env  CC=1  out:2
  packages.resource-agent-hypervisor.hypervisor.deployment_registry.env_config  [3 funcs]
    load_deployments_uri_config  CC=2  out:3
    load_runtime_uri_config  CC=2  out:3
    repo_config_dir  CC=2  out:2
  packages.resource-agent-hypervisor.hypervisor.deployment_registry.env_merge  [2 funcs]
    materialize_env_values  CC=6  out:8
    merge_runtime_defaults  CC=3  out:4
  packages.resource-agent-hypervisor.hypervisor.deployment_registry.loader  [4 funcs]
    _parse_deployment  CC=3  out:12
    _read_yaml  CC=3  out:4
    default_registry_path  CC=1  out:1
    load_deployment_registry  CC=5  out:8
  packages.resource-agent-hypervisor.hypervisor.deployment_registry.remote_runner  [6 funcs]
    apply_ssh_deploy_plan  CC=7  out:6
    build_ssh_deploy_plan  CC=3  out:10
    build_ssh_run_plan  CC=7  out:13
    generated_agent_dir  CC=1  out:2
    remote_module_for  CC=2  out:2
    verify_remote_deployment  CC=12  out:6
  packages.resource-agent-hypervisor.hypervisor.deployment_registry.runner  [10 funcs]
    _start_process  CC=4  out:6
    agent_logs_uri  CC=5  out:9
    agent_status  CC=6  out:11
    build_run_plan  CC=10  out:18
    local_target_to_module  CC=4  out:3
    local_target_to_relative_path  CC=3  out:6
    resolve_deployment  CC=7  out:9
    restart_agent  CC=1  out:2
    run_agent  CC=9  out:17
    stop_agent  CC=8  out:19
  packages.resource-agent-hypervisor.hypervisor.deployment_registry.runtime_state  [7 funcs]
    clear_runtime_state  CC=2  out:3
    is_process_alive  CC=4  out:1
    load_runtime_state  CC=3  out:5
    runtime_root  CC=2  out:2
    runtime_status  CC=6  out:7
    save_runtime_state  CC=1  out:4
    state_path  CC=1  out:1
  packages.resource-agent-hypervisor.hypervisor.deployment_registry.status  [7 funcs]
    deployment_from_uri_tree  CC=8  out:17
    get_deployment_for_agent  CC=3  out:2
    infer_port  CC=3  out:3
    list_deployments  CC=2  out:2
    registry_summary  CC=4  out:2
    resolve_status  CC=11  out:7
    sync_from_uri_tree  CC=2  out:4
  packages.resource-agent-hypervisor.hypervisor.domain_pack.artifact_generators.agent_contract  [1 funcs]
    generate_agent_contract  CC=2  out:3
  packages.resource-agent-hypervisor.hypervisor.domain_pack.artifact_generators.commands  [1 funcs]
    generate_commands  CC=2  out:6
  packages.resource-agent-hypervisor.hypervisor.domain_pack.artifact_generators.handlers  [1 funcs]
    generate_handlers  CC=3  out:2
  packages.resource-agent-hypervisor.hypervisor.domain_pack.artifact_generators.proto  [1 funcs]
    generate_proto  CC=2  out:2
  packages.resource-agent-hypervisor.hypervisor.domain_pack.artifact_generators.renderers  [1 funcs]
    generate_renderers  CC=3  out:5
  packages.resource-agent-hypervisor.hypervisor.domain_pack.artifact_generators.resources  [1 funcs]
    generate_resources  CC=2  out:5
  packages.resource-agent-hypervisor.hypervisor.domain_pack.artifact_generators.views  [1 funcs]
    generate_views  CC=2  out:1
  packages.resource-agent-hypervisor.hypervisor.domain_pack.generator  [2 funcs]
    generate_domain_pack  CC=1  out:3
    generate_domain_pack_from_tree  CC=2  out:11
  packages.resource-agent-hypervisor.hypervisor.domain_pack.pack_writer  [1 funcs]
    write_domain_pack  CC=3  out:30
  packages.resource-agent-hypervisor.hypervisor.domain_pack.parser  [2 funcs]
    derive_domain_model  CC=1  out:2
    parse_uri_tree  CC=1  out:3
  packages.resource-agent-hypervisor.hypervisor.domain_pack.writer  [1 funcs]
    write_file  CC=1  out:3
  packages.resource-agent-hypervisor.hypervisor.evolution.cli  [1 funcs]
    main  CC=10  out:11
  packages.resource-agent-hypervisor.hypervisor.paths  [2 funcs]
    find_repo_root  CC=6  out:6
    repo_root  CC=1  out:1
  packages.resource-agent-hypervisor.hypervisor.uri.client  [4 funcs]
    graph  CC=1  out:1
    logs  CC=2  out:2
    nl2uri  CC=1  out:1
    schema  CC=1  out:1
  packages.resource-agent-hypervisor.meta_agent.cli_commands  [6 funcs]
    cmd_generate  CC=2  out:5
    cmd_pipeline  CC=3  out:5
    cmd_plan  CC=2  out:5
    cmd_repair  CC=2  out:4
    cmd_validate  CC=3  out:5
    cmd_verify  CC=3  out:4
  packages.resource-agent-hypervisor.meta_agent.orchestrator  [4 funcs]
    asdict_result  CC=1  out:0
    pipeline_from_prompt  CC=1  out:2
    save_proposal_from_prompt  CC=2  out:6
    validate_repair_generate  CC=7  out:16
  packages.uri3.uri3.cli  [10 funcs]
    _list_payload  CC=2  out:3
    _quick_reference  CC=5  out:5
    graph  CC=3  out:5
    list_cmd  CC=4  out:10
    logs  CC=2  out:6
    resolve  CC=2  out:8
    scan  CC=8  out:21
    schema  CC=4  out:9
    validate  CC=1  out:3
    validate_tree  CC=3  out:5
  packages.uri3.uri3.config.cli_shortcuts  [6 funcs]
    _repo_root  CC=5  out:6
    cli_config_path  CC=1  out:1
    cli_examples  CC=3  out:3
    load_cli_config  CC=2  out:3
    resolve_scan_target  CC=4  out:4
    scan_shortcuts  CC=4  out:6
  packages.uri3.uri3.config.docker_stacks  [5 funcs]
    _repo_root  CC=5  out:6
    docker_config_path  CC=1  out:1
    load_docker_config  CC=2  out:3
    resolve_agent_stack  CC=4  out:15
    resolve_stack  CC=5  out:13
  packages.uri3.uri3.config.llm_profile_builder  [4 funcs]
    chosen_profile_name  CC=3  out:2
    normalize_model_name  CC=2  out:2
    parse_llm_query  CC=7  out:6
    resolve_profile_api_key  CC=4  out:4
  packages.uri3.uri3.config.llm_profiles  [4 funcs]
    _repo_root  CC=4  out:5
    llm_config_path  CC=1  out:1
    load_llm_config  CC=2  out:3
    resolve_llm_profile  CC=10  out:32
  packages.uri3.uri3.config.ssh_auth  [7 funcs]
    _password_from_env_file  CC=5  out:4
    _repo_root  CC=5  out:6
    _resolve_password_value  CC=5  out:5
    load_ssh_config  CC=2  out:3
    resolve_ssh_password  CC=12  out:13
    ssh_auth_hint  CC=3  out:2
    ssh_config_path  CC=1  out:1
  packages.uri3.uri3.config.uri_yaml  [3 funcs]
    is_uri  CC=4  out:3
    load_uri_yaml  CC=2  out:5
    resolve_uri_values  CC=13  out:11
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
  packages.uri3.uri3.paths  [2 funcs]
    find_repo_root  CC=6  out:6
    repo_root  CC=1  out:1
  packages.uri3.uri3.protocols.schemes.analyze  [3 funcs]
    _analyze_query  CC=14  out:10
    analyze_uri  CC=2  out:7
    describe_uri  CC=2  out:3
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
  packages.uri3.uri3.resolvers.dispatch  [3 funcs]
    _resolve_docker  CC=1  out:1
    resolve_target  CC=3  out:4
    scheme_from_uri  CC=2  out:2
  packages.uri3.uri3.resolvers.docker_resolver  [6 funcs]
    _bool  CC=3  out:2
    _first  CC=2  out:1
    _int  CC=3  out:2
    parse_docker_uri  CC=12  out:23
    resolve_docker  CC=2  out:4
    resolve_docker_target  CC=1  out:1
  packages.uri3.uri3.resolvers.env_resolver  [7 funcs]
    call  CC=1  out:1
    resolve  CC=1  out:1
    _env_var_name  CC=3  out:3
    _first  CC=2  out:1
    _repo_root  CC=5  out:6
    call_env  CC=8  out:17
    resolve_env  CC=1  out:2
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
  packages.uri3.uri3.resolvers.router  [2 funcs]
    call  CC=8  out:8
    resolve  CC=2  out:3
  packages.uri3.uri3.resolvers.ssh_resolver  [6 funcs]
    _ssh_options  CC=2  out:3
    build_ssh_command  CC=4  out:4
    parse_ssh_uri  CC=8  out:7
    resolve_ssh  CC=1  out:6
    run_ssh  CC=1  out:2
    ssh_transport_option  CC=4  out:7
  packages.uri3.uri3.scanner.docker_scanner  [5 funcs]
    _compose_ps  CC=6  out:8
    _inspect_container  CC=5  out:9
    scan_compose_stack  CC=5  out:4
    scan_container  CC=2  out:2
    scan_docker  CC=4  out:4
  packages.uri3.uri3.scanner.http_scanner  [6 funcs]
    _kind_for_path  CC=5  out:3
    _origin  CC=1  out:3
    _probe  CC=3  out:7
    _status_for  CC=5  out:0
    health_scan_ok  CC=6  out:3
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
  packages.uri3.uri3.cli._quick_reference → packages.uri3.uri3.config.cli_shortcuts.scan_shortcuts
  packages.uri3.uri3.cli._quick_reference → packages.uri3.uri3.config.cli_shortcuts.cli_examples
  packages.uri3.uri3.cli._list_payload → packages.uri3.uri3.config.cli_shortcuts.cli_examples
  packages.uri3.uri3.cli._list_payload → packages.uri3.uri3.protocols.schemes.spec_registry.list_schemes
  packages.uri3.uri3.cli._list_payload → packages.uri3.uri3.config.cli_shortcuts.scan_shortcuts
  packages.uri3.uri3.cli.list_cmd → packages.uri3.uri3.cli._list_payload
  packages.uri3.uri3.cli.list_cmd → packages.uri3.uri3.cli._quick_reference
  packages.uri3.uri3.cli.validate → uri3.validators.uri_validator.validate_uri
  packages.uri3.uri3.cli.validate_tree → packages.uri3.uri3.validators.uri_tree_validator.validate_uri_tree
  packages.uri3.uri3.cli.graph → uri3.graph.uri_graph.build_graph_from_tree
  packages.uri3.uri3.cli.scan → packages.uri3.uri3.config.cli_shortcuts.scan_shortcuts
  packages.uri3.uri3.cli.scan → packages.uri3.uri3.config.cli_shortcuts.resolve_scan_target
  packages.uri3.uri3.cli.logs → packages.uri3.uri3.logs.reader.summarize_logs
  packages.uri3.uri3.cli.logs → packages.uri3.uri3.logs.reader.read_logs_result
  packages.uri3.uri3.cli.schema → packages.uri3.uri3.protocols.schemes.spec_registry.list_schemes
  packages.uri3.uri3.cli.schema → packages.uri3.uri3.protocols.schemes.analyze.analyze_uri
  packages.uri3.uri3.cli.schema → packages.uri3.uri3.protocols.schemes.analyze.describe_uri
  packages.uri3.uri3.paths.repo_root → packages.uri3.uri3.paths.find_repo_root
  packages.uri3.uri3.logs.parsing.parse_log_line → packages.uri3.uri3.logs.parsing.empty_entry
  packages.uri3.uri3.logs.parsing.parse_log_line → packages.uri3.uri3.logs.parsing.parse_json_entry
  packages.uri3.uri3.logs.parsing.parse_log_line → packages.uri3.uri3.logs.parsing.parse_text_entry
  packages.uri3.uri3.logs.filters.matches_level → packages.uri3.uri3.logs.filters.level_rank
  packages.uri3.uri3.logs.filters.matches_time_window → packages.uri3.uri3.logs.filters.entry_timestamp
  packages.uri3.uri3.logs.filters.matches_filters → packages.uri3.uri3.logs.filters.matches_level
  packages.uri3.uri3.logs.filters.matches_filters → packages.uri3.uri3.logs.filters.matches_logger
  packages.uri3.uri3.logs.filters.matches_filters → packages.uri3.uri3.logs.filters.matches_grep
  packages.uri3.uri3.logs.filters.matches_filters → packages.uri3.uri3.logs.filters.matches_time_window
  packages.uri3.uri3.logs.reader.resolve_log_path → packages.uri3.uri3.paths.find_repo_root
  packages.uri3.uri3.logs.reader.read_logs → packages.uri3.uri3.resolvers.log_resolver.parse_log_uri
  packages.uri3.uri3.logs.reader.read_logs → packages.uri3.uri3.logs.reader.resolve_log_path
  packages.uri3.uri3.logs.reader.read_logs → packages.uri3.uri3.logs.reader._parse_since
  packages.uri3.uri3.logs.reader.read_logs → packages.uri3.uri3.logs.parsing.parse_log_line
  packages.uri3.uri3.logs.reader.read_logs → packages.uri3.uri3.logs.filters.matches_filters
  packages.uri3.uri3.logs.reader.read_logs_result → packages.uri3.uri3.logs.reader.summarize_logs
  packages.uri3.uri3.logs.reader.read_logs_result → packages.uri3.uri3.logs.reader.read_logs
  packages.uri3.uri3.logs.reader.summarize_logs → packages.uri3.uri3.resolvers.log_resolver.parse_log_uri
  packages.uri3.uri3.logs.reader.summarize_logs → packages.uri3.uri3.logs.reader.resolve_log_path
  packages.uri3.uri3.logs.reader.summarize_logs → packages.uri3.uri3.logs.reader.read_logs
  packages.uri3.uri3.logs.writer.append_log → packages.uri3.uri3.paths.find_repo_root
  uri3.validators.uri_validator.validate_uri → uri3.protocols.parser.parse_uri
  packages.uri3.uri3.validators.uri_tree_validator.validate_uri_tree → packages.uri3.uri3.validators.uri_tree_validator.load_yaml
  packages.uri3.uri3.docker.controller.control_docker → packages.uri3.uri3.resolvers.docker_resolver.parse_docker_uri
  packages.uri3.uri3.docker.controller.control_docker → packages.uri3.uri3.docker.actions.container.handles_container_action
  packages.uri3.uri3.docker.controller.control_docker → packages.uri3.uri3.docker.compose_generator.write_generated_compose
  packages.uri3.uri3.docker.controller.control_docker → packages.uri3.uri3.docker.actions.container.control_container
  packages.uri3.uri3.docker.controller.control_docker → packages.uri3.uri3.docker.actions.compose.control_compose
  packages.uri3.uri3.docker.compose_generator.build_generate_plan → packages.uri3.uri3.config.docker_stacks.resolve_agent_stack
  packages.uri3.uri3.docker.compose_generator.write_generated_compose → packages.uri3.uri3.docker.compose_generator.build_generate_plan
  packages.uri3.uri3.docker.actions.container.control_container → packages.uri3.uri3.docker.actions.container._container_name
  packages.uri3.uri3.docker.actions.container.control_container → packages.uri3.uri3.docker.runner.run_command
```

### Code Analysis (`project/analysis.toon.yaml`)

```toon markpact:analysis path=project/analysis.toon.yaml
# code2llm | 235f 10275L | python:169,yaml:35,json:10,toml:5,yml:3,shell:3,txt:2,proto:2,j2:1 | 2026-06-14
# generated in 0.04s
# CC̅=3.4 | critical:1/457 | dups:0 | cycles:4

HEALTH[1]:
  🟡 CC    main CC=20 (limit:15)

REFACTOR[2]:
  1. split 1 high-CC methods  (CC>15)
  2. break 4 circular dependencies

PIPELINES[131]:
  [1] Src [main]: main
      PURITY: 100% pure
  [2] Src [list_cmd]: list_cmd → _list_payload → cli_examples → load_cli_config → ...(2 more)
      PURITY: 100% pure
  [3] Src [validate]: validate → validate_uri → parse_uri
      PURITY: 100% pure
  [4] Src [validate_tree]: validate_tree → validate_uri_tree → load_yaml
      PURITY: 100% pure
  [5] Src [graph]: graph → build_graph_from_tree
      PURITY: 100% pure
  [6] Src [call]: call
      PURITY: 100% pure
  [7] Src [scan]: scan → scan_shortcuts → load_cli_config → cli_config_path → ...(1 more)
      PURITY: 100% pure
  [8] Src [logs]: logs → summarize_logs → parse_log_uri → parse_query → ...(1 more)
      PURITY: 100% pure
  [9] Src [schema]: schema → list_schemes
      PURITY: 100% pure
  [10] Src [add_node]: add_node
      PURITY: 100% pure
  [11] Src [add_edge]: add_edge
      PURITY: 100% pure
  [12] Src [scan]: scan → parse_uri
      PURITY: 100% pure
  [13] Src [normalize_uri]: normalize_uri → parse_uri
      PURITY: 100% pure
  [14] Src [spec]: spec
      PURITY: 100% pure
  [15] Src [spec]: spec
      PURITY: 100% pure
  [16] Src [to_dict]: to_dict
      PURITY: 100% pure
  [17] Src [to_dict]: to_dict
      PURITY: 100% pure
  [18] Src [spec]: spec
      PURITY: 100% pure
  [19] Src [spec]: spec
      PURITY: 100% pure
  [20] Src [spec]: spec
      PURITY: 100% pure
  [21] Src [spec]: spec
      PURITY: 100% pure
  [22] Src [spec]: spec
      PURITY: 100% pure
  [23] Src [spec]: spec
      PURITY: 100% pure
  [24] Src [resource_like_spec]: resource_like_spec
      PURITY: 100% pure
  [25] Src [spec]: spec
      PURITY: 100% pure
  [26] Src [resolve]: resolve → resolve_http_like
      PURITY: 100% pure
  [27] Src [fetch]: fetch
      PURITY: 100% pure
  [28] Src [resolve_docker_target]: resolve_docker_target → parse_docker_uri → _first
      PURITY: 100% pure
  [29] Src [resolve]: resolve → resolve_llm
      PURITY: 100% pure
  [30] Src [resolve]: resolve → resolve_env → _env_var_name
      PURITY: 100% pure
  [31] Src [call]: call → call_env → _env_var_name
      PURITY: 100% pure
  [32] Src [resolve]: resolve → resolve_python → _split_python_uri
      PURITY: 100% pure
  [33] Src [call]: call → call_python → _split_python_uri
      PURITY: 100% pure
  [34] Src [to_dict]: to_dict
      PURITY: 100% pure
  [35] Src [resolve]: resolve → resolve_log → parse_log_uri → parse_query → ...(1 more)
      PURITY: 100% pure
  [36] Src [read]: read → read_logs → parse_log_uri → parse_query → ...(1 more)
      PURITY: 100% pure
  [37] Src [main]: main → iter_agent_specs
      PURITY: 100% pure
  [38] Src [main]: main → expand_paths
      PURITY: 100% pure
  [39] Src [main]: main → verify_generated → verify_generated_agent → file_sha256
      PURITY: 100% pure
  [40] Src [generate]: generate → plan_from_prompt → _is_weather_prompt
      PURITY: 100% pure
  [41] Src [main]: main
      PURITY: 100% pure
  [42] Src [llm_plan]: llm_plan → plan_from_prompt → _is_weather_prompt
      PURITY: 100% pure
  [43] Src [generate]: generate → run_full_pipeline → run_generate_pipeline → generate_tree → ...(2 more)
      PURITY: 100% pure
  [44] Src [main]: main
      PURITY: 100% pure
  [45] Src [health]: health
      PURITY: 100% pure
  [46] Src [proposal_from_prompt]: proposal_from_prompt → save_proposal_from_prompt → infer_intent → singularize
      PURITY: 100% pure
  [47] Src [validate]: validate → validate_agent → load_agent_spec
      PURITY: 100% pure
  [48] Src [repair]: repair → repair_agent_spec → validate_agent → load_agent_spec
      PURITY: 100% pure
  [49] Src [generate]: generate → asdict_result
      PURITY: 100% pure
  [50] Src [pipeline]: pipeline → pipeline_from_prompt → save_proposal_from_prompt → infer_intent → ...(1 more)
      PURITY: 100% pure

LAYERS:
  generator/                      CC̄=6.0    ←in:14  →out:0
  │ validate                     0L  0C    3m  CC=11     ←5
  │ hashutil                     0L  0C    1m  CC=1      ←2
  │ verify                       0L  0C    3m  CC=9      ←4
  │ model                        0L  2C    2m  CC=7      ←2
  │ __init__                     0L  0C    0m  CC=0.0    ←0
  │ Dockerfile.j2                0L  0C    0m  CC=0.0    ←0
  │
  hypervisor/                     CC̄=3.7    ←in:0  →out:0
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
  │ !! cli                          0L  0C    1m  CC=20     ←0
  │ registry_exporter            0L  0C    2m  CC=6      ←1
  │ schema_validator             0L  1C    4m  CC=6      ←1
  │ merger                       0L  0C    1m  CC=12     ←1
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
  packages/                       CC̄=3.3    ←in:0  →out:0
  │ runner                     286L  0C   10m  CC=10     ←2
  │ domain_planner             236L  0C   11m  CC=10     ←4
  │ cli                        203L  0C   12m  CC=8      ←1
  │ remote_runner              186L  0C    6m  CC=12     ←2
  │ docker_resolver            160L  1C    8m  CC=12     ←5
  │ status                     151L  0C   10m  CC=11     ←4
  │ cli                        148L  0C   15m  CC=4      ←0
  │ pipeline                   141L  2C    4m  CC=4      ←1
  │ cli_commands               128L  0C    6m  CC=7      ←1
  │ instance_parser            119L  0C   13m  CC=4      ←2
  │ ssh_resolver               107L  0C    6m  CC=8      ←4
  │ agent_generator            106L  0C    4m  CC=5      ←2
  │ reader                     104L  0C    5m  CC=9      ←5
  │ env_resolver               103L  1C    8m  CC=8      ←3
  │ ssh_auth                   100L  0C    8m  CC=12     ←2
  │ compose                     99L  0C    8m  CC=9      ←1
  │ loader                      96L  0C    5m  CC=6      ←2
  │ spec_registry               94L  0C    5m  CC=5      ←2
  │ llm_profiles                92L  1C    5m  CC=10     ←1
  │ docker_scanner              91L  0C    5m  CC=6      ←2
  │ ssh_scanner                 90L  0C    6m  CC=8      ←2
  │ log_resolver                85L  2C    5m  CC=7      ←3
  │ core                        84L  1C    7m  CC=3      ←0
  │ uri_yaml                    79L  0C    3m  CC=13     ←7
  │ pack_writer                 79L  0C    1m  CC=3      ←1
  │ router                      78L  2C    5m  CC=8      ←0
  │ http_scanner                76L  0C    6m  CC=7      ←3
  │ log                         76L  0C    1m  CC=3      ←0
  │ docker_runner               76L  0C    6m  CC=9      ←2
  │ generator                   75L  0C    2m  CC=2      ←1
  │ parsing                     73L  0C    4m  CC=14     ←1
  │ filters                     73L  0C    7m  CC=7      ←1
  │ analyze                     73L  0C    3m  CC=14     ←2
  │ orchestrator                72L  0C    4m  CC=7      ←2
  │ cli_commands                69L  0C    6m  CC=3      ←1
  │ base                        67L  2C    2m  CC=4      ←0
  │ docker_stacks               66L  0C    5m  CC=5      ←2
  │ runtime_state               65L  0C    8m  CC=6      ←1
  │ defaults                    63L  0C    4m  CC=4      ←1
  │ __init__                    59L  0C    0m  CC=0.0    ←0
  │ log_query                   55L  0C    6m  CC=8      ←1
  │ header                      51L  0C    5m  CC=3      ←1
  │ dispatch                    51L  0C    3m  CC=3      ←1
  │ cli                         51L  0C    1m  CC=7      ←0
  │ cli_shortcuts               50L  0C    6m  CC=5      ←1
  │ models                      50L  2C    3m  CC=5      ←0
  │ config_checks               50L  0C    4m  CC=7      ←1
  │ env                         50L  0C    3m  CC=9      ←2
  │ nlp2uri.yaml                50L  0C    0m  CC=0.0    ←0
  │ agent_contract              48L  0C    1m  CC=2      ←1
  │ compose_generator           46L  0C    2m  CC=2      ←2
  │ loader                      44L  0C    4m  CC=5      ←3
  │ llm_profile_builder         44L  0C    4m  CC=7      ←1
  │ docker                      43L  0C    1m  CC=1      ←0
  │ scanner                     42L  0C    2m  CC=5      ←0
  │ cli                         42L  0C    2m  CC=5      ←0
  │ uri_config                  40L  0C    2m  CC=10     ←1
  │ capabilities                40L  0C    3m  CC=7      ←1
  │ client                      38L  1C    8m  CC=2      ←0
  │ container                   37L  0C    3m  CC=8      ←1
  │ controller                  36L  0C    1m  CC=11     ←2
  │ cross_validator             36L  0C    2m  CC=5      ←1
  │ writer                      34L  0C    1m  CC=3      ←2
  │ cli                         33L  0C    1m  CC=10     ←0
  │ validators                  33L  0C    2m  CC=5      ←1
  │ pyproject.toml              33L  0C    0m  CC=0.0    ←0
  │ capabilities                32L  0C    1m  CC=13     ←1
  │ env_merge                   31L  0C    2m  CC=6      ←1
  │ pyproject.toml              31L  0C    0m  CC=0.0    ←0
  │ env_config                  28L  0C    3m  CC=2      ←1
  │ protocol_resolver           27L  0C    4m  CC=4      ←3
  │ pyproject.toml              27L  0C    0m  CC=0.0    ←0
  │ registry                    27L  0C    0m  CC=0.0    ←0
  │ resources                   26L  0C    2m  CC=7      ←1
  │ model                       25L  1C    1m  CC=1      ←0
  │ pyproject.toml              25L  0C    0m  CC=0.0    ←0
  │ resources                   24L  0C    1m  CC=2      ←1
  │ scheme_registry             24L  0C    0m  CC=0.0    ←0
  │ runner                      23L  0C    1m  CC=4      ←2
  │ env                         22L  0C    1m  CC=1      ←0
  │ resources                   22L  0C    1m  CC=6      ←1
  │ constants                   22L  0C    0m  CC=0.0    ←0
  │ uri_tree_validator          20L  0C    2m  CC=2      ←3
  │ python                      18L  0C    1m  CC=1      ←0
  │ paths                       18L  0C    2m  CC=6      ←0
  │ commands                    18L  0C    1m  CC=2      ←1
  │ paths                       17L  0C    2m  CC=6      ←12
  │ paths                       17L  0C    2m  CC=6      ←1
  │ parser                      17L  0C    2m  CC=1      ←1
  │ llm                         16L  0C    1m  CC=1      ←0
  │ resource_like               16L  0C    1m  CC=1      ←0
  │ views                       16L  0C    1m  CC=2      ←1
  │ proto_index                 16L  0C    2m  CC=2      ←3
  │ mcp                         15L  0C    1m  CC=1      ←0
  │ http                        15L  0C    1m  CC=1      ←0
  │ pypi                        15L  0C    1m  CC=1      ←0
  │ a2a                         15L  0C    1m  CC=1      ←0
  │ renderers                   14L  0C    1m  CC=3      ←1
  │ planner                     13L  1C    1m  CC=1      ←1
  │ validate                    13L  0C    1m  CC=1      ←2
  │ __init__                    12L  0C    0m  CC=0.0    ←0
  │ writer                      11L  0C    1m  CC=1      ←2
  │ handlers                    10L  0C    1m  CC=3      ←1
  │ __init__                     9L  0C    0m  CC=0.0    ←0
  │ llm_planner                  8L  0C    1m  CC=2      ←0
  │ proto                        8L  0C    1m  CC=2      ←1
  │ __init__                     4L  0C    0m  CC=0.0    ←0
  │ __init__                     4L  0C    0m  CC=0.0    ←0
  │ __init__                     4L  0C    0m  CC=0.0    ←0
  │ __init__                     3L  0C    0m  CC=0.0    ←0
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
  │ uri_validator                0L  0C    1m  CC=2      ←1
  │ normalizer                   0L  0C    1m  CC=3      ←0
  │ parser                       0L  1C    1m  CC=2      ←4
  │ http_resolver                0L  1C    2m  CC=2      ←0
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
  runtime_client/                 CC̄=1.7    ←in:0  →out:0
  │ client                       0L  1C    3m  CC=2      ←0
  │
  nl2uri/                         CC̄=1.0    ←in:2  →out:0
  │ writer                       0L  0C    1m  CC=1      ←2
  │
  nl2a/                           CC̄=1.0    ←in:0  →out:1
  │ cli                          0L  0C    2m  CC=1      ←0
  │
  ./                              CC̄=0.0    ←in:0  →out:0
  │ !! planfile.yaml             1319L  0C    0m  CC=0.0    ←0
  │ !! goal.yaml                  511L  0C    0m  CC=0.0    ←0
  │ tree.txt                   240L  0C    0m  CC=0.0    ←0
  │ pyproject.toml             126L  0C    0m  CC=0.0    ←0
  │ prefact.yaml                97L  0C    0m  CC=0.0    ←0
  │ Makefile                    72L  0C    0m  CC=0.0    ←0
  │ project.sh                  59L  0C    0m  CC=0.0    ←0
  │ docker-compose.yml          18L  0C    0m  CC=0.0    ←0
  │ Dockerfile                  13L  0C    0m  CC=0.0    ←0
  │ nlp2uri.yaml                 8L  0C    0m  CC=0.0    ←0
  │
  schemas/                        CC̄=0.0    ←in:0  →out:0
  │ contract_registry.schema.json   129L  0C    0m  CC=0.0    ←0
  │ agent_contract.schema.json    79L  0C    0m  CC=0.0    ←0
  │ uri_tree.schema.json        78L  0C    0m  CC=0.0    ←0
  │ resources.schema.json       56L  0C    0m  CC=0.0    ←0
  │ views.schema.json           54L  0C    0m  CC=0.0    ←0
  │ evolution_proposal.schema.json    48L  0C    0m  CC=0.0    ←0
  │ command_contract.schema.json    43L  0C    0m  CC=0.0    ←0
  │ renderer_contract.schema.json    35L  0C    0m  CC=0.0    ←0
  │ domain_pack.schema.json     20L  0C    0m  CC=0.0    ←0
  │
  examples/                       CC̄=0.0    ←in:0  →out:0
  │ docker-compose.yml          10L  0C    0m  CC=0.0    ←0
  │ run.sh                       7L  0C    0m  CC=0.0    ←0
  │ create_orders_agent.yaml     0L  0C    0m  CC=0.0    ←0
  │ broken_agent.yaml            0L  0C    0m  CC=0.0    ←0
  │ create_invoices_agent_prompt.txt     0L  0C    0m  CC=0.0    ←0
  │
  evolution/                      CC̄=0.0    ←in:0  →out:0
  │ add_invoices_agent.yaml      0L  0C    0m  CC=0.0    ←0
  │ add_orders_agent.yaml        0L  0C    0m  CC=0.0    ←0
  │
  deployments/                    CC̄=0.0    ←in:0  →out:0
  │ agent_deployments.yaml      29L  0C    0m  CC=0.0    ←0
  │
  output/                         CC̄=0.0    ←in:0  →out:0
  │ contract_registry.resolved.json   174L  0C    0m  CC=0.0    ←0
  │
  testql-scenarios/               CC̄=0.0    ←in:0  →out:0
  │ generated-api-smoke.testql.toon.yaml    35L  0C    0m  CC=0.0    ←0
  │ generated-cli-tests.testql.toon.yaml    20L  0C    0m  CC=0.0    ←0
  │ generated-from-pytests.testql.toon.yaml    14L  0C    0m  CC=0.0    ←0
  │
  config/                         CC̄=0.0    ←in:0  →out:0
  │ llm.uri.yaml                43L  0C    0m  CC=0.0    ←0
  │ docker.uri.yaml             25L  0C    0m  CC=0.0    ←0
  │ deployments.uri.yaml        18L  0C    0m  CC=0.0    ←0
  │ uri3.uri.yaml               17L  0C    0m  CC=0.0    ←0
  │ ssh.uri.yaml                15L  0C    0m  CC=0.0    ←0
  │ runtime.uri.yaml            12L  0C    0m  CC=0.0    ←0
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
  ── zero ──
     evolution/proposals/add_invoices_agent.yaml  0L
     evolution/proposals/add_orders_agent.yaml  0L
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
     hypervisor/contract_registry/cli.py       0L
     hypervisor/contract_registry/loader.py    0L
     hypervisor/contract_registry/merger.py    0L
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
                                      packages.resource-agent-hypervisor                       packages.uri3                     packages.nl2uri                           generator        hypervisor.contract_registry                          meta_agent                   meta_agent.repair     packages.resource-agent-factory                      uri3.resolvers      hypervisor.deployment_registry                      uri3.protocols            hypervisor.compatibility                hypervisor.evolution                 hypervisor.verifier                              nl2uri
  packages.resource-agent-hypervisor                                  ──                                  46                                   1                                   4                                   2                                   3                                   2                                   1                                                                       2                                                                                                           2                                  ←1                                      hub
                       packages.uri3                                 ←46                                  ──                                  ←8                                                                      ←1                                                                                                                                               4                                                                       1                                                                                                                                                  hub
                     packages.nl2uri                                   2                                   8                                  ──                                   1                                   1                                                                                                           1                                                                                                                                                                                                                                                           2  !! fan-out
                           generator                                  ←4                                                                      ←1                                  ──                                                                      ←2                                  ←3                                  ←4                                                                                                                                                                                                                                                              hub
        hypervisor.contract_registry                                   6                                   1                                  ←1                                                                      ──                                                                                                                                                                                                                                                          ←2                                                                      ←1                                      hub
                          meta_agent                                   5                                                                                                           2                                                                      ──                                   1                                                                                                                                                                                                                                                                                                  !! fan-out
                   meta_agent.repair                                  ←2                                                                                                           3                                                                       1                                  ──                                                                                                                                                                                                                                                                                                
     packages.resource-agent-factory                                  ←1                                                                      ←1                                   4                                                                                                                                              ──                                                                                                                                                                                                                                                            
                      uri3.resolvers                                                                       1                                                                                                                                                                                                                                                          ──                                                                       1                                                                                                                                                
      hypervisor.deployment_registry                                   1                                                                                                                                                                                                                                                                                                                                  ──                                                                                                                                                                                    
                      uri3.protocols                                                                      ←1                                                                                                                                                                                                                                                          ←1                                                                      ──                                                                                                                                                
            hypervisor.compatibility                                                                                                                                                                                   2                                                                                                                                                                                                                                                          ──                                                                                                            
                hypervisor.evolution                                  ←2                                                                                                                                                                                                                                                                                                                                                                                                                                              ──                                                                        
                 hypervisor.verifier                                   1                                                                                                                                               1                                                                                                                                                                                                                                                                                                                                  ──                                    
                              nl2uri                                                                                                          ←2                                                                                                                                                                                                                                                                                                                                                                                                                                              ──
  CYCLES: 4
  HUB: packages.uri3/ (fan-in=56)
  HUB: packages.resource-agent-hypervisor/ (fan-in=15)
  HUB: generator/ (fan-in=14)
  HUB: hypervisor.contract_registry/ (fan-in=6)
  SMELL: packages.nl2uri/ fan-out=15 → split needed
  SMELL: packages.uri3/ fan-out=8 → split needed
  SMELL: packages.resource-agent-hypervisor/ fan-out=65 → split needed
  SMELL: meta_agent/ fan-out=8 → split needed

EXTERNAL:
  validation: run `vallm batch .` → validation.toon
  duplication: run `redup scan .` → duplication.toon
```

### Duplication (`project/duplication.toon.yaml`)

```toon markpact:analysis path=project/duplication.toon.yaml
# redup/duplication | 10 groups | 178f 7657L | 2026-06-14

SUMMARY:
  files_scanned: 178
  total_lines:   7657
  dup_groups:    10
  dup_fragments: 32
  saved_lines:   197
  scan_ms:       2399

HOTSPOTS[7] (files with most duplication):
  packages/resource-agent-hypervisor/hypervisor/domain_pack/templates.py  dup=76L  groups=1  frags=3  (1.0%)
  packages/uri3/uri3/protocols/schemes/instance_parser.py  dup=40L  groups=1  frags=10  (0.5%)
  packages/resource-agent-factory/generator/header.py  dup=18L  groups=1  frags=3  (0.2%)
  packages/uri3/uri3/protocols/schemes/a2a.py  dup=12L  groups=1  frags=1  (0.2%)
  packages/uri3/uri3/protocols/schemes/mcp.py  dup=12L  groups=1  frags=1  (0.2%)
  packages/resource-agent-hypervisor/hypervisor/cli.py  dup=12L  groups=1  frags=2  (0.2%)
  packages/uri3/uri3/resolvers/docker_resolver.py  dup=10L  groups=2  frags=2  (0.1%)

DUPLICATES[10] (ranked by impact):
  [49d1d03e6ce392a1] ! STRU  weather_proto  L=43 N=3 saved=86 sim=1.00
      packages/resource-agent-hypervisor/hypervisor/domain_pack/templates.py:36-78  (weather_proto)
      packages/resource-agent-hypervisor/hypervisor/domain_pack/templates.py:81-106  (weather_handler)
      packages/resource-agent-hypervisor/hypervisor/domain_pack/templates.py:109-115  (generic_handler)
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
  [41a517b24660e0a8]   EXAC  find_repo_root  L=8 N=3 saved=16 sim=1.00
      packages/resource-agent-factory/generator/paths.py:6-13  (find_repo_root)
      packages/resource-agent-hypervisor/hypervisor/paths.py:6-14  (find_repo_root)
      packages/uri3/uri3/paths.py:6-13  (find_repo_root)
  [befef45cfb21329b]   STRU  _repo_root  L=8 N=3 saved=16 sim=1.00
      packages/uri3/uri3/config/cli_shortcuts.py:9-16  (_repo_root)
      packages/uri3/uri3/config/docker_stacks.py:9-16  (_repo_root)
      packages/uri3/uri3/config/ssh_auth.py:10-17  (_repo_root)
  [277a3a34943f29ee]   STRU  python_file_header  L=6 N=3 saved=12 sim=1.00
      packages/resource-agent-factory/generator/header.py:21-26  (python_file_header)
      packages/resource-agent-factory/generator/header.py:29-34  (dockerfile_header)
      packages/resource-agent-factory/generator/header.py:37-42  (markdown_generated_banner)
  [71dc3d2f70a63bf5]   STRU  spec  L=12 N=2 saved=12 sim=1.00
      packages/uri3/uri3/protocols/schemes/a2a.py:4-15  (spec)
      packages/uri3/uri3/protocols/schemes/mcp.py:4-15  (spec)
  [fdc7786ef049b370]   STRU  deploy_agent_cmd  L=6 N=2 saved=6 sim=1.00
      packages/resource-agent-hypervisor/hypervisor/cli.py:111-116  (deploy_agent_cmd)
      packages/resource-agent-hypervisor/hypervisor/cli.py:129-134  (docker_cmd)
  [9a928c6cb43e19ba]   STRU  _first  L=5 N=2 saved=5 sim=1.00
      packages/uri3/uri3/resolvers/docker_resolver.py:59-63  (_first)
      packages/uri3/uri3/resolvers/log_query.py:7-11  (first)
  [06621f22a60e830d]   STRU  _bool  L=5 N=2 saved=5 sim=1.00
      packages/uri3/uri3/resolvers/docker_resolver.py:66-70  (_bool)
      packages/uri3/uri3/resolvers/log_query.py:24-28  (query_bool)
  [bc6d855bfb035b8b]   STRU  resolve_a2a  L=3 N=2 saved=3 sim=1.00
      packages/uri3/uri3/resolvers/protocol_resolver.py:10-12  (resolve_a2a)
      packages/uri3/uri3/resolvers/protocol_resolver.py:15-17  (resolve_mcp)

REFACTOR[10] (ranked by priority):
  [1] ○ extract_function   → packages/resource-agent-hypervisor/hypervisor/domain_pack/utils/weather_proto.py
      WHY: 3 occurrences of 43-line block across 1 files — saves 86 lines
      FILES: packages/resource-agent-hypervisor/hypervisor/domain_pack/templates.py
  [2] ○ extract_function   → packages/uri3/uri3/protocols/schemes/utils/_parse_env.py
      WHY: 10 occurrences of 4-line block across 1 files — saves 36 lines
      FILES: packages/uri3/uri3/protocols/schemes/instance_parser.py
  [3] ○ extract_function   → packages/utils/find_repo_root.py
      WHY: 3 occurrences of 8-line block across 3 files — saves 16 lines
      FILES: packages/resource-agent-factory/generator/paths.py, packages/resource-agent-hypervisor/hypervisor/paths.py, packages/uri3/uri3/paths.py
  [4] ○ extract_function   → packages/uri3/uri3/config/utils/_repo_root.py
      WHY: 3 occurrences of 8-line block across 3 files — saves 16 lines
      FILES: packages/uri3/uri3/config/cli_shortcuts.py, packages/uri3/uri3/config/docker_stacks.py, packages/uri3/uri3/config/ssh_auth.py
  [5] ○ extract_function   → packages/resource-agent-factory/generator/utils/python_file_header.py
      WHY: 3 occurrences of 6-line block across 1 files — saves 12 lines
      FILES: packages/resource-agent-factory/generator/header.py
  [6] ○ extract_function   → packages/uri3/uri3/protocols/schemes/utils/spec.py
      WHY: 2 occurrences of 12-line block across 2 files — saves 12 lines
      FILES: packages/uri3/uri3/protocols/schemes/a2a.py, packages/uri3/uri3/protocols/schemes/mcp.py
  [7] ○ extract_function   → packages/resource-agent-hypervisor/hypervisor/utils/deploy_agent_cmd.py
      WHY: 2 occurrences of 6-line block across 1 files — saves 6 lines
      FILES: packages/resource-agent-hypervisor/hypervisor/cli.py
  [8] ○ extract_function   → packages/uri3/uri3/resolvers/utils/_first.py
      WHY: 2 occurrences of 5-line block across 2 files — saves 5 lines
      FILES: packages/uri3/uri3/resolvers/docker_resolver.py, packages/uri3/uri3/resolvers/log_query.py
  [9] ○ extract_function   → packages/uri3/uri3/resolvers/utils/_bool.py
      WHY: 2 occurrences of 5-line block across 2 files — saves 5 lines
      FILES: packages/uri3/uri3/resolvers/docker_resolver.py, packages/uri3/uri3/resolvers/log_query.py
  [10] ○ extract_function   → packages/uri3/uri3/resolvers/utils/resolve_a2a.py
      WHY: 2 occurrences of 3-line block across 1 files — saves 3 lines
      FILES: packages/uri3/uri3/resolvers/protocol_resolver.py

QUICK_WINS[7] (low risk, high savings — do first):
  [1] extract_function   saved=86L  → packages/resource-agent-hypervisor/hypervisor/domain_pack/utils/weather_proto.py
      FILES: templates.py
  [2] extract_function   saved=36L  → packages/uri3/uri3/protocols/schemes/utils/_parse_env.py
      FILES: instance_parser.py
  [3] extract_function   saved=16L  → packages/utils/find_repo_root.py
      FILES: paths.py, paths.py, paths.py
  [4] extract_function   saved=16L  → packages/uri3/uri3/config/utils/_repo_root.py
      FILES: cli_shortcuts.py, docker_stacks.py, ssh_auth.py
  [5] extract_function   saved=12L  → packages/resource-agent-factory/generator/utils/python_file_header.py
      FILES: header.py
  [6] extract_function   saved=12L  → packages/uri3/uri3/protocols/schemes/utils/spec.py
      FILES: a2a.py, mcp.py
  [7] extract_function   saved=6L  → packages/resource-agent-hypervisor/hypervisor/utils/deploy_agent_cmd.py
      FILES: cli.py

EFFORT_ESTIMATE (total ≈ 8.0h):
  hard   weather_proto                       saved=86L  ~258min
  medium _parse_env                          saved=36L  ~72min
  medium find_repo_root                      saved=16L  ~32min
  medium _repo_root                          saved=16L  ~32min
  easy   python_file_header                  saved=12L  ~24min
  easy   spec                                saved=12L  ~24min
  easy   deploy_agent_cmd                    saved=6L  ~12min
  easy   _first                              saved=5L  ~10min
  easy   _bool                               saved=5L  ~10min
  easy   resolve_a2a                         saved=3L  ~6min

METRICS-TARGET:
  dup_groups:  10 → 0
  saved_lines: 197 lines recoverable
```

### Evolution / Churn (`project/evolution.toon.yaml`)

```toon markpact:analysis path=project/evolution.toon.yaml
# code2llm/evolution | 457 func | 135f | 2026-06-14
# generated in 0.00s

NEXT[3] (ranked by impact):
  [1] !  SPLIT-FUNC      main  CC=20  fan=11
      WHY: CC=20 exceeds 15
      EFFORT: ~1h  IMPACT: 220

  [2] !! SPLIT           planfile.yaml
      WHY: 1319L, 0 classes, max CC=0
      EFFORT: ~4h  IMPACT: 0

  [3] !! SPLIT           goal.yaml
      WHY: 511L, 0 classes, max CC=0
      EFFORT: ~4h  IMPACT: 0


RISKS[2]:
  ⚠ Splitting planfile.yaml may break 0 import paths
  ⚠ Splitting goal.yaml may break 0 import paths

METRICS-TARGET:
  CC̄:          3.4 → ≤2.4
  max-CC:      20 → ≤10
  god-modules: 2 → 0
  high-CC(≥15): 1 → ≤0
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
  prev CC̄=3.6 → now CC̄=3.4
```

## Intent

WronAI resource agent monorepo — uri3, nl2uri, hypervisor, agent factory
