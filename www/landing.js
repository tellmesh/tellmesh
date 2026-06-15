/**
 * Taskinity landing — product tour slides, scroll reveal, FAQ
 */
(function () {
  "use strict";

  const THEME_KEY = "taskinity.theme";
  const LANG_KEY = "taskinity.lang";
  const THEMES = ["warm", "dark", "light"];
  const LANGS = ["pl", "en", "de"];
  const TRANSLATIONS = {
    pl: {
      title: "Taskinity — command center dla automatyzacji i agentów AI",
      metaDescription: "Jeden chat i dashboard: integracje WordPress, WooCommerce, BaseLinker, Allegro, ERP, CRM, agenci AI, health, incident i naprawa.",
      nav: {
        problem: "Problem",
        tour: "Jak działa",
        integrations: "Integracje",
        office: "Przykłady biuro",
        lab: "Lab integracji",
        docs: "Docs examples",
        offer: "Oferta",
        chat: "Otwórz chat",
        demo: "Umów demo",
      },
      controls: {
        warm: "Warm",
        dark: "Dark",
        light: "Light",
        prev: "← Wstecz",
        next: "Dalej →",
        pause: "⏸ Pauza",
        play: "▶ Odtwórz",
        copyChat: "Kopiuj chat",
        copied: "Skopiowano",
        noChat: "Brak chatu",
        error: "Błąd",
        noClipboard: "Brak schowka",
      },
      hero: {
        badge: "Command center · PL · self-host",
        title: "Automatyzacje i agenci AI przestali działać? Taskinity pokaże gdzie, dlaczego i co zrobić dalej.",
        lead: "Jeden chat i dashboard dla skryptów, webhooków, n8n, API, Dockera i agentów AI. Health, logi, incident, ticket i propozycja naprawy — bez szukania po pięciu narzędziach.",
        demo: "Zobacz demo (2 min)",
        chat: "Wypróbuj chat na żywo",
        stat1: "3 procesy",
        stat1Sub: "w pilocie",
        stat2: "7–14 dni",
        stat2Sub: "wdrożenie",
        stat3: "od 2 500 zł",
        stat3Sub: "audyt",
        shotTop: "autonomy run · 3 agents · repair loop",
        shotUser: "stwórz 3 agentów i pilnuj health",
        shotPlan: "Plan: generate → run → inspect → repair",
        shotOk: "user-agent naprawiony · 1 próba",
      },
      problem: {
        title: "Znasz ten poniedziałek o 9:00?",
        lead: "Klient nie mówi „potrzebuję control plane”. Mówi tak:",
        card1: "Automatyzacja faktur znowu nie działa — nie wiem, gdzie tego szukać.",
        card2: "Scenario w n8n poszedł, ale dane nie doszły do ERP.",
        card3: "Skrypt pisał ktoś, kto już nie pracuje — nie wiemy, czy w ogóle działa.",
        card4: "Nie mam jednego miejsca na crony, webhooki, pipeline’y i agentów.",
      },
      tour: {
        title: "Autonomia w praktyce",
        lead: "Interaktywny pokaz: komenda NL tworzy agentów, runtime odbija zajęte porty, a supervisor naprawia awarię w pętli.",
        steps: ["Komenda NL", "Plan URI", "3 agenci", "Awaria", "Repair loop", "Proof"],
        labKicker: "Tryb praktyczny",
        labTitle: "Odtwórz przebieg autonomii w terminalu",
        replay: "Odtwórz terminal",
        tabs: ["3 agenci", "Port zajęty", "Awaria + repair", "E-commerce", "Biuro"],
        mapKicker: "Mapa systemu",
        mapTitle: "Od komendy po naprawę",
      },
      features: {
        title: "Co dostajesz",
        lead: "Kontrola nad chaosem automatyzacji — nie kolejny framework agenta.",
        card1Title: "Jeden widok",
        card1Lead: "Cron, API, Docker, n8n, agenci — status w jednym miejscu.",
        card2Title: "Chat po polsku",
        card2Lead: "„Co się stało z procesem faktur?” → status, przyczyna, logi.",
        card3Title: "Health",
        card3Lead: "Widać od razu, co działa, a co wymaga uwagi.",
        card4Title: "Incident → ticket",
        card4Lead: "Błąd z kontekstem — eskalacja do naprawy lub zmiany w systemie.",
        card5Title: "Naprawa z podglądem",
        card5Lead: "Propozycja kroków — dry-run, potem świadome approve.",
        card6Title: "Wdrożenie w PL",
        card6Lead: "Polski język, lokalny support, self-host u klienta.",
      },
      audience: {
        title: "Dla kogo",
        card1Title: "Software house’y",
        card1Lead: "Panel procesów dla projektów i klientów — możliwość odsprzedaży utrzymania.",
        card2Title: "Integratorzy n8n / Make",
        card2Lead: "Warstwa SLA nad wdrożeniami — panel serwisowy dla klientów.",
        card3Title: "E-commerce",
        card3Lead: "Zamówienia, faktury, ERP, marketplace — jeden chat przy awarii.",
        card4Title: "Biura i BPO",
        card4Lead: "Dokumenty, OCR, KSeF — widok od maila do systemu księgowego.",
      },
      integrations: {
        title: "Integracje w 3 krokach",
        lead: "Nie zastępujemy WordPressa, WooCommerce, Baselinkera ani Allegro — spinamy je w jeden command center. Każda integracja to ten sam wzorzec: <strong>zdarzenie → URI → health → chat przy awarii</strong>.",
        simpleKicker: "Najprostszy wzorzec",
        simpleTitle: "Nie przepinasz firmy na nowy system. Dokładasz cienką warstwę nad tym, co już działa.",
        simpleLead: "Każdy portal, ERP, CRM albo sklep dostaje jeden opis procesu: skąd przychodzi zdarzenie, jakie URI ma zostać wykonane, gdzie sprawdzić health i kto akceptuje kroki ryzykowne.",
        fastKicker: "Start w 15 minut",
        fastTitle: "Minimalny kontrakt integracji",
        fastLead: "Najpierw nie budujesz pełnego konektora. Rejestrujesz jeden proces, jeden health check i jeden sposób diagnozy.",
        step1Title: "Podłącz źródło",
        step1Lead: "Webhook, REST API, plugin WordPress, cron lub skrypt — cokolwiek już masz. Taskinity woła to przez http:// albo shell://.",
        step2Title: "Zarejestruj proces",
        step2Lead: "Jeden wpis w rejestrze deploymentów: nazwa, health URI, logi. Widzisz status w dashboardzie i API.",
        step3Title: "Monitoruj i naprawiaj",
        step3Lead: "Health co 5 min, alert webhookiem, chat po polsku i dry-run przed każdą mutacją.",
        pipe1Title: "System źródłowy",
        pipe1Lead: "WordPress, WooCommerce, BaseLinker, Allegro, ERP, CRM lub portal WWW.",
        pipe2Title: "Webhook / API",
        pipe2Lead: "REST, cron, plugin, skrypt, Playwright albo adapter okienkowy.",
        pipe3Title: "URI workflow",
        pipe3Lead: "workflow://order/sync, health://agent/... albo repair://...",
        pipe4Title: "Chat i proof",
        pipe4Lead: "Wynik, screenshot, logi, dry-run, approval i raport audytowy w jednym miejscu.",
        wordpressTitle: "Lead z formularza do CRM",
        wordpressLead: "Hook formularza lub REST API wysyła zdarzenie do Taskinity, a agent dopisuje kontakt w CRM i odsyła potwierdzenie.",
        wooTitle: "Zamówienie do faktury i magazynu",
        wooLead: "Webhook sklepu uruchamia workflow: pobierz zamówienie, sprawdź płatność, wystaw fakturę i zsynchronizuj stan.",
        baselinkerTitle: "Marketplace hub bez ślepych cronów",
        baselinkerLead: "Cron lub n8n woła API BaseLinker, a Taskinity porównuje zamówienia, stany i błędy synchronizacji z ERP.",
        allegroTitle: "OAuth, zamówienia, zwroty",
        allegroLead: "Agent pilnuje tokenu OAuth, pobiera checkout forms, wykrywa 429/503 i pokazuje w chacie, które zamówienie utknęło.",
        erpTitle: "Comarch, Subiekt, HubSpot, Salesforce",
        erpLead: "REST, SOAP, CSV, SQL albo okna Windows. System rozdziela automatyczne kroki od tych, które wymagają akceptacji człowieka.",
        portalTitle: "Logowanie, pobieranie danych, formularze",
        portalLead: "Playwright lub browser adapter wykonuje czynności w portalu, robi screenshot i zatrzymuje się przed wysyłką danych.",
      },
      office: {
        title: "Jak pracuje biuro — konkretne przykłady",
        lead: "Marta, specjalista ds. rozliczeń, nie pisze skryptów. Opisuje zadanie po polsku w chacie. Taskinity planuje kroki: strona WWW, portal, okna w systemie, faktura, bank — a gdy trzeba tokenu na telefonie, <strong>prosi Martę o jeden klik</strong> i kontynuuje resztę.",
      },
      offer: {
        title: "Oferta",
        lead: "Od audytu do utrzymania — konkretny efekt, nie abstrakcyjna „platforma agentowa”.",
        auditTitle: "Audyt automatyzacji",
        auditMeta: "netto · 1–3 dni",
        pilotTitle: "Pilot 3 procesów",
        pilotMeta: "netto · 7–14 dni",
        careTitle: "Utrzymanie",
        careMeta: "netto / mies.",
        auditCta: "Zapytaj o audyt",
        pilotCta: "Umów pilot",
        careCta: "Porozmawiajmy",
      },
      tech: {
        title: "Dla zespołów technicznych",
        lead: "URI to sekret architektoniczny — nie pierwsze hasło sprzedażowe.",
      },
      contact: {
        title: "Umów 10-min demo",
        lead: "Pokażemy scenariusz: webhook → błąd API → incident → ticket → naprawa.",
        mail: "Napisz: kontakt@taskinity.local",
        chat: "Otwórz chat produkcyjny",
        demo: "Demo techniczne (URI)",
      },
      faq: {
        q1: "Czy Taskinity obsługuje banki i token na telefonie?",
        a1: "Tak — w modelu human-in-the-loop. Agent wypełnia przelew w banku online, zatrzymuje się przed autoryzacją, pokazuje podgląd i czeka na klik człowieka.",
        q2: "Jak podłączyć WooCommerce, Baselinker lub Allegro?",
        a2: "Webhook lub cron woła URI agenta. Taskinity rejestruje proces, monitoruje health i przy awarii pokazuje incident w chacie.",
        q3: "Czy zastępujecie n8n / Make / Zapier?",
        a3: "Nie. Masz już automatyzacje — Taskinity pokazuje, które działają, które padły i co dalej.",
        q4: "Czym różnicie się od LangSmith Engine?",
        a4: "LangSmith Engine skupia się na agentach LangChain. Taskinity spina skrypty, cron, webhooki, n8n, Docker i agentów w jeden command center.",
        q5: "Czy to dla firm bez agentów AI?",
        a5: "Tak — skrypty, cron i webhooki często padają pierwsze i też je monitorujemy.",
        q6: "Czy macie SOC2 / enterprise governance?",
        a6: "Nie — produkt dla MŚP i software house’ów, self-host z policy gate i dry-run przed mutacją.",
      },
      steps: {
        prompt: {
          title: "Jedna komenda zamiast ręcznego klejenia usług",
          caption: "Operator opisuje cel po polsku. Taskinity zamienia go na plan URI, artefakty i kontrolowany runtime.",
        },
        plan: {
          title: "NL → plan URI",
          caption: "System rozbija prompt na kroki: generowanie agentów, rejestr deploymentów, start, inspect i supervisor.",
        },
        agents: {
          title: "3 agenci startują mimo zajętych portów",
          caption: "Preferowane porty są zajęte przez inne usługi, więc runtime wybiera wolne porty i zapisuje effective health URI.",
        },
        failure: {
          title: "Jeden agent pada",
          caption: "Proces user-agent zostaje zabity poza hypervisorem. State nadal wskazuje stary PID, więc inspect widzi stale runtime.",
        },
        repair: {
          title: "Supervisor naprawia w pętli",
          caption: "Inspect → klasyfikacja → restart na effective port → ponowny health/card. Po jednej próbie agent wraca do healthy.",
        },
        proof: {
          title: "Dowód: proces, health, card i logi są spójne",
          caption: "Ta sama prawda jest widoczna w Web UI, CLI, API i runtime state. To pozwala systemowi działać autonomicznie.",
        },
      },
    },
    en: {
      title: "Taskinity — command center for automation and AI agents",
      metaDescription: "One chat and dashboard for WordPress, WooCommerce, BaseLinker, Allegro, ERP, CRM, AI agents, health checks, incidents and repairs.",
      nav: {
        problem: "Problem",
        tour: "How it works",
        integrations: "Integrations",
        office: "Office examples",
        lab: "Integration lab",
        docs: "Docs examples",
        offer: "Offer",
        chat: "Open chat",
        demo: "Book demo",
      },
      controls: {
        warm: "Warm",
        dark: "Dark",
        light: "Light",
        prev: "← Back",
        next: "Next →",
        pause: "⏸ Pause",
        play: "▶ Play",
        copyChat: "Copy chat",
        copied: "Copied",
        noChat: "No chat",
        error: "Error",
        noClipboard: "No clipboard",
      },
      hero: {
        badge: "Command center · EN · self-host",
        title: "Did your automations or AI agents stop working? Taskinity shows where, why, and what to do next.",
        lead: "One chat and dashboard for scripts, webhooks, n8n, APIs, Docker and AI agents. Health, logs, incidents, tickets and repair proposals without searching five tools.",
        demo: "See demo (2 min)",
        chat: "Try live chat",
        stat1: "3 processes",
        stat1Sub: "in the pilot",
        stat2: "7–14 days",
        stat2Sub: "deployment",
        stat3: "from PLN 2,500",
        stat3Sub: "audit",
        shotTop: "autonomy run · 3 agents · repair loop",
        shotUser: "create 3 agents and monitor health",
        shotPlan: "Plan: generate → run → inspect → repair",
        shotOk: "user-agent repaired · 1 attempt",
      },
      problem: {
        title: "You know that Monday at 9:00?",
        lead: "Clients do not ask for a control plane. They say this:",
        card1: "Invoice automation is broken again and I do not know where to look.",
        card2: "The n8n scenario ran, but the data never reached ERP.",
        card3: "The script was written by someone who no longer works here.",
        card4: "I do not have one place for cron jobs, webhooks, pipelines and agents.",
      },
      tour: {
        title: "Autonomy in practice",
        lead: "Interactive walkthrough: an NL command creates agents, runtime handles busy ports, and supervisor repairs failures in a loop.",
        steps: ["NL command", "URI plan", "3 agents", "Failure", "Repair loop", "Proof"],
        labKicker: "Practical mode",
        labTitle: "Replay the autonomy flow in terminal",
        replay: "Replay terminal",
        tabs: ["3 agents", "Busy port", "Failure + repair", "E-commerce", "Office"],
        mapKicker: "System map",
        mapTitle: "From command to repair",
      },
      features: {
        title: "What you get",
        lead: "Control over automation chaos, not another agent framework.",
        card1Title: "One view",
        card1Lead: "Cron, API, Docker, n8n and agents — status in one place.",
        card2Title: "Natural-language chat",
        card2Lead: "“What happened to invoice processing?” → status, cause and logs.",
        card3Title: "Health",
        card3Lead: "See immediately what works and what needs attention.",
        card4Title: "Incident → ticket",
        card4Lead: "A failure with context, ready for escalation or repair.",
        card5Title: "Repair with preview",
        card5Lead: "Proposed steps: dry-run first, then explicit approve.",
        card6Title: "Local rollout",
        card6Lead: "Polish support, self-hosted deployment and client-specific setup.",
      },
      audience: {
        title: "Who it is for",
        card1Title: "Software houses",
        card1Lead: "Process panel for projects and clients, with maintenance resale potential.",
        card2Title: "n8n / Make integrators",
        card2Lead: "An SLA layer above automations and a service panel for clients.",
        card3Title: "E-commerce",
        card3Lead: "Orders, invoices, ERP and marketplace flows with one chat on failure.",
        card4Title: "Offices and BPO",
        card4Lead: "Documents, OCR and accounting flows from email to the target system.",
      },
      integrations: {
        title: "Integrations in 3 steps",
        lead: "We do not replace WordPress, WooCommerce, BaseLinker or Allegro. We connect them into one command center. Every integration follows the same pattern: <strong>event → URI → health → chat on failure</strong>.",
        simpleKicker: "The simplest pattern",
        simpleTitle: "You do not migrate the company to a new system. You add a thin layer above what already works.",
        simpleLead: "Every portal, ERP, CRM or store gets one process contract: where the event comes from, which URI to run, where to check health, and who approves risky steps.",
        fastKicker: "Start in 15 minutes",
        fastTitle: "Minimal integration contract",
        fastLead: "Do not build a full connector first. Register one process, one health check and one diagnosis path.",
        step1Title: "Connect the source",
        step1Lead: "Webhook, REST API, WordPress plugin, cron or script: whatever you already have. Taskinity calls it via http:// or shell://.",
        step2Title: "Register the process",
        step2Lead: "One deployment registry entry: name, health URI and logs. You see status in the dashboard and API.",
        step3Title: "Monitor and repair",
        step3Lead: "Health every 5 minutes, webhook alert, natural-language chat and dry-run before every mutation.",
        pipe1Title: "Source system",
        pipe1Lead: "WordPress, WooCommerce, BaseLinker, Allegro, ERP, CRM or any web portal.",
        pipe2Title: "Webhook / API",
        pipe2Lead: "REST, cron, plugin, script, Playwright or desktop UI adapter.",
        pipe3Title: "URI workflow",
        pipe3Lead: "workflow://order/sync, health://agent/... or repair://...",
        pipe4Title: "Chat and proof",
        pipe4Lead: "Result, screenshot, logs, dry-run, approval and audit report in one place.",
        wordpressTitle: "Form lead to CRM",
        wordpressLead: "A form hook or REST API sends the event to Taskinity. The agent creates the CRM contact and returns confirmation.",
        wooTitle: "Order to invoice and stock",
        wooLead: "A store webhook starts the workflow: fetch order, check payment, issue invoice and sync inventory.",
        baselinkerTitle: "Marketplace hub without blind cron jobs",
        baselinkerLead: "Cron or n8n calls the BaseLinker API, while Taskinity compares orders, stock and ERP sync errors.",
        allegroTitle: "OAuth, orders, returns",
        allegroLead: "The agent watches the OAuth token, fetches checkout forms, detects 429/503 and shows the stuck order in chat.",
        erpTitle: "Comarch, Subiekt, HubSpot, Salesforce",
        erpLead: "REST, SOAP, CSV, SQL or Windows UI. The system separates automatic steps from human approval.",
        portalTitle: "Login, data extraction, forms",
        portalLead: "Playwright or the browser adapter works in the portal, takes screenshots and stops before sending data.",
      },
      office: {
        title: "How an office works — concrete examples",
        lead: "Marta from accounting does not write scripts. She describes the task in chat. Taskinity plans the steps: website, portal, desktop app, invoice, bank. When a phone token is needed, <strong>Taskinity asks Marta for one click</strong> and continues.",
      },
      offer: {
        title: "Offer",
        lead: "From audit to maintenance: concrete outcomes, not an abstract agent platform.",
        auditTitle: "Automation audit",
        auditMeta: "net · 1–3 days",
        pilotTitle: "3-process pilot",
        pilotMeta: "net · 7–14 days",
        careTitle: "Maintenance",
        careMeta: "net / month",
        auditCta: "Ask about audit",
        pilotCta: "Book pilot",
        careCta: "Talk to us",
      },
      tech: {
        title: "For technical teams",
        lead: "URI is the architecture secret, not the first sales headline.",
      },
      contact: {
        title: "Book a 10-minute demo",
        lead: "We will show: webhook → API error → incident → ticket → repair.",
        mail: "Email: kontakt@taskinity.local",
        chat: "Open production chat",
        demo: "Technical demo (URI)",
      },
      faq: {
        q1: "Does Taskinity support banks and phone tokens?",
        a1: "Yes, in a human-in-the-loop model. The agent prepares the transfer, stops before authorization, shows a preview and waits for a human click.",
        q2: "How do I connect WooCommerce, BaseLinker or Allegro?",
        a2: "A webhook or cron calls the agent URI. Taskinity registers the process, monitors health and shows an incident in chat on failure.",
        q3: "Do you replace n8n / Make / Zapier?",
        a3: "No. You already have automations. Taskinity shows which work, which failed and what comes next.",
        q4: "How are you different from LangSmith Engine?",
        a4: "LangSmith Engine focuses on LangChain agents. Taskinity connects scripts, cron, webhooks, n8n, Docker and agents into one command center.",
        q5: "Is this for companies without AI agents?",
        a5: "Yes. Scripts, cron jobs and webhooks often fail first, and we monitor them too.",
        q6: "Do you have SOC2 / enterprise governance?",
        a6: "No. This is for SMBs and software houses: self-hosted, with policy gates and dry-run before mutation.",
      },
      steps: {
        prompt: {
          title: "One command instead of hand-wiring services",
          caption: "The operator describes the goal in natural language. Taskinity turns it into a URI plan, artifacts and controlled runtime.",
        },
        plan: {
          title: "NL → URI plan",
          caption: "The system breaks the prompt into steps: agent generation, deployment registry, start, inspect and supervisor.",
        },
        agents: {
          title: "3 agents start despite busy ports",
          caption: "Preferred ports are busy, so runtime selects free ports and stores the effective health URI.",
        },
        failure: {
          title: "One agent fails",
          caption: "The user-agent process is killed outside hypervisor. State points to an old PID, so inspect sees stale runtime.",
        },
        repair: {
          title: "Supervisor repairs in a loop",
          caption: "Inspect → classify → restart on effective port → health/card verification. The agent returns healthy after one attempt.",
        },
        proof: {
          title: "Proof: process, health, card and logs match",
          caption: "The same truth is visible in Web UI, CLI, API and runtime state. That is what enables autonomy.",
        },
      },
    },
    de: {
      title: "Taskinity — Command Center fuer Automatisierung und KI-Agenten",
      metaDescription: "Ein Chat und Dashboard fuer WordPress, WooCommerce, BaseLinker, Allegro, ERP, CRM, KI-Agenten, Health Checks, Incidents und Reparaturen.",
      nav: {
        problem: "Problem",
        tour: "Ablauf",
        integrations: "Integrationen",
        office: "Buero-Beispiele",
        lab: "Integrationslabor",
        docs: "Docs examples",
        offer: "Angebot",
        chat: "Chat oeffnen",
        demo: "Demo buchen",
      },
      controls: {
        warm: "Warm",
        dark: "Dunkel",
        light: "Hell",
        prev: "← Zurueck",
        next: "Weiter →",
        pause: "⏸ Pause",
        play: "▶ Start",
        copyChat: "Chat kopieren",
        copied: "Kopiert",
        noChat: "Kein Chat",
        error: "Fehler",
        noClipboard: "Keine Zwischenablage",
      },
      hero: {
        badge: "Command Center · DE · self-host",
        title: "Automatisierungen oder KI-Agenten funktionieren nicht? Taskinity zeigt wo, warum und was als Naechstes zu tun ist.",
        lead: "Ein Chat und Dashboard fuer Skripte, Webhooks, n8n, APIs, Docker und KI-Agenten. Health, Logs, Incidents, Tickets und Reparaturvorschlaege ohne Suche in fuenf Tools.",
        demo: "Demo ansehen (2 Min)",
        chat: "Live-Chat testen",
        stat1: "3 Prozesse",
        stat1Sub: "im Piloten",
        stat2: "7–14 Tage",
        stat2Sub: "Einfuehrung",
        stat3: "ab 2 500 PLN",
        stat3Sub: "Audit",
        shotTop: "autonomy run · 3 agents · repair loop",
        shotUser: "3 Agenten erstellen und Health pruefen",
        shotPlan: "Plan: generate → run → inspect → repair",
        shotOk: "user-agent repariert · 1 Versuch",
      },
      problem: {
        title: "Kennen Sie diesen Montag um 9:00?",
        lead: "Kunden fragen nicht nach einer Control Plane. Sie sagen:",
        card1: "Die Rechnungsautomatisierung ist wieder kaputt und niemand weiss, wo man suchen soll.",
        card2: "Das n8n-Szenario lief, aber die Daten kamen nie im ERP an.",
        card3: "Das Skript schrieb jemand, der nicht mehr im Unternehmen ist.",
        card4: "Es gibt keinen Ort fuer Cronjobs, Webhooks, Pipelines und Agenten.",
      },
      tour: {
        title: "Autonomie in der Praxis",
        lead: "Interaktive Demo: ein NL-Befehl erstellt Agenten, Runtime behandelt belegte Ports, Supervisor repariert Fehler in einer Schleife.",
        steps: ["NL-Befehl", "URI-Plan", "3 Agenten", "Ausfall", "Repair loop", "Proof"],
        labKicker: "Praxis-Modus",
        labTitle: "Autonomie-Ablauf im Terminal abspielen",
        replay: "Terminal abspielen",
        tabs: ["3 Agenten", "Port belegt", "Ausfall + Repair", "E-Commerce", "Buero"],
        mapKicker: "Systemkarte",
        mapTitle: "Vom Befehl zur Reparatur",
      },
      features: {
        title: "Was Sie bekommen",
        lead: "Kontrolle ueber Automatisierungschaos, nicht noch ein Agenten-Framework.",
        card1Title: "Eine Ansicht",
        card1Lead: "Cron, API, Docker, n8n und Agenten — Status an einem Ort.",
        card2Title: "Chat in natuerlicher Sprache",
        card2Lead: "„Was ist mit Rechnungen passiert?” → Status, Ursache und Logs.",
        card3Title: "Health",
        card3Lead: "Sofort sehen, was funktioniert und was Aufmerksamkeit braucht.",
        card4Title: "Incident → Ticket",
        card4Lead: "Fehler mit Kontext, bereit fuer Eskalation oder Reparatur.",
        card5Title: "Reparatur mit Vorschau",
        card5Lead: "Vorgeschlagene Schritte: erst Dry-run, dann explizite Freigabe.",
        card6Title: "Lokale Einfuehrung",
        card6Lead: "Lokaler Support, self-hosted Deployment und kundenspezifische Einrichtung.",
      },
      audience: {
        title: "Fuer wen",
        card1Title: "Softwarehaeuser",
        card1Lead: "Prozesspanel fuer Projekte und Kunden, auch als Wartungsangebot.",
        card2Title: "n8n / Make Integratoren",
        card2Lead: "SLA-Schicht ueber Automatisierungen und Servicepanel fuer Kunden.",
        card3Title: "E-Commerce",
        card3Lead: "Bestellungen, Rechnungen, ERP und Marketplace-Flows mit einem Chat bei Ausfall.",
        card4Title: "Bueros und BPO",
        card4Lead: "Dokumente, OCR und Abrechnungsprozesse von E-Mail bis Zielsystem.",
      },
      integrations: {
        title: "Integrationen in 3 Schritten",
        lead: "Wir ersetzen WordPress, WooCommerce, BaseLinker oder Allegro nicht. Wir verbinden sie in einem Command Center. Jede Integration folgt dem Muster: <strong>Ereignis → URI → Health → Chat bei Ausfall</strong>.",
        simpleKicker: "Einfachstes Muster",
        simpleTitle: "Sie migrieren die Firma nicht auf ein neues System. Sie legen eine duenne Schicht ueber das, was schon funktioniert.",
        simpleLead: "Jedes Portal, ERP, CRM oder jeder Shop bekommt einen Prozessvertrag: Quelle des Ereignisses, auszufuehrende URI, Health Check und menschliche Freigabe fuer riskante Schritte.",
        fastKicker: "Start in 15 Minuten",
        fastTitle: "Minimaler Integrationsvertrag",
        fastLead: "Nicht sofort einen kompletten Connector bauen. Erst einen Prozess, einen Health Check und einen Diagnoseweg registrieren.",
        step1Title: "Quelle verbinden",
        step1Lead: "Webhook, REST API, WordPress-Plugin, Cron oder Skript: alles, was bereits vorhanden ist. Taskinity ruft es via http:// oder shell:// auf.",
        step2Title: "Prozess registrieren",
        step2Lead: "Ein Registry-Eintrag: Name, Health URI und Logs. Status ist im Dashboard und in der API sichtbar.",
        step3Title: "Ueberwachen und reparieren",
        step3Lead: "Health alle 5 Minuten, Webhook-Alarm, Chat in natuerlicher Sprache und Dry-run vor jeder Mutation.",
        pipe1Title: "Quellsystem",
        pipe1Lead: "WordPress, WooCommerce, BaseLinker, Allegro, ERP, CRM oder ein Webportal.",
        pipe2Title: "Webhook / API",
        pipe2Lead: "REST, Cron, Plugin, Skript, Playwright oder Desktop-UI-Adapter.",
        pipe3Title: "URI-Workflow",
        pipe3Lead: "workflow://order/sync, health://agent/... oder repair://...",
        pipe4Title: "Chat und Proof",
        pipe4Lead: "Ergebnis, Screenshot, Logs, Dry-run, Freigabe und Auditbericht an einem Ort.",
        wordpressTitle: "Formular-Lead ins CRM",
        wordpressLead: "Ein Formular-Hook oder REST API sendet das Ereignis an Taskinity. Der Agent erstellt den CRM-Kontakt und bestaetigt den Schritt.",
        wooTitle: "Bestellung zu Rechnung und Bestand",
        wooLead: "Ein Shop-Webhook startet den Workflow: Bestellung holen, Zahlung pruefen, Rechnung erstellen und Bestand synchronisieren.",
        baselinkerTitle: "Marketplace-Hub ohne blinde Cronjobs",
        baselinkerLead: "Cron oder n8n ruft die BaseLinker API auf, Taskinity vergleicht Bestellungen, Bestände und ERP-Sync-Fehler.",
        allegroTitle: "OAuth, Bestellungen, Retouren",
        allegroLead: "Der Agent ueberwacht den OAuth-Token, holt Checkout-Forms, erkennt 429/503 und zeigt die haengende Bestellung im Chat.",
        erpTitle: "Comarch, Subiekt, HubSpot, Salesforce",
        erpLead: "REST, SOAP, CSV, SQL oder Windows-UI. Das System trennt automatische Schritte von menschlicher Freigabe.",
        portalTitle: "Login, Datenabruf, Formulare",
        portalLead: "Playwright oder Browser-Adapter arbeitet im Portal, erstellt Screenshots und stoppt vor dem Absenden von Daten.",
      },
      office: {
        title: "So arbeitet ein Buero — konkrete Beispiele",
        lead: "Marta aus der Abrechnung schreibt keine Skripte. Sie beschreibt die Aufgabe im Chat. Taskinity plant Website, Portal, Desktop-App, Rechnung und Bank. Wenn ein Telefon-Token noetig ist, <strong>fragt Taskinity Marta nach einem Klick</strong> und macht weiter.",
      },
      offer: {
        title: "Angebot",
        lead: "Vom Audit bis zur Wartung: konkrete Ergebnisse statt abstrakter Agentenplattform.",
        auditTitle: "Automatisierungs-Audit",
        auditMeta: "netto · 1–3 Tage",
        pilotTitle: "Pilot mit 3 Prozessen",
        pilotMeta: "netto · 7–14 Tage",
        careTitle: "Wartung",
        careMeta: "netto / Monat",
        auditCta: "Audit anfragen",
        pilotCta: "Pilot buchen",
        careCta: "Sprechen wir",
      },
      tech: {
        title: "Fuer technische Teams",
        lead: "URI ist das Architekturdetail, nicht die erste Marketingzeile.",
      },
      contact: {
        title: "10-Minuten-Demo buchen",
        lead: "Wir zeigen: Webhook → API-Fehler → Incident → Ticket → Reparatur.",
        mail: "E-Mail: kontakt@taskinity.local",
        chat: "Produktions-Chat oeffnen",
        demo: "Technische Demo (URI)",
      },
      faq: {
        q1: "Unterstuetzt Taskinity Banken und Telefon-Token?",
        a1: "Ja, im Human-in-the-loop-Modell. Der Agent bereitet die Ueberweisung vor, stoppt vor der Autorisierung, zeigt eine Vorschau und wartet auf den Klick.",
        q2: "Wie verbindet man WooCommerce, BaseLinker oder Allegro?",
        a2: "Webhook oder Cron ruft die Agent-URI auf. Taskinity registriert den Prozess, ueberwacht Health und zeigt bei Ausfall einen Incident im Chat.",
        q3: "Ersetzt ihr n8n / Make / Zapier?",
        a3: "Nein. Automatisierungen bleiben bestehen. Taskinity zeigt, welche laufen, welche ausgefallen sind und was als Naechstes kommt.",
        q4: "Unterschied zu LangSmith Engine?",
        a4: "LangSmith Engine fokussiert LangChain-Agenten. Taskinity verbindet Skripte, Cron, Webhooks, n8n, Docker und Agenten in einem Command Center.",
        q5: "Ist das fuer Firmen ohne KI-Agenten?",
        a5: "Ja. Skripte, Cronjobs und Webhooks fallen oft zuerst aus und werden ebenfalls ueberwacht.",
        q6: "Habt ihr SOC2 / Enterprise Governance?",
        a6: "Nein. Das Produkt ist fuer KMU und Softwarehaeuser: self-hosted, mit Policy Gates und Dry-run vor Mutationen.",
      },
      steps: {
        prompt: {
          title: "Ein Befehl statt manuellem Verkleben von Services",
          caption: "Der Operator beschreibt das Ziel natuerlich. Taskinity macht daraus URI-Plan, Artefakte und kontrollierte Runtime.",
        },
        plan: {
          title: "NL → URI-Plan",
          caption: "Das System zerlegt den Prompt in Schritte: Agenten-Generierung, Deployment Registry, Start, Inspect und Supervisor.",
        },
        agents: {
          title: "3 Agenten starten trotz belegter Ports",
          caption: "Bevorzugte Ports sind belegt, Runtime waehlt freie Ports und speichert die effektive Health URI.",
        },
        failure: {
          title: "Ein Agent faellt aus",
          caption: "Der user-agent Prozess wird ausserhalb des Hypervisors beendet. State zeigt auf eine alte PID, Inspect sieht stale runtime.",
        },
        repair: {
          title: "Supervisor repariert in der Schleife",
          caption: "Inspect → Klassifikation → Restart auf effektivem Port → Health/Card-Pruefung. Nach einem Versuch ist der Agent healthy.",
        },
        proof: {
          title: "Proof: Prozess, Health, Card und Logs stimmen",
          caption: "Dieselbe Wahrheit ist in Web UI, CLI, API und Runtime State sichtbar. Das ermoeglicht Autonomie.",
        },
      },
    },
  };

  const TEXT_BINDINGS = [
    ["nav.problem", '.nav-links a[href="#problem"]'],
    ["nav.tour", '.nav-links a[href="#tour"]'],
    ["nav.integrations", '.nav-links a[href="#integracje"]'],
    ["nav.office", '.nav-links a[href="#przyklady-biuro"]'],
    ["nav.lab", '.nav-links a[href="przyklady.html"]'],
    ["nav.docs", '.nav-links a[href="docs/examples.html"]'],
    ["nav.offer", '.nav-links a[href="#oferta"]'],
    ["nav.chat", '.nav-links a[href="chat.html"]'],
    ["nav.demo", '.nav-links a[href="#kontakt"]'],
    ["controls.warm", '[data-theme-choice="warm"]'],
    ["controls.dark", '[data-theme-choice="dark"]'],
    ["controls.light", '[data-theme-choice="light"]'],
    ["hero.badge", ".hero-badge"],
    ["hero.title", ".hero h1"],
    ["hero.lead", ".hero-lead"],
    ["hero.demo", '.hero-cta a[href="#tour"]'],
    ["hero.chat", '.hero-cta a[href="chat.html"]'],
    ["hero.stat1", ".hero-stats div:nth-child(1) strong"],
    ["hero.stat1Sub", ".hero-stats div:nth-child(1)", "mixedAfterStrong"],
    ["hero.stat2", ".hero-stats div:nth-child(2) strong"],
    ["hero.stat2Sub", ".hero-stats div:nth-child(2)", "mixedAfterStrong"],
    ["hero.stat3", ".hero-stats div:nth-child(3) strong"],
    ["hero.stat3Sub", ".hero-stats div:nth-child(3)", "mixedAfterStrong"],
    ["hero.shotTop", ".product-shot-top span:nth-child(2)"],
    ["hero.shotUser", ".shot-chat .shot-line:nth-child(1)"],
    ["hero.shotPlan", ".shot-chat .shot-line:nth-child(2)"],
    ["hero.shotOk", ".shot-chat .shot-line:nth-child(3)"],
    ["problem.title", "#problem .section-head h2"],
    ["problem.lead", "#problem .section-head p"],
    ["problem.card1", "#problem .pain-card:nth-child(1) p"],
    ["problem.card2", "#problem .pain-card:nth-child(2) p"],
    ["problem.card3", "#problem .pain-card:nth-child(3) p"],
    ["problem.card4", "#problem .pain-card:nth-child(4) p"],
    ["tour.title", "#tour .section-head h2"],
    ["tour.lead", "#tour .section-head p"],
    ["tour.labKicker", ".scenario-lab .scenario-kicker"],
    ["tour.labTitle", ".scenario-lab h3"],
    ["tour.replay", "#scenario-replay"],
    ["tour.mapKicker", ".system-map .scenario-kicker"],
    ["tour.mapTitle", ".system-map-head strong"],
    ["features.title", "#funkcje .section-head h2"],
    ["features.lead", "#funkcje .section-head p"],
    ["features.card1Title", "#funkcje .feature-card:nth-child(1) h3"],
    ["features.card1Lead", "#funkcje .feature-card:nth-child(1) p"],
    ["features.card2Title", "#funkcje .feature-card:nth-child(2) h3"],
    ["features.card2Lead", "#funkcje .feature-card:nth-child(2) p"],
    ["features.card3Title", "#funkcje .feature-card:nth-child(3) h3"],
    ["features.card3Lead", "#funkcje .feature-card:nth-child(3) p"],
    ["features.card4Title", "#funkcje .feature-card:nth-child(4) h3"],
    ["features.card4Lead", "#funkcje .feature-card:nth-child(4) p"],
    ["features.card5Title", "#funkcje .feature-card:nth-child(5) h3"],
    ["features.card5Lead", "#funkcje .feature-card:nth-child(5) p"],
    ["features.card6Title", "#funkcje .feature-card:nth-child(6) h3"],
    ["features.card6Lead", "#funkcje .feature-card:nth-child(6) p"],
    ["audience.title", "#dla-kogo .section-head h2"],
    ["audience.card1Title", "#dla-kogo .audience-card:nth-child(1) h3"],
    ["audience.card1Lead", "#dla-kogo .audience-card:nth-child(1) p"],
    ["audience.card2Title", "#dla-kogo .audience-card:nth-child(2) h3"],
    ["audience.card2Lead", "#dla-kogo .audience-card:nth-child(2) p"],
    ["audience.card3Title", "#dla-kogo .audience-card:nth-child(3) h3"],
    ["audience.card3Lead", "#dla-kogo .audience-card:nth-child(3) p"],
    ["audience.card4Title", "#dla-kogo .audience-card:nth-child(4) h3"],
    ["audience.card4Lead", "#dla-kogo .audience-card:nth-child(4) p"],
    ["integrations.title", "#integracje .section-head h2"],
    ["integrations.lead", "#integracje .section-head p", "html"],
    ["integrations.step1Title", ".integration-steps .integration-step:nth-child(1) h3"],
    ["integrations.step1Lead", ".integration-steps .integration-step:nth-child(1) p"],
    ["integrations.step2Title", ".integration-steps .integration-step:nth-child(2) h3"],
    ["integrations.step2Lead", ".integration-steps .integration-step:nth-child(2) p"],
    ["integrations.step3Title", ".integration-steps .integration-step:nth-child(3) h3"],
    ["integrations.step3Lead", ".integration-steps .integration-step:nth-child(3) p"],
    ["integrations.simpleKicker", ".integration-simple-copy .scenario-kicker"],
    ["integrations.simpleTitle", ".integration-simple-copy h3"],
    ["integrations.simpleLead", ".integration-simple-copy p"],
    ["integrations.pipe1Title", ".integration-pipeline-step:nth-child(1) strong"],
    ["integrations.pipe1Lead", ".integration-pipeline-step:nth-child(1) p"],
    ["integrations.pipe2Title", ".integration-pipeline-step:nth-child(2) strong"],
    ["integrations.pipe2Lead", ".integration-pipeline-step:nth-child(2) p"],
    ["integrations.pipe3Title", ".integration-pipeline-step:nth-child(3) strong"],
    ["integrations.pipe3Lead", ".integration-pipeline-step:nth-child(3) p"],
    ["integrations.pipe4Title", ".integration-pipeline-step:nth-child(4) strong"],
    ["integrations.pipe4Lead", ".integration-pipeline-step:nth-child(4) p"],
    ["integrations.wordpressTitle", ".connector-board .connector-card:nth-child(1) h3"],
    ["integrations.wordpressLead", ".connector-board .connector-card:nth-child(1) p"],
    ["integrations.wooTitle", ".connector-board .connector-card:nth-child(2) h3"],
    ["integrations.wooLead", ".connector-board .connector-card:nth-child(2) p"],
    ["integrations.baselinkerTitle", ".connector-board .connector-card:nth-child(3) h3"],
    ["integrations.baselinkerLead", ".connector-board .connector-card:nth-child(3) p"],
    ["integrations.allegroTitle", ".connector-board .connector-card:nth-child(4) h3"],
    ["integrations.allegroLead", ".connector-board .connector-card:nth-child(4) p"],
    ["integrations.erpTitle", ".connector-board .connector-card:nth-child(5) h3"],
    ["integrations.erpLead", ".connector-board .connector-card:nth-child(5) p"],
    ["integrations.portalTitle", ".connector-board .connector-card:nth-child(6) h3"],
    ["integrations.portalLead", ".connector-board .connector-card:nth-child(6) p"],
    ["integrations.fastKicker", ".integration-faststart .scenario-kicker"],
    ["integrations.fastTitle", ".integration-faststart h3"],
    ["integrations.fastLead", ".integration-faststart p"],
    ["office.title", "#przyklady-biuro .section-head h2"],
    ["office.lead", "#przyklady-biuro .section-head p", "html"],
    ["offer.title", "#oferta .section-head h2"],
    ["offer.lead", "#oferta .section-head p"],
    ["offer.auditTitle", "#oferta .price-card:nth-child(1) h3"],
    ["offer.auditMeta", "#oferta .price-card:nth-child(1) .price span"],
    ["offer.auditCta", "#oferta .price-card:nth-child(1) .btn"],
    ["offer.pilotTitle", "#oferta .price-card:nth-child(2) h3"],
    ["offer.pilotMeta", "#oferta .price-card:nth-child(2) .price span"],
    ["offer.pilotCta", "#oferta .price-card:nth-child(2) .btn"],
    ["offer.careTitle", "#oferta .price-card:nth-child(3) h3"],
    ["offer.careMeta", "#oferta .price-card:nth-child(3) .price span"],
    ["offer.careCta", "#oferta .price-card:nth-child(3) .btn"],
    ["tech.title", "#tech .section-head h2"],
    ["tech.lead", "#tech .section-head p"],
    ["contact.title", "#kontakt .section-head h2"],
    ["contact.lead", "#kontakt .section-head p"],
    ["contact.mail", '#kontakt a[href^="mailto:"]'],
    ["contact.chat", '#kontakt a[href="chat.html"]'],
    ["contact.demo", '#kontakt a[href="demo.html"]'],
    ["faq.q1", ".faq-item:nth-child(1) .faq-q"],
    ["faq.a1", ".faq-item:nth-child(1) .faq-a-inner"],
    ["faq.q2", ".faq-item:nth-child(2) .faq-q"],
    ["faq.a2", ".faq-item:nth-child(2) .faq-a-inner"],
    ["faq.q3", ".faq-item:nth-child(3) .faq-q"],
    ["faq.a3", ".faq-item:nth-child(3) .faq-a-inner"],
    ["faq.q4", ".faq-item:nth-child(4) .faq-q"],
    ["faq.a4", ".faq-item:nth-child(4) .faq-a-inner"],
    ["faq.q5", ".faq-item:nth-child(5) .faq-q"],
    ["faq.a5", ".faq-item:nth-child(5) .faq-a-inner"],
    ["faq.q6", ".faq-item:nth-child(6) .faq-q"],
    ["faq.a6", ".faq-item:nth-child(6) .faq-a-inner"],
  ];

  const SLIDE_DURATION_MS = 5500;
  const STEPS = [
    {
      id: "prompt",
      title: "Jedna komenda zamiast ręcznego klejenia usług",
      caption: "Operator opisuje cel po polsku. Taskinity zamienia go na plan URI, artefakty i kontrolowany runtime.",
      build: buildSlidePrompt,
    },
    {
      id: "plan",
      title: "NL → plan URI",
      caption: "System rozbija prompt na kroki: generowanie agentów, rejestr deploymentów, start, inspect i supervisor.",
      build: buildSlidePlan,
    },
    {
      id: "agents",
      title: "3 agenci startują mimo zajętych portów",
      caption: "Preferowane porty są zajęte przez inne usługi, więc runtime wybiera wolne porty i zapisuje effective health URI.",
      build: buildSlideAgents,
    },
    {
      id: "failure",
      title: "Jeden agent pada",
      caption: "Proces user-agent zostaje zabity poza hypervisorem. State nadal wskazuje stary PID, więc inspect widzi stale runtime.",
      build: buildSlideFailure,
    },
    {
      id: "repair",
      title: "Supervisor naprawia w pętli",
      caption: "Inspect → klasyfikacja → restart na effective port → ponowny health/card. Po jednej próbie agent wraca do healthy.",
      build: buildSlideRepair,
    },
    {
      id: "proof",
      title: "Dowód: proces, health, card i logi są spójne",
      caption: "Ta sama prawda jest widoczna w Web UI, CLI, API i runtime state. To pozwala systemowi działać autonomicznie.",
      build: buildSlideProof,
    },
  ];
  const SCENARIOS = {
    agents: {
      title: "3 agenci wygenerowani i uruchomieni",
      summary: "Plan NL przechodzi przez generate, rejestr deploymentów i health-check dla każdego agenta.",
      lines: [
        { tone: "info", text: '$ urish ask "stwórz 3 agentów i uruchom lokalnie"' },
        { tone: "ok", text: "plan://run/agents accepted · policy=dry-run" },
        { tone: "ok", text: "generate weather-map-agent.local → agents/generated/weather_map_agent" },
        { tone: "ok", text: "generate user-agent.local → agents/generated/user_agent" },
        { tone: "ok", text: "generate invoices-agent.local → agents/generated/invoices_agent" },
        { tone: "ok", text: "health summary: 3/3 healthy" },
      ],
      metrics: [
        ["Agents", "3 generated"],
        ["Health", "3/3 OK"],
        ["Repair", "none"],
        ["State", "persisted"],
      ],
      focus: ["nl", "uri", "registry", "runtime", "proof"],
    },
    ports: {
      title: "Runtime wybiera port efektywny",
      summary: "Deklarowany port może być zajęty. System zapisuje realny health URI zamiast kończyć działanie błędem.",
      lines: [
        { tone: "info", text: "$ hypervisor run-agent weather-map-agent.local --port 8101" },
        { tone: "warn", text: "port :8101 busy · owner: previous service" },
        { tone: "ok", text: "selected effective port :8110" },
        { tone: "ok", text: "runtime_state.health_uri = http://localhost:8110/health" },
        { tone: "ok", text: "card://agent/weather-map-agent.local → healthy" },
      ],
      metrics: [
        ["Declared", ":8101"],
        ["Effective", ":8110"],
        ["Health URI", "synced"],
        ["Status", "healthy"],
      ],
      focus: ["uri", "registry", "runtime", "proof"],
    },
    repair: {
      title: "Awaria przechodzi przez repair loop",
      summary: "Supervisor rozróżnia proces running od service healthy, czyta state/logi i wykonuje ograniczoną naprawę.",
      lines: [
        { tone: "info", text: "$ hypervisor inspect-agent user-agent.local" },
        { tone: "bad", text: "RUNTIME_STATE_STALE · saved PID not alive" },
        { tone: "warn", text: "health failed on http://localhost:8118/health" },
        { tone: "info", text: "$ hypervisor supervise user-agent.local --repair auto --max-attempts 3" },
        { tone: "ok", text: "strategy restart_agent selected · safe mutation approved" },
        { tone: "ok", text: "verify health OK · card OK · logs clean · attempts=1" },
      ],
      metrics: [
        ["Before", "stale"],
        ["Strategy", "restart"],
        ["Attempts", "1/3"],
        ["After", "healthy"],
      ],
      focus: ["registry", "runtime", "repair", "proof"],
    },
    ecommerce: {
      title: "WooCommerce → Baselinker → ERP w jednym widoku",
      summary: "Webhook ze sklepu, sync magazynu i faktura w ERP — Taskinity rejestruje każdy krok i przy awarii pokazuje incident w chacie.",
      lines: [
        { tone: "info", text: "Woo webhook order.created → workflow://order/new" },
        { tone: "ok", text: "Baselinker getOrders · 12 new · shell://scripts/sync-baselinker.sh OK" },
        { tone: "ok", text: "invoices-agent.local → http://erp.local/api/invoices · 201 Created" },
        { tone: "warn", text: "Allegro OAuth token expires in 2h · refresh scheduled" },
        { tone: "bad", text: "ERP POST 503 · order #4521 stuck in processing" },
        { tone: "info", text: '$ urish ask "zdiagnozuj synchronizację Allegro i pokaż błędy ERP"' },
        { tone: "ok", text: "repair://agent/invoices-agent.local/diagnose · incident opened" },
      ],
      metrics: [
        ["Woo", "webhook OK"],
        ["Baselinker", "sync OK"],
        ["ERP", "503 retry"],
        ["Chat", "diagnose"],
      ],
      focus: ["nl", "uri", "registry", "repair"],
    },
    office: {
      title: "Dzień Marty — portal, faktury, bank, token Android",
      summary: "Biuro opisuje zadanie po polsku. System łączy WWW, ERP, bank online i telefon — zatrzymując się na 2FA i approve.",
      lines: [
        { tone: "info", text: '$ urish ask "pobierz raport VAT z portalu i zapisz w rozliczeniach"' },
        { tone: "ok", text: "browser://portal/vat-report → CSV saved · output/rozliczenia/" },
        { tone: "ok", text: "workflow://invoices/batch/dry-run → 8 PDF · waiting approval" },
        { tone: "info", text: 'Marta: "wyślij zatwierdzone"' },
        { tone: "ok", text: "invoices-agent.local → ERP + e-mail · 8/8 sent" },
        { tone: "warn", text: "workflow://bank/batch-transfer · STOP before 2FA" },
        { tone: "info", text: "android://device/pixel-7/screenshot → push shown in chat" },
        { tone: "ok", text: "Marta confirmed on phone · browser://bank/confirm OK" },
      ],
      metrics: [
        ["Portal", "CSV OK"],
        ["Faktury", "8 sent"],
        ["Bank", "2FA OK"],
        ["Audit", "logged"],
      ],
      focus: ["nl", "uri", "registry", "proof"],
    },
  };

  function storageGet(key) {
    try {
      return window.localStorage?.getItem(key) || "";
    } catch (err) {
      return "";
    }
  }

  function storageSet(key, value) {
    try {
      window.localStorage?.setItem(key, value);
    } catch (err) {
      // Preferences are progressive enhancement; ignore blocked storage.
    }
  }

  function normalizeChoice(value, allowed, fallback) {
    return allowed.includes(value) ? value : fallback;
  }

  let currentLang = normalizeChoice(storageGet(LANG_KEY) || document.documentElement.lang, LANGS, "en");
  let currentTheme = normalizeChoice(document.documentElement.dataset.theme || storageGet(THEME_KEY), THEMES, "dark");
  let currentStep = 0;
  let autoTimer = null;
  let paused = false;
  let progressRAF = null;
  let progressStart = 0;
  let scenarioTimers = [];

  const stageEl = document.getElementById("tour-slide-host");
  const captionTitle = document.getElementById("tour-caption-title");
  const captionText = document.getElementById("tour-caption-text");
  const progressBar = document.getElementById("tour-progress-bar");
  const countEl = document.getElementById("tour-count");
  const stepButtons = document.querySelectorAll(".tour-step-btn");
  const btnPrev = document.getElementById("tour-prev");
  const btnNext = document.getElementById("tour-next");
  const btnPlay = document.getElementById("tour-play");
  const btnCopyChat = document.getElementById("tour-copy-chat");
  const scenarioTabs = document.querySelectorAll(".scenario-tab");
  const scenarioTerminal = document.getElementById("scenario-terminal");
  const scenarioResult = document.getElementById("scenario-result");
  const scenarioReplay = document.getElementById("scenario-replay");
  const systemMapNodes = document.querySelectorAll(".system-map-node");

  function lookup(key) {
    const langCopy = TRANSLATIONS[currentLang] || TRANSLATIONS.en;
    const fallbackCopy = TRANSLATIONS.en;
    const read = (obj) => key.split(".").reduce((acc, part) => (acc && acc[part] !== undefined ? acc[part] : undefined), obj);
    return read(langCopy) ?? read(fallbackCopy) ?? "";
  }

  function getStepCopy(id) {
    const step = STEPS.find((item) => item.id === id);
    return {
      title: lookup(`steps.${id}.title`) || step?.title || "",
      caption: lookup(`steps.${id}.caption`) || step?.caption || "",
    };
  }

  function setNodeText(selector, value, mode) {
    const el = document.querySelector(selector);
    if (!el || value === undefined || value === "") return;
    if (mode === "html") {
      el.innerHTML = value;
      return;
    }
    if (mode === "mixedAfterStrong") {
      const strong = el.querySelector("strong");
      if (strong) el.innerHTML = `<strong>${escapeHtml(strong.textContent || "")}</strong> ${escapeHtml(value)}`;
      return;
    }
    el.textContent = value;
  }

  function applyTheme(theme) {
    currentTheme = normalizeChoice(theme, THEMES, "dark");
    document.documentElement.dataset.theme = currentTheme;
    storageSet(THEME_KEY, currentTheme);
    document.querySelectorAll("[data-theme-choice]").forEach((btn) => {
      const active = btn.getAttribute("data-theme-choice") === currentTheme;
      btn.classList.toggle("is-active", active);
      btn.setAttribute("aria-pressed", active ? "true" : "false");
    });
  }

  function updatePlayButton() {
    if (!btnPlay) return;
    btnPlay.textContent = paused ? lookup("controls.play") : lookup("controls.pause");
    btnPlay.dataset.state = paused ? "paused" : "playing";
    btnPlay.setAttribute("aria-pressed", paused ? "true" : "false");
  }

  function applyLanguage(lang) {
    currentLang = normalizeChoice(lang, LANGS, "en");
    document.documentElement.lang = currentLang;
    storageSet(LANG_KEY, currentLang);
    const copy = TRANSLATIONS[currentLang] || TRANSLATIONS.en;
    document.title = copy.title || TRANSLATIONS.en.title;
    const meta = document.querySelector('meta[name="description"]');
    if (meta) meta.setAttribute("content", copy.metaDescription || TRANSLATIONS.en.metaDescription);

    TEXT_BINDINGS.forEach(([key, selector, mode]) => setNodeText(selector, lookup(key), mode));
    document.querySelectorAll("[data-lang-choice]").forEach((btn) => {
      const active = btn.getAttribute("data-lang-choice") === currentLang;
      btn.classList.toggle("is-active", active);
      btn.setAttribute("aria-pressed", active ? "true" : "false");
    });
    document.querySelectorAll(".tour-step-btn").forEach((btn, index) => {
      const label = lookup("tour.steps")?.[index];
      const labelEl = btn.querySelector(".tour-step-label");
      if (labelEl && label) labelEl.textContent = label;
    });
    document.querySelectorAll(".scenario-tab").forEach((btn, index) => {
      const label = lookup("tour.tabs")?.[index];
      if (label) btn.textContent = label;
    });
    if (btnPrev) btnPrev.textContent = lookup("controls.prev");
    if (btnNext) btnNext.textContent = lookup("controls.next");
    if (btnCopyChat) btnCopyChat.textContent = lookup("controls.copyChat");
    updatePlayButton();

    const activeScenario = document.querySelector(".scenario-tab.is-active")?.getAttribute("data-scenario") || "agents";
    if (scenarioTerminal && scenarioResult) renderScenario(activeScenario, { animate: false });
    if (stageEl?.children.length) renderStep(currentStep);
    window.TaskinityOfficeCards?.apply(currentLang);
  }

  function initPreferences() {
    applyTheme(currentTheme);
    document.querySelectorAll("[data-theme-choice]").forEach((btn) => {
      btn.addEventListener("click", () => applyTheme(btn.getAttribute("data-theme-choice") || "dark"));
    });
    document.querySelectorAll("[data-lang-choice]").forEach((btn) => {
      btn.addEventListener("click", () => applyLanguage(btn.getAttribute("data-lang-choice") || "en"));
    });
    applyLanguage(currentLang);
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function buildSlidePrompt(container) {
    container.innerHTML = `
      <div class="demo-command">
        <div class="demo-command-bar">
          <span class="live-dot"></span>
          <span>urish ask</span>
        </div>
        <p>„Wygeneruj 3 agentów: pogodę, użytkowników i faktury. Uruchom lokalnie, sprawdź health i napraw automatycznie, jeśli któryś padnie.”</p>
      </div>
      <div class="flow-diagram flow-diagram-wide" aria-hidden="true">
        <div class="flow-node info" style="animation-delay:0.1s">NL prompt</div>
        <span class="flow-arrow" style="animation-delay:0.2s">→</span>
        <div class="flow-node ok" style="animation-delay:0.3s">plan URI</div>
        <span class="flow-arrow" style="animation-delay:0.4s">→</span>
        <div class="flow-node ok" style="animation-delay:0.5s">generate</div>
        <span class="flow-arrow" style="animation-delay:0.6s">→</span>
        <div class="flow-node ok" style="animation-delay:0.7s">supervise</div>
      </div>
      <div class="demo-note">
        <span class="dot ok"></span>
        <div>
          Użytkownik nie musi znać <code>uvicorn</code>, PID-ów ani portów. System zachowuje artefakty, URI i runtime state.
        </div>
      </div>`;
  }

  function mockShell(activeId, messagesHtml, inputText) {
    const processes = [
      { id: "weather", name: "weather-map-agent", status: "ok", label: "healthy · :8110" },
      { id: "user", name: "user-agent", status: activeId === "user-bad" ? "bad" : "ok", label: activeId === "user-bad" ? "stale · PID dead" : "healthy · :8118" },
      { id: "invoices", name: "invoices-agent", status: "ok", label: "healthy · :8122" },
    ];
    const sidebar = processes
      .map(
        (p) => `
      <div class="mock-process${p.id === activeId ? " is-highlight" : ""}">
        <div class="name">${escapeHtml(p.name)}</div>
        <div class="status ${p.status}">${escapeHtml(p.label)}</div>
      </div>`
      )
      .join("");

    return `
      <div class="mock-layout">
        <div class="mock-sidebar">
          <h4>Agenci</h4>
          ${sidebar}
        </div>
        <div class="mock-chat">
          <div class="mock-messages">${messagesHtml}</div>
          <div class="mock-input">
            <span class="${inputText ? "typing-cursor" : ""}">${escapeHtml(inputText || "Napisz pytanie…")}</span>
          </div>
        </div>
      </div>`;
  }

  function buildSlidePlan(container) {
    const html = mockShell(
      "weather",
      `<div class="mock-msg user" style="animation-delay:0.1s">
        <div class="label">Ty</div>
        Wygeneruj 3 agentów, uruchom, sprawdź health i napraw awarię.
      </div>
      <div class="mock-msg bot" style="animation-delay:0.3s">
        <div class="label">Taskinity</div>
        Plan:
        <ol>
          <li><code>urigen generate</code> dla 3 kontraktów</li>
          <li><code>hypervisor run-agent</code> z dynamicznym portem</li>
          <li><code>inspect-agent</code> health/card/logs</li>
          <li><code>supervise --repair auto</code> przy awarii</li>
        </ol>
      </div>`,
      ""
    );
    container.innerHTML = html;
  }

  function buildSlideAgents(container) {
    container.innerHTML = `
      <div class="agent-run-grid">
        ${agentRunCard("weather-map-agent", "8101", "8110", "healthy", "0.1s")}
        ${agentRunCard("user-agent", "8102", "8118", "healthy", "0.25s")}
        ${agentRunCard("invoices-agent", "8103", "8122", "healthy", "0.4s")}
      </div>
      <div class="repair-timeline compact" aria-label="Start agentów">
        <div class="repair-event is-done" style="animation-delay:0.1s"><strong>generate</strong><span>pliki agentów</span></div>
        <div class="repair-event is-done" style="animation-delay:0.25s"><strong>port check</strong><span>8101/8102/8103 zajęte</span></div>
        <div class="repair-event is-done" style="animation-delay:0.4s"><strong>rebind</strong><span>8110/8118/8122</span></div>
        <div class="repair-event is-done" style="animation-delay:0.55s"><strong>health</strong><span>3 healthy</span></div>
      </div>`;
  }

  function agentRunCard(name, declared, effective, state, delay) {
    return `
      <div class="agent-run-card ${state}" style="animation-delay:${delay}">
        <div class="agent-run-top">
          <span class="dot ok"></span>
          <strong>${escapeHtml(name)}</strong>
        </div>
        <div class="agent-run-port">
          <span>declared</span><code>:${escapeHtml(declared)}</code>
          <i>→</i>
          <span>effective</span><code>:${escapeHtml(effective)}</code>
        </div>
        <div class="agent-run-status">health OK · card OK · logs clean</div>
      </div>`;
  }

  function buildSlideFailure(container) {
    container.innerHTML = mockShell(
      "user-bad",
      `<div class="mock-msg bot" style="animation-delay:0.1s">
        <div class="label">Taskinity</div>
        Wykryto awarię:
        <code>readiness://agent/user-agent.local</code>
        <ul>
          <li><strong style="color:#fb7185">RUNTIME_STATE_STALE</strong></li>
          <li>PID zapisany w state nie żyje</li>
          <li>Health/card na <code>:8118</code> nie odpowiada</li>
          <li>Rekomendacja: <code>restart</code></li>
        </ul>
      </div>`,
      ""
    );
  }

  function buildSlideRepair(container) {
    container.innerHTML = `
      <div class="repair-loop" aria-label="Pętla naprawcza">
        <div class="repair-event is-bad" style="animation-delay:0.1s">
          <strong>inspect</strong><span>stale runtime · health failed</span>
        </div>
        <div class="repair-event is-warn" style="animation-delay:0.25s">
          <strong>classify</strong><span>safe repair: restart_agent</span>
        </div>
        <div class="repair-event is-info" style="animation-delay:0.4s">
          <strong>apply</strong><span>start na effective :8118</span>
        </div>
        <div class="repair-event is-done" style="animation-delay:0.55s">
          <strong>verify</strong><span>health OK · card OK · PID nowy</span>
        </div>
      </div>
      <div class="repair-result">
        <div>
          <span>before</span>
          <strong class="bad-text">stale</strong>
        </div>
        <i></i>
        <div>
          <span>attempts</span>
          <strong>1</strong>
        </div>
        <i></i>
        <div>
          <span>after</span>
          <strong class="ok-text">healthy</strong>
        </div>
      </div>
      <pre class="demo-code">hypervisor supervise user-agent.local --repair auto --max-attempts 3
→ strategy: restart
→ port: 8118
→ result: healthy</pre>`;
  }

  function buildSlideProof(container) {
    const items = [
      "Chat layer",
      "Web API",
      "CLI",
      "Runtime",
      "Health",
      "Agent card",
      "Logs",
      "Policy gate",
      "Repair loop",
    ];
    container.innerHTML = `
      <p class="proof-lead">Ten sam agent w każdej warstwie — <code>agent://user-agent</code></p>
      <div class="proof-grid">
        ${items
          .map(
            (label, i) => `
          <div class="proof-item" style="animation-delay:${(i * 0.08).toFixed(2)}s">
            <span>${escapeHtml(label)}</span>
            <span class="ok-badge">OK</span>
          </div>`
          )
          .join("")}
      </div>
      <pre class="demo-code">$ hypervisor inspect-agent user-agent.local
process: running
health:  ok
card:    ok
repair:  none</pre>`;
  }

  function copyTourChat() {
    const slide = stageEl?.querySelector(".tour-slide");
    const messages = slide?.querySelectorAll(".mock-msg");
    if (!messages?.length) {
      flashTourCopy(lookup("controls.noChat"));
      return;
    }
    const lines = ["# Taskinity — demo chat", ""];
    messages.forEach((msg) => {
      const label = msg.querySelector(".label")?.textContent?.trim() || "Wiadomość";
      const clone = msg.cloneNode(true);
      clone.querySelector(".label")?.remove();
      lines.push(`## ${label}`);
      lines.push("");
      lines.push((clone.textContent || "").trim());
      lines.push("");
    });
    const text = lines.join("\n").trim();
    if (navigator.clipboard?.writeText) {
      navigator.clipboard.writeText(text).then(() => flashTourCopy()).catch(() => flashTourCopy(lookup("controls.error")));
      return;
    }
    flashTourCopy(lookup("controls.noClipboard"));
  }

  function flashTourCopy(label = lookup("controls.copied")) {
    if (!btnCopyChat) return;
    const original = btnCopyChat.textContent;
    btnCopyChat.textContent = label;
    window.setTimeout(() => {
      btnCopyChat.textContent = original;
    }, 1400);
  }

  function clearScenarioTimers() {
    scenarioTimers.forEach((timer) => window.clearTimeout(timer));
    scenarioTimers = [];
  }

  function getScenario(id) {
    return SCENARIOS[id] || SCENARIOS.agents;
  }

  function renderScenarioResult(scenario) {
    if (!scenarioResult) return;
    scenarioResult.innerHTML = `
      <div class="scenario-result-head">
        <span class="live-dot"></span>
        <div>
          <strong>${escapeHtml(scenario.title)}</strong>
          <p>${escapeHtml(scenario.summary)}</p>
        </div>
      </div>
      <div class="scenario-metrics">
        ${scenario.metrics
          .map(
            ([label, value]) => `
          <div class="scenario-metric">
            <span>${escapeHtml(label)}</span>
            <strong>${escapeHtml(value)}</strong>
          </div>`
          )
          .join("")}
      </div>`;
  }

  function setSystemMapFocus(focus = []) {
    if (!systemMapNodes.length) return;
    const active = new Set(focus);
    systemMapNodes.forEach((node) => {
      const key = node.getAttribute("data-map-node") || "";
      node.classList.toggle("is-active", active.has(key));
    });
  }

  function appendScenarioLine(line, index) {
    if (!scenarioTerminal) return;
    const row = document.createElement("div");
    row.className = `terminal-line is-${line.tone || "info"}`;
    row.style.animationDelay = `${Math.min(index * 0.04, 0.2)}s`;
    row.innerHTML = `<span class="terminal-caret">›</span><span>${escapeHtml(line.text)}</span>`;
    scenarioTerminal.appendChild(row);
  }

  function renderScenario(id, options = {}) {
    if (!scenarioTerminal || !scenarioResult) return;
    const scenario = getScenario(id);
    const animate = options.animate !== false && !window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;
    clearScenarioTimers();
    scenarioTerminal.innerHTML = "";
    renderScenarioResult(scenario);
    setSystemMapFocus(scenario.focus);

    scenario.lines.forEach((line, index) => {
      if (!animate) {
        appendScenarioLine(line, index);
        return;
      }
      const timer = window.setTimeout(() => appendScenarioLine(line, index), index * 260);
      scenarioTimers.push(timer);
    });
  }

  function initScenarioLab() {
    if (!scenarioTerminal || !scenarioResult || !scenarioTabs.length) return;
    scenarioTabs.forEach((tab) => {
      tab.addEventListener("click", () => {
        const id = tab.getAttribute("data-scenario") || "agents";
        scenarioTabs.forEach((item) => {
          const selected = item === tab;
          item.classList.toggle("is-active", selected);
          item.setAttribute("aria-selected", selected ? "true" : "false");
        });
        renderScenario(id);
      });
    });

    scenarioReplay?.addEventListener("click", () => {
      const active = document.querySelector(".scenario-tab.is-active")?.getAttribute("data-scenario") || "agents";
      renderScenario(active);
    });

    renderScenario("agents", { animate: false });
  }

  function renderStep(index) {
    const step = STEPS[index];
    if (!step || !stageEl) return;
    const stepCopy = getStepCopy(step.id);

    currentStep = index;
    stageEl.innerHTML = "";
    const slide = document.createElement("div");
    slide.className = "tour-slide is-active";
    slide.id = `slide-${step.id}`;
    stageEl.appendChild(slide);
    step.build(slide);

    if (captionTitle) captionTitle.textContent = stepCopy.title;
    if (captionText) captionText.textContent = stepCopy.caption;
    if (countEl) countEl.textContent = `${index + 1} / ${STEPS.length}`;

    stepButtons.forEach((btn, i) => {
      btn.classList.toggle("is-active", i === index);
      btn.setAttribute("aria-current", i === index ? "step" : "false");
    });

    resetProgress();
  }

  function resetProgress() {
    if (!progressBar) return;
    progressStart = performance.now();
    if (progressRAF) cancelAnimationFrame(progressRAF);
    function tick(now) {
      if (paused) {
        progressRAF = requestAnimationFrame(tick);
        return;
      }
      const elapsed = now - progressStart;
      const pct = Math.min(100, (elapsed / SLIDE_DURATION_MS) * 100);
      progressBar.style.width = `${pct}%`;
      if (pct < 100) progressRAF = requestAnimationFrame(tick);
    }
    progressRAF = requestAnimationFrame(tick);
  }

  function stopAuto() {
    if (autoTimer) {
      clearInterval(autoTimer);
      autoTimer = null;
    }
  }

  function startAuto() {
    stopAuto();
    if (paused) return;
    autoTimer = setInterval(() => {
      goToStep((currentStep + 1) % STEPS.length);
    }, SLIDE_DURATION_MS);
  }

  function goToStep(index) {
    renderStep(index);
    if (!paused) startAuto();
  }

  function pauseTourPlayback() {
    paused = true;
    updatePlayButton();
    stopAuto();
  }

  function bindTourStepButtons() {
    stepButtons.forEach((btn, i) => {
      btn.addEventListener("click", () => {
        pauseTourPlayback();
        goToStep(i);
      });
    });
  }

  function bindTourNavButtons() {
    btnPrev?.addEventListener("click", () => {
      pauseTourPlayback();
      goToStep((currentStep - 1 + STEPS.length) % STEPS.length);
    });
    btnNext?.addEventListener("click", () => {
      pauseTourPlayback();
      goToStep((currentStep + 1) % STEPS.length);
    });
  }

  function bindTourPlayButton() {
    btnPlay?.addEventListener("click", () => {
      paused = !paused;
      updatePlayButton();
      if (paused) {
        stopAuto();
        return;
      }
      resetProgress();
      startAuto();
    });
  }

  function bindTourHoverPause() {
    const tourSection = document.getElementById("tour");
    tourSection?.addEventListener("mouseenter", () => {
      paused = true;
      stopAuto();
    });
    tourSection?.addEventListener("mouseleave", () => {
      if (btnPlay?.dataset.state === "playing") {
        paused = false;
        resetProgress();
        startAuto();
      }
    });
  }

  function initTour() {
    if (!stageEl) return;
    bindTourStepButtons();
    bindTourNavButtons();
    bindTourPlayButton();
    btnCopyChat?.addEventListener("click", copyTourChat);
    bindTourHoverPause();
    renderStep(0);
    startAuto();
  }

  function initReveal() {
    const els = document.querySelectorAll(".reveal");
    if (!els.length || !("IntersectionObserver" in window)) {
      els.forEach((el) => el.classList.add("is-visible"));
      return;
    }
    let done = false;
    let failSafeTimer = null;
    const revealAll = () => {
      if (done) return;
      done = true;
      els.forEach((el) => el.classList.add("is-visible"));
      obs.disconnect();
      if (failSafeTimer) window.clearTimeout(failSafeTimer);
    };
    const obs = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add("is-visible");
            obs.unobserve(e.target);
          }
        });
        if (Array.from(els).every((el) => el.classList.contains("is-visible"))) {
          revealAll();
        }
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    els.forEach((el) => obs.observe(el));
    failSafeTimer = window.setTimeout(revealAll, 1800);
  }

  function initFaq() {
    document.querySelectorAll(".faq-item").forEach((item) => {
      const btn = item.querySelector(".faq-q");
      btn?.addEventListener("click", () => {
        const open = item.classList.contains("is-open");
        document.querySelectorAll(".faq-item.is-open").forEach((o) => o.classList.remove("is-open"));
        if (!open) item.classList.add("is-open");
      });
    });
  }

  function initSmoothAnchors() {
    document.querySelectorAll('a[href^="#"]').forEach((a) => {
      a.addEventListener("click", (e) => {
        const id = a.getAttribute("href");
        if (!id || id === "#") return;
        const target = document.querySelector(id);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: "smooth", block: "start" });
        }
      });
    });
  }

  function initOfficeCards() {
    document.querySelectorAll(".office-use-card").forEach((card) => {
      card.classList.add("office-use-card--clickable");
      card.addEventListener("click", () => {
        const quote = card.querySelector(".office-chat-quote")?.textContent?.trim();
        if (!quote) return;
        const prompt = quote.replace(/^[„""']+|[„""']+$/g, "").trim();
        storageSet("taskinity.chatPrompt", prompt);
        window.location.href = "chat.html";
      });
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    initPreferences();
    initTour();
    initScenarioLab();
    initReveal();
    initFaq();
    initSmoothAnchors();
    initOfficeCards();
  });
})();
