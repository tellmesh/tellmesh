# AUTO-GENERATED FILE. DO NOT EDIT.
# Source: contracts/agents/generuj_mape_pogody_dwa_tygodnie_do_przodu_w_html_agent.yaml
# Contract hash: sha256:1032ca7c45efe2b94b47aa66b6bda819294316637b494c4ac51dd2724c009bda

# ruff: noqa: E501

AGENT_CARD = {'name': 'generuj-mape-pogody-dwa-tygodnie-do-przodu-w-html-agent',
 'version': '0.1.0',
 'description': 'generuj mape pogody dwa tygodnie do przodu w html',
 'generated_from': {'contract': 'contracts/agents/generuj_mape_pogody_dwa_tygodnie_do_przodu_w_html_agent.yaml',
                    'contract_hash': 'sha256:1032ca7c45efe2b94b47aa66b6bda819294316637b494c4ac51dd2724c009bda'},
 'capabilities': [{'name': 'run',
                   'type': 'command',
                   'description': '',
                   'uri': None,
                   'output_schema': None,
                   'renderer': None,
                   'command': 'RunTask',
                   'input_schema': 'app.generuj_mape_pogody_dwa_tygodnie_do_przodu_w_html.v1.RunTaskCommand',
                   'emits': ['TaskRequested', 'TaskCompleted']}]}
