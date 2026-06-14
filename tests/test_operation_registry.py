from uri2ops.operation_registry.loader import load_operation_registry
from uri2ops.operation_registry.validator import validate_operation_registry


def test_registry_loads():
    reg = load_operation_registry()
    assert reg.get("browser", "open") is not None
    assert reg.get("assertion", "check") is not None


def test_registry_validates():
    assert validate_operation_registry(load_operation_registry()) == []
