"""Tests for office automation NL intent routing."""

from __future__ import annotations

from urish.backends.ask import ask_prompt
from urish.intent import detect_intent


def test_detect_office_invoice_batch():
    intent = detect_intent("wystaw faktury za wczoraj i pokaż podgląd przed wysyłką")
    assert intent["kind"] == "office"
    assert intent["subtype"] == "invoice_batch"
    assert "workflow://invoices/batch/dry-run" in intent["planned_uris"]


def test_detect_office_portal_report():
    intent = detect_intent(
        "Wejdź na stronę dostawcy, pobierz raport CSV za ten miesiąc i zapisz w rozliczeniach."
    )
    assert intent["kind"] == "office"
    assert intent["subtype"] == "portal_report"
    assert "workflow://office/supplier-report/monthly" in intent["planned_uris"]


def test_detect_office_bank_transfer():
    intent = detect_intent("przygotuj przelewy z listy i zatrzymaj się przed autoryzacją w banku")
    assert intent["kind"] == "office"
    assert intent["subtype"] == "bank_transfer"
    assert "workflow://bank/batch-transfer/dry-run" in intent["planned_uris"]


def test_detect_office_invoice_status():
    intent = detect_intent("co się stało z procesem faktur? pokaż ostatni błąd")
    assert intent["kind"] == "office"
    assert intent["subtype"] in {"office_status", "invoice_status"}


def test_agent_diagnose_still_wins_over_office():
    intent = detect_intent("zdiagnozuj agenta invoices-agent.local")
    assert intent["kind"] == "agent"
    assert intent["subtype"] == "diagnose"


def test_ask_office_invoice_batch():
    result = ask_prompt(
        "Wystaw faktury za zamówienia z WooCommerce, pokaż listę do akceptacji "
        "i wyślij tylko zatwierdzone."
    )
    data = result["data"]
    assert data["detected_kind"] == "office"
    assert data["detected_subtype"] == "invoice_batch"
    assert data.get("scenario_id") == "invoice_batch_woo"
    assert "workflow://invoices/batch/dry-run" in data["planned_uris"]


def test_detect_office_ecommerce_sync():
    intent = detect_intent("połącz WooCommerce, BaseLinker i ERP; pokaż błędy w chacie")
    assert intent["kind"] == "office"
    assert intent["subtype"] == "ecommerce_sync"
    assert "workflow://order/woocommerce-to-erp/dry-run" in intent["planned_uris"]


def test_detect_office_allegro_erp_failure():
    intent = detect_intent("dlaczego zamówienie z Allegro nie trafiło do ERP?")
    assert intent["kind"] == "office"
    assert intent["subtype"] == "ecommerce_sync"
    assert "log://hypervisor?grep=order&level=ERROR" in intent["planned_uris"]


def test_ask_office_ecommerce_sync():
    result = ask_prompt("połącz WooCommerce, BaseLinker i ERP; pokaż błędy w chacie")
    data = result["data"]
    assert data["detected_subtype"] == "ecommerce_sync"
    assert "workflow://order/woocommerce-to-erp/dry-run" in data["planned_uris"]
    assert any("32_ecommerce_integrations" in step for step in data["next_steps"])
