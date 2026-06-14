# Example 01 — lokalny quickstart

Minimalny przepływ bez Dockera i bez LLM.

```bash
pip install -e .[dev]
make uri-tree
make validate
make graph
make test
```

Lub skrypt:

```bash
./examples/01_quickstart_local/run.sh
```

Wynikowy URI Tree:

```txt
domains/weather_map/uri_tree.yaml
```

Łańcuch:

```txt
prompt -> nl2uri -> URI Tree -> uri3 validate/graph
```
