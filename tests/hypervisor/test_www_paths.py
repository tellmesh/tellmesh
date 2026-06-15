from __future__ import annotations

from hypervisor.paths import resolve_www_dir


def test_resolve_www_dir_prefers_tellmesh(repo_root):
    resolved = resolve_www_dir(repo_root)
    assert resolved is not None
    assert (resolved / "index.html").is_file()
    assert resolved.name == "www"
    hypervisor_www = repo_root / "www"
    assert not (hypervisor_www / "index.html").exists()
    if (repo_root.parent.parent / "tellmesh" / "www" / "index.html").is_file():
        assert "tellmesh" in resolved.as_posix()
