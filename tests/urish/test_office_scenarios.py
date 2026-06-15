"""Tests for landing-page office scenario routing."""

from __future__ import annotations

import pytest
from urish.backends.ask import ask_prompt
from urish.intent import detect_intent
from urish.scenario_registry import match_scenario, scenarios_for_kind

LANDING_QUOTES = [
    (
        "website_report",
        "portal_report",
        "Wejdź na stronę dostawcy, pobierz raport CSV za ten miesiąc i zapisz w rozliczeniach.",
        "workflow://office/supplier-report/monthly",
    ),
    (
        "portal_zus_form",
        "portal_form",
        "Zaloguj się do portalu klienta, uzupełnij formularz ZUS i wyślij — "
        "najpierw pokaż podgląd.",
        "workflow://portal/zus-form/dry-run",
    ),
    (
        "erp_subiekt",
        "erp_pcwin",
        "Otwórz Subiekta, wklej dane z Excela do faktury i zapisz jako szkic.",
        "pcwin://window/Subiekt GT/focus",
    ),
    (
        "invoice_batch_woo",
        "invoice_batch",
        "Wystaw faktury za zamówienia z WooCommerce, pokaż listę do akceptacji "
        "i wyślij tylko zatwierdzone.",
        "workflow://invoices/batch/dry-run",
    ),
    (
        "bank_batch",
        "bank_transfer",
        "Przygotuj przelewy do dostawców z listy — zatrzymaj się przed autoryzacją.",
        "workflow://bank/batch-transfer/dry-run",
    ),
    (
        "android_2fa",
        "android_2fa",
        "Bank czeka na potwierdzenie w aplikacji — pokaż mi ekran telefonu.",
        "android://device/pixel-7/screenshot",
    ),
]


@pytest.mark.parametrize(
    ("scenario_id", "subtype", "prompt", "expected_uri"),
    LANDING_QUOTES,
)
def test_landing_quote_maps_to_scenario(scenario_id, subtype, prompt, expected_uri):
    scenario = match_scenario(prompt, kind="office")
    assert scenario is not None
    assert scenario["id"] == scenario_id
    assert scenario["subtype"] == subtype

    intent = detect_intent(prompt)
    assert intent["kind"] == "office"
    assert intent["subtype"] == subtype
    assert intent.get("scenario_id") == scenario_id
    assert expected_uri in intent["planned_uris"]


@pytest.mark.parametrize(("scenario_id", "_subtype", "prompt", "_expected_uri"), LANDING_QUOTES)
def test_ask_landing_quote_returns_card_uris(scenario_id, _subtype, prompt, _expected_uri):
    result = ask_prompt(prompt)
    data = result["data"]
    assert data["detected_kind"] == "office"
    assert data.get("scenario_id") == scenario_id
    assert data["planned_uris"]


def test_office_scenario_count_matches_landing():
    assert len(scenarios_for_kind("office")) == 6
