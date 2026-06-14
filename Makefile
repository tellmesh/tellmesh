.PHONY: validate generate verify test clean run-user-agent run-meta-agent meta-plan meta-pipeline meta-repair
.PHONY: uri-tree graph nl2a-weather docker-ssh-up docker-ssh-down scan-http evolution-check examples

WEATHER_PROMPT = generuj mape pogody dwa tygodnie do przodu w html

validate:
	python -m generator.validate contracts

generate:
	python -m generator.agent_generator contracts/agents/*.yaml

verify:
	python -m generator.verify agents/generated

test:
	pytest -q

uri-tree:
	nl2uri generate --no-llm -p "$(WEATHER_PROMPT)" --out domains/weather_map/uri_tree.yaml

graph:
	uri3 graph domains/weather_map/uri_tree.yaml

nl2a-weather:
	nl2a generate --no-llm -p "$(WEATHER_PROMPT)"

run-user-agent:
	uvicorn agents.generated.user_agent.main:app --reload --port 8101

run-meta-agent:
	uvicorn meta_agent.api:app --reload --port 8200

meta-plan:
	python -m meta_agent.cli plan "Stwórz agenta do obsługi zamówień z odczytem zamówienia, historią i tworzeniem zamówienia"

meta-pipeline:
	python -m meta_agent.cli pipeline "Stwórz agenta do obsługi zamówień z odczytem zamówienia, historią i tworzeniem zamówienia"

meta-repair:
	python -m meta_agent.cli repair examples/05_meta_repair/broken_agent.yaml --write

docker-ssh-up:
	docker compose -f examples/03_ssh_remote_agent/docker-compose.yml up --build -d

docker-ssh-down:
	docker compose -f examples/03_ssh_remote_agent/docker-compose.yml down -v

scan-http:
	uri3 scan http://localhost:8101

evolution-check:
	python -m hypervisor.evolution.cli examples/08_evolution/proposals/*.yaml

examples:
	@echo "See examples/README.md for the full catalog (01–08)."

clean:
	rm -rf agents/generated/* output/* .pytest_cache
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
