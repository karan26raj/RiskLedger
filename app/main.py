from enum import Enum
from typing import Annotated

from fastapi import FastAPI, HTTPException, Path

app = FastAPI(title="RiskLedger API", version="0.1.0")

TIERS: tuple[str, ...] = ("critical", "high", "medium", "low")

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


class Scanner(str, Enum):
    NESSUS = "nessus"
    QUALYS = "qualys"
    OPENVAS = "openvas"


SCANNERS: dict[Scanner, dict] = {
    Scanner.NESSUS: {
        "scanner": "nessus",
        "display_name": "Tenable Nessus",
        "severity_scale": "cvss_v3",
    },
    Scanner.QUALYS: {
        "scanner": "qualys",
        "display_name": "Qualys VMDR",
        "severity_scale": "cvss_v3",
    },
    Scanner.OPENVAS: {
        "scanner": "openvas",
        "display_name": "OpenVAS",
        "severity_scale": "cvss_v3",
    },
}


def summarize_vendors(vendors: list[dict]) -> dict:
    by_tier = {tier: 0 for tier in TIERS}
    for vendor in vendors:
        by_tier[vendor["tier"]] += 1
    active = sum(1 for vendor in vendors if vendor["status"] == "active")
    return {"total": len(vendors), "by_tier": by_tier, "active": active}


def open_findings_by_cvss(findings: list[dict]) -> list[dict]:
    open_findings = [f for f in findings if f["status"] == "open"]
    return sorted(open_findings, key=lambda f: f["cvss"], reverse=True)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "riskledger", "version": app.version}


@app.get("/vendors")
def list_vendors() -> list[dict]:
    return VENDORS


@app.get("/vendors/summary")
def vendors_summary() -> dict:
    return summarize_vendors(VENDORS)


@app.get("/findings")
def list_findings() -> list[dict]:
    return FINDINGS


@app.get("/findings/open")
def list_open_findings() -> list[dict]:
    return open_findings_by_cvss(FINDINGS)


@app.get("/vendors/{vendor_id}")
def get_vendor(vendor_id: Annotated[int, Path(ge=1)]) -> dict | None:
    for vendor in VENDORS:
        if vendor_id == vendor["id"]:
            return vendor

    raise HTTPException(status_code=404, detail=f"Vendor {vendor_id} not found")


@app.get("/findings/{finding_id}")
def get_findings(finding_id: Annotated[int, Path(ge=1)]) -> dict | None:
    for finding in FINDINGS:
        if finding_id == finding["id"]:
            return finding
    raise HTTPException(status_code=404, detail=f"ID {finding_id} doesn't exist")


@app.get("/vendors/{vendor_id}/findings")
def vendor_findings(vendor_id: Annotated[int, Path(ge=1)]) -> list[dict]:
    if not any(vendor["id"] == vendor_id for vendor in VENDORS):
        raise HTTPException(status_code=404, detail=f"Vendor {vendor_id} not found")

    return [finding for finding in FINDINGS if finding["vendor_id"] == vendor_id]


@app.get("/vendors/{vendor_id}/findings/{finding_id}")
def get_vendor_finding(
    vendor_id: Annotated[int, Path(ge=1)], finding_id: Annotated[int, Path(ge=1)]
) -> dict:
    if not any(vendor["id"] == vendor_id for vendor in VENDORS):
        raise HTTPException(status_code=404, detail=f"Vendor {vendor_id} not found")

    for finding in FINDINGS:
        if finding["id"] == finding_id and finding["vendor_id"] == vendor_id:
            return finding
    raise HTTPException(
        status_code=404,
        detail=f"Finding {finding_id} not found for vendor {vendor_id}",
    )


@app.get("/scanners/{scanner}")
def get_scanner(scanner: Scanner) -> dict:
    return SCANNERS[scanner]
