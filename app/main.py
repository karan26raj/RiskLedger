from fastapi import FastAPI

app = FastAPI(title="RiskLedger API", version="0.1.0")

VENDORS: list[dict] = [
    {
        "id": 1,
        "name": "Acme Payroll",
        "domain": "acmepayroll.com",
        "tier": "critical",
        "status": "active",
    },
    {
        "id": 2,
        "name": "CloudNote",
        "domain": "cloudnote.io",
        "tier": "medium",
        "status": "offboarded",
    },
    {
        "id": 3,
        "name": "Northwind Logistics",
        "domain": "northwind.example",
        "tier": "high",
        "status": "active",
    },
    {
        "id": 4,
        "name": "Brightdesk",
        "domain": "brightdesk.example",
        "tier": "low",
        "status": "active",
    },
]

FINDINGS: list[dict] = [
    {
        "id": 1,
        "vendor_id": 1,
        "title": "Outdated TLS configuration",
        "cvss": 7.4,
        "severity": "high",
        "status": "open",
    },
    {
        "id": 2,
        "vendor_id": 1,
        "title": "Exposed admin panel",
        "cvss": 9.1,
        "severity": "critical",
        "status": "open",
    },
    {
        "id": 3,
        "vendor_id": 2,
        "title": "Missing security headers",
        "cvss": 4.3,
        "severity": "medium",
        "status": "resolved",
    },
    {
        "id": 4,
        "vendor_id": 3,
        "title": "Verbose error messages",
        "cvss": 2.1,
        "severity": "low",
        "status": "open",
    },
    {
        "id": 5,
        "vendor_id": 4,
        "title": "Weak password policy",
        "cvss": 6.5,
        "severity": "medium",
        "status": "resolved",
    },
]


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "riskledger", "version": app.version}


@app.get("/vendors")
def list_vendors() -> list[dict]:
    return VENDORS


@app.get("/findings")
def list_findings() -> list[dict]:
    return FINDINGS


@app.get("/findings/open")
def count_open_findings() -> dict:
    open_count = sum(1 for finding in FINDINGS if finding["status"] == "open")
    return {"open": open_count}


TIERS = ("critical", "high", "medium", "low")


@app.get("/vendors/summary")
def vendors_summary() -> dict:
    by_tier = {}
    for tier in TIERS:
        by_tier[tier] = 0

    active = 0
    for vendor in VENDORS:
        by_tier[vendor["tier"]] = by_tier.get(vendor["tier"], 0) + 1
        if vendor["status"] == "active":
            active += 1

    return {"total": len(VENDORS), "by_tier": by_tier, "active": active}
