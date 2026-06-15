"""Tests for examples/*/ABOUT.md landing integration builder."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def _www_scripts(repo_root: Path) -> Path:
    return repo_root.parent.parent / "tellmesh" / "www" / "scripts"


def test_about_parser_loads_cards(repo_root: Path):
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "about_parser",
        _www_scripts(repo_root) / "about_parser.py",
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)

    path = repo_root / "examples" / "32_ecommerce_integrations" / "ABOUT.md"
    about = module.load_about(path)
    assert about["example_id"] == "32_ecommerce_integrations"
    assert len(about["cards"]) >= 5
    assert any(c.get("id") == "woocommerce-connector" for c in about["cards"])


def test_build_landing_integrations_check(repo_root: Path):
    script = _www_scripts(repo_root) / "build_landing_integrations.py"
    result = subprocess.run(
        [sys.executable, str(script), "--check"],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr or result.stdout


def test_build_examples_manifest_check(repo_root: Path):
    script = _www_scripts(repo_root) / "build_examples_manifest.py"
    result = subprocess.run(
        [sys.executable, str(script), "--check"],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr or result.stdout


def test_examples_manifest_includes_office_chains(repo_root: Path):
    script = _www_scripts(repo_root) / "build_examples_manifest.py"
    import importlib.util

    spec = importlib.util.spec_from_file_location("build_examples_manifest", script)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)

    manifest = module.build_manifest()
    chains = manifest.get("officeChains") or []
    assert len(chains) >= 4
    assert chains[0]["steps"]
    assert any(chain["id"] == "portal-report" for chain in chains)


def test_index_has_generated_integration_cards(www_root: Path):
    html = (www_root / "index.html").read_text(encoding="utf-8")
    assert 'data-integration-card="woocommerce-connector"' in html
    assert "workflow://order/woocommerce-to-erp" in html
    assert "integration-build-hint" not in html or "Run" not in html.split("integration-build-hint")[1][:120]


def test_spotlight_includes_full_i18n_cta_and_body(repo_root: Path):
    import importlib.util

    script = _www_scripts(repo_root) / "build_landing_integrations.py"
    spec = importlib.util.spec_from_file_location("build_landing_integrations", script)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)

    cards, _ = module.collect_cards()
    spotlight = next(c for c in cards if c.get("id") == "ecommerce-spotlight")
    html = module.render_spotlight(spotlight, spotlight.get("_body_html") or "")
    assert 'data-i18n-lang="en"' in html
    assert 'data-i18n-lang="pl"' in html
    assert "Try a question in chat" in html
    assert "Wypróbuj pytanie w chacie" in html
    assert "integration-i18n" in html
    assert "WooCommerce webhook" in html or "WooCommerce Webhook" in spotlight.get("_body_html", "")


def _load_integrations_module(repo_root: Path):
    import importlib.util

    script = _www_scripts(repo_root) / "build_landing_integrations.py"
    spec = importlib.util.spec_from_file_location("build_landing_integrations", script)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_all_about_cards_reused_on_website(repo_root: Path, www_root: Path):
    """Every card from examples/*/ABOUT.md must appear on index.html with key content."""
    import html as html_lib
    import importlib.util

    about_spec = importlib.util.spec_from_file_location(
        "about_parser",
        _www_scripts(repo_root) / "about_parser.py",
    )
    about_mod = importlib.util.module_from_spec(about_spec)
    assert about_spec.loader is not None
    about_spec.loader.exec_module(about_mod)

    mod = _load_integrations_module(repo_root)
    index = (www_root / "index.html").read_text(encoding="utf-8")
    fragment = (www_root / "generated/integrations.fragment.html").read_text(encoding="utf-8")
    cards, _ = mod.collect_cards()

    assert len(cards) >= 16

    for card in cards:
        card_id = str(card.get("id"))
        example = str(card.get("example"))
        assert f'data-integration-card="{card_id}"' in index, card_id
        assert f'data-integration-card="{card_id}"' in fragment, card_id
        assert f'data-example="{example}"' in index, card_id

        snippet = str(card.get("snippet") or "").strip()
        if snippet:
            first_line = snippet.splitlines()[0]
            assert html_lib.escape(first_line) in index, card_id

        en_title = ((card.get("i18n") or {}).get("en") or {}).get("title")
        if en_title:
            assert en_title in index, card_id

        if card.get("layout") == "card":
            body_src = str(card.get("body") or "").strip()
            if not body_src:
                about = about_mod.load_about(repo_root / "examples" / example / "ABOUT.md")
                body_src = about["body"].strip()
            if body_src:
                assert "integration-card-body" in index
                import re

                plain = re.sub(r"<[^>]+>", " ", body_src)
                tokens = [t for t in re.findall(r"[\w:/.-]{8,}", plain) if not t.startswith("http")]
                assert any(token in index for token in tokens), f"{card_id}: {tokens[:3]}"

    # No ABOUT body without a card/spotlight consumer
    for path in about_mod.iter_about_files(repo_root / "examples"):
        about = about_mod.load_about(path)
        if not about["body"].strip():
            continue
        consumers = [c for c in about["cards"] if c.get("layout") in {"card", "spotlight"}]
        assert consumers, f"orphan ABOUT body: {path.parent.name}"


def test_index_integrations_match_fragment(repo_root: Path, www_root: Path):
    mod = _load_integrations_module(repo_root)
    cards, _ = mod.collect_cards()
    connectors_html, grid_html = mod.build_sections(cards)
    expected = (connectors_html + "\n" + grid_html).strip()
    fragment = (www_root / "generated/integrations.fragment.html").read_text(encoding="utf-8").strip()
    index = (www_root / "index.html").read_text(encoding="utf-8")

    assert fragment == expected

    def extract(html: str, start: str, end: str) -> str:
        a = html.index(start) + len(start)
        b = html.index(end, a)
        return html[a:b].strip()

    index_connectors = extract(
        index,
        "<!-- @integrations-connectors:start -->",
        "<!-- @integrations-connectors:end -->",
    )
    index_grid = extract(
        index,
        "<!-- @integrations-grid:start -->",
        "<!-- @integrations-grid:end -->",
    )
    assert index_connectors in expected
    assert index_grid in expected


def test_ecommerce_cards_use_distinct_bodies(repo_root: Path):
    mod = _load_integrations_module(repo_root)
    cards, _ = mod.collect_cards()
    by_id = {c["id"]: c for c in cards}
    woo_body = by_id["woocommerce-card"]["_body_html"]
    bl_body = by_id["baselinker-card"]["_body_html"]
    al_body = by_id["allegro-card"]["_body_html"]
    assert "order.created" in woo_body
    assert "getOrders" in bl_body
    assert "OAuth Allegro" in al_body
    assert woo_body != bl_body != al_body
