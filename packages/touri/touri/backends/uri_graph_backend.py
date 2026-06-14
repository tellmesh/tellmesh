"""Compatibility shim — graph backend execution lives in uri2run."""

from touri.backends.uri_flow_backend import call_uri_graph_backend

__all__ = ["call_uri_graph_backend"]
