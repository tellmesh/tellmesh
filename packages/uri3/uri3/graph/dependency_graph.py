from __future__ import annotations

from collections import deque
from typing import Any

from uri3.graph.models import WorkflowGraph


def adjacency(graph: WorkflowGraph) -> dict[str, list[str]]:
    mapping: dict[str, list[str]] = {node_id: [] for node_id in graph.nodes}
    for edge in graph.edges:
        mapping.setdefault(edge.source, []).append(edge.target)
        mapping.setdefault(edge.target, mapping.get(edge.target, []))
    return mapping


def reverse_adjacency(graph: WorkflowGraph) -> dict[str, list[str]]:
    mapping: dict[str, list[str]] = {node_id: [] for node_id in graph.nodes}
    for edge in graph.edges:
        mapping.setdefault(edge.target, []).append(edge.source)
        mapping.setdefault(edge.source, mapping.get(edge.source, []))
    return mapping


def detect_cycles(graph: WorkflowGraph) -> list[list[str]]:
    indegree = {node_id: 0 for node_id in graph.nodes}
    outgoing: dict[str, list[str]] = {node_id: [] for node_id in graph.nodes}
    for edge in graph.edges:
        if edge.source not in graph.nodes or edge.target not in graph.nodes:
            continue
        outgoing[edge.source].append(edge.target)
        indegree[edge.target] += 1
    queue = deque(node_id for node_id, count in indegree.items() if count == 0)
    visited = 0
    while queue:
        node_id = queue.popleft()
        visited += 1
        for target in outgoing[node_id]:
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
    if visited == len(graph.nodes):
        return []
    remaining = [node_id for node_id, count in indegree.items() if count > 0]
    return [remaining] if remaining else []


def topological_sort(graph: WorkflowGraph) -> list[str]:
    cycles = detect_cycles(graph)
    if cycles:
        raise ValueError(f"Workflow graph contains dependency cycle: {cycles[0]}")
    indegree = {node_id: 0 for node_id in graph.nodes}
    outgoing: dict[str, list[str]] = {node_id: [] for node_id in graph.nodes}
    for edge in graph.edges:
        if edge.source not in graph.nodes or edge.target not in graph.nodes:
            continue
        outgoing[edge.source].append(edge.target)
        indegree[edge.target] += 1
    queue = deque(sorted(node_id for node_id, count in indegree.items() if count == 0))
    order: list[str] = []
    while queue:
        node_id = queue.popleft()
        order.append(node_id)
        for target in sorted(outgoing[node_id]):
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
    if len(order) != len(graph.nodes):
        raise ValueError("Unable to produce topological order for workflow graph")
    return order


def dependency_summary(graph: WorkflowGraph) -> dict[str, Any]:
    return {
        "id": graph.id,
        "node_count": len(graph.nodes),
        "edge_count": len(graph.edges),
        "roots": [node_id for node_id in graph.nodes if not any(edge.target == node_id for edge in graph.edges)],
        "leaves": [node_id for node_id in graph.nodes if not any(edge.source == node_id for edge in graph.edges)],
        "cycles": detect_cycles(graph),
        "order": topological_sort(graph) if not detect_cycles(graph) else [],
    }
