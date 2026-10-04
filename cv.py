#!/usr/bin/env python3
"""Builds role-specific one-page CVs (HTML -> PDF via headless Chrome). Run: python3 cv.py"""
import html, os, subprocess, shutil
e = html.escape
PORTFOLIO = "portfolio.khalilrezgui0.workers.dev"
HEADER = ["Tunis, Tunisia (UTC+1)", "+216 92 428 859", "khalilrezgui0@gmail.com", "linkedin.com/in/khalil-rezgui", "github.com/khalilrez"]
SUB = "Italian citizen: EU work authorization, no sponsorship needed · Remote since 2024 with a Paris-based team"

EXP = {  # (role, dates, bullets) per variant; bullets ordered by relevance
 "sre": [
  ("Technical Project Lead", "Jan 2026 – Present", [
   "Own reliability and delivery for 5+ production data workstreams (CRM, tracking, monitoring, attribution, identity resolution), coordinating priorities and deadlines for the team.",
   "Led a company-wide infrastructure and FinOps redesign across GCP, BigQuery, MySQL, ClickHouse, Hetzner and Scaleway; defined a “cost per million events” KPI and a roadmap to absorb ~20x ingestion growth.",
   "Built SQL/ClickHouse post-production validation that catches event-volume anomalies and identifier gaps before customers are affected.",
   "Directed failure-mode benchmarks of ingestion architectures (direct ClickHouse, managed queues, HA Nomad) under a 20x load scenario.",
  ]),
  ("DataOps & Site Reliability Engineer", "Jan 2024 – Jan 2026", [
   "Carried on-call and overnight pager duty; resolved live incidents (MySQL crashes, pipeline bugs) by rollback or in-incident debugging while sustaining 99.9% uptime on GCP and HashiCorp Nomad.",
   "Built the observability and alerting stack (Fluentd, Elasticsearch, Graylog, Grafana, Prometheus) across 100+ daily jobs, cutting mean time to resolution by 65%.",
   "Migrated critical data from MySQL to ClickHouse with zero downtime (blue-green): 100x faster queries on 10M+ records.",
   "Led a team optimizing GCP infrastructure for a 50% cost reduction.",
   "Turned recurring failures into alerts, runbooks and recovery workflows (restart, rollback, database recovery, post-recovery validation).",
  ]),
 ],
 "data": [
  ("Technical Project Lead", "Jan 2026 – Present", [
   "Led a data architecture and FinOps redesign across GCP, BigQuery, MySQL, ClickHouse, Hetzner and Scaleway; built a cost model and a roadmap to absorb ~20x ingestion growth without proportional cost.",
   "Benchmarked ingestion and storage options (direct ClickHouse, managed queues, HA Nomad, optimized MySQL, DuckLake/Parquet on object storage) on throughput, CPU/RAM, storage footprint and projected cost.",
   "Defined 4+ data-quality KPIs (identifiable and identified sessions, hard candidate and identification rates) and compared BFS and DSU engines across 2-day to 7-month windows to validate an identity-resolution system.",
   "Built SQL/ClickHouse monitoring for event volumes, identifier coverage and source consistency; own 5+ production data workstreams.",
  ]),
  ("DataOps & Site Reliability Engineer", "Jan 2024 – Jan 2026", [
   "Migrated critical analytics from MySQL to a ClickHouse cluster with zero downtime: 100x faster queries and real-time diagnostics on 10M+ records.",
   "Built a server-side event collection pipeline in Go (Docker, Nomad) routing events to multiple destinations such as Meta and Google Ads.",
   "Built the observability stack (Fluentd, Elasticsearch, Graylog, Grafana, Prometheus) across 100+ daily jobs, cutting MTTR by 65%; 99.9% uptime on GCP and Nomad.",
   "Shipped a Python AI agent to production with 85% prediction accuracy.",
   "Led a team optimizing GCP data infrastructure for a 50% cost reduction.",
  ]),
 ],
 "gcp": [
  ("Technical Project Lead", "Jan 2026 – Present", [
   "Led a company-wide cloud cost and architecture redesign across GCP, BigQuery, MySQL, ClickHouse, Hetzner and Scaleway; defined a “cost per million events” KPI separating traffic-driven, fixed and mixed costs.",
   "Designed the target architecture and roadmap to absorb ~20x ingestion growth without linear cost increase, after benchmarking managed queues, serverless pipelines and self-hosted HA clusters.",
   "Built SQL/ClickHouse monitoring that flags anomalous event volumes and cost or usage patterns; own 5+ production data workstreams.",
  ]),
  ("DataOps & Site Reliability Engineer", "Jan 2024 – Jan 2026", [
   "Led a GCP optimization initiative for a 50% cost reduction: removed obsolete and cost-heavy services (Pub/Sub, Cloud Run, Cloud Functions, BigQuery) and rewrote hot production paths in Go to cut memory use.",
   "Operated production on GCP and HashiCorp Nomad at 99.9% uptime, including on-call and overnight pager duty.",
   "Built the observability stack (Cloud Monitoring, Prometheus, Grafana, Fluentd, Graylog) across 100+ daily jobs, cutting MTTR by 65%.",
   "Migrated MySQL workloads to ClickHouse with zero downtime: 100x faster queries on 10M+ records.",
   "Shipped a Python AI agent to production with 85% prediction accuracy.",
  ]),
 ],
 "go": [
  ("Technical Project Lead", "Jan 2026 – Present", [
   "Own reliability and delivery for 5+ production data workstreams, coordinating priorities and deadlines for the team.",
   "Led an infrastructure redesign and benchmark programme (direct ClickHouse ingestion, queues, HA Nomad clusters) under a 20x load scenario; defined a “cost per million events” KPI.",
   "Built SQL/ClickHouse validation that catches event-volume anomalies and identifier gaps before customer impact.",
  ]),
  ("DataOps & Site Reliability Engineer", "Jan 2024 – Jan 2026", [
   "Built a server-side event collection service in Go, containerized and run on HashiCorp Nomad, that processes analytics events and routes them to multiple destinations (Meta, Google Ads).",
   "Rewrote hot production paths in Go to cut memory use, contributing to a 50% GCP cost reduction.",
   "Built custom Go-based ETL on Nomad; sustained 99.9% uptime including on-call and overnight pager duty.",
   "Built observability (Fluentd, Elasticsearch, Graylog, Grafana, Prometheus) across 100+ daily jobs, cutting MTTR by 65%.",
   "Migrated MySQL to ClickHouse with zero downtime: 100x faster queries on 10M+ records.",
  ]),
 ],
}

PROJ = {
 "sre": [("Production Incident Detection & Recovery (2025)", "Centralized monitoring across infrastructure, application and data-quality signals, with restart, rollback and database-recovery runbooks. Introduced the company's first dedicated on-call platform."),
         ("Enterprise CI/CD Pipeline (2023)", "Jenkins, SonarQube and Git for a Spring Boot/Angular app: 1-hour manual release to 15-minute automated deploys, 85% coverage.")],
 "data": [("Customer Identity Resolution & Graph Validation (2026)", "KPI framework and engine comparison (BFS vs DSU) validating event-to-profile matching over 2-day, 30-day, 60-day and 7-month windows."),
          ("Multi-Agent AI Orchestrator (2025)", "Built from scratch to answer complex Shopify analytics queries, with OpenTelemetry tracing end to end.")],
 "gcp": [("Cost per Million Events Model (2026)", "Cost model splitting traffic-driven and fixed spend across GCP, BigQuery, ClickHouse, MySQL and bare-metal providers; turned the monthly invoice into an engineering metric."),
         ("Multi-Agent AI Orchestrator (2025)", "Built from scratch to answer complex Shopify analytics queries, with OpenTelemetry tracing end to end.")],
 "go": [("Server-Side Tracking Service, Go (2024)", "Event collector and router on Nomad feeding Meta and Google Ads; basis of the company's attribution pipeline."),
        ("Open source: debug-practice-go, pulse-sre", "Go alerting utilities and queue packages with tests and a written debug report (github.com/khalilrez).")],
}

SKILLS = {
 "sre":  [("Reliability","On-call · Incident response · Runbooks · Rollback & recovery · Alerting · MTTR reduction"),
          ("Observability","Prometheus · Grafana · Graylog · Fluentd · Elasticsearch · OpenTelemetry"),
          ("Cloud & infra","GCP · Azure · Docker · Kubernetes · HashiCorp Nomad · Ansible · CI/CD (Jenkins, GitHub Actions)"),
          ("Data","ClickHouse · MySQL · PostgreSQL · BigQuery · DuckDB · Message queues"),
          ("Code","Go · Python · SQL · Bash · Rust · JavaScript · Java")],
 "data": [("Data stores","ClickHouse · BigQuery · MySQL · PostgreSQL · DuckDB/DuckLake · Parquet & object storage"),
          ("Pipelines","ETL · Message queues · Pub/Sub · Server-side event ingestion · Data quality & validation"),
          ("Code","SQL · Python · Go · Bash · Rust"),
          ("Cloud & infra","GCP · Docker · Kubernetes · HashiCorp Nomad · Ansible · CI/CD"),
          ("Observability","Grafana · Prometheus · Graylog · Fluentd · Elasticsearch · OpenTelemetry")],
 "gcp":  [("Google Cloud","Pub/Sub · Cloud Run · Cloud Functions · BigQuery · IAM · Cloud Monitoring & Logging · Cloud DNS"),
          ("Cost & architecture","FinOps · Cost modelling · Capacity planning · Benchmarking · Multi-cloud (Hetzner, Scaleway, Azure)"),
          ("Infra","Docker · Kubernetes · HashiCorp Nomad · Ansible · CI/CD (Jenkins, GitHub Actions)"),
          ("Reliability","On-call · Prometheus · Grafana · Graylog · Fluentd · Elasticsearch"),
          ("Code & data","Go · Python · SQL · Bash · ClickHouse · BigQuery · MySQL")],
 "go":   [("Languages","Go · Python · SQL · Bash · Rust · JavaScript · Java"),
          ("Backend","Event-driven services · Message queues · ETL · REST · Testing & TDD · Microservices"),
          ("Infra","Docker · HashiCorp Nomad · Kubernetes · GCP · Ansible · CI/CD (Jenkins, GitHub Actions)"),
          ("Data","ClickHouse · MySQL · PostgreSQL · BigQuery"),
          ("Observability","Prometheus · Grafana · Graylog · Fluentd · OpenTelemetry")],
}

VARIANTS = {
 "sre":  ("Site Reliability & Platform Engineer","SRE and DataOps engineer with two years of production on-call on GCP and HashiCorp Nomad. Kept 99.9% uptime, cut MTTR by 65% with a full observability stack, and migrated MySQL to ClickHouse for 100x faster queries. Promoted to Technical Project Lead for delivery and cost ownership, working remotely with a Paris-based team."),
 "data": ("Data Engineer","Data engineer who owns pipelines end to end: ingestion, ClickHouse and BigQuery storage, data-quality monitoring and cost per event. Migrated critical analytics from MySQL to ClickHouse (100x faster on 10M+ records) and designed the architecture roadmap for ~20x event growth. Technical Project Lead, remote with a Paris-based team."),
 "gcp":  ("Cloud Engineer (GCP)","Cloud and SRE engineer running production on Google Cloud (Pub/Sub, Cloud Run, Cloud Functions, BigQuery). Led a 50% GCP cost reduction and built a cost-per-million-events model that makes cloud spend an engineering metric. 99.9% uptime, 65% lower MTTR. Technical Project Lead, remote with a Paris-based team."),
 "go":   ("Go Backend & Infrastructure Engineer","Engineer who writes and operates production Go: a server-side event collection service feeding multiple ad platforms, memory-optimized hot paths that helped halve cloud cost, and ETL on Nomad. Kept 99.9% uptime with on-call duty, and migrated MySQL to ClickHouse for 100x faster queries. Technical Project Lead, remote with a Paris-based team."),
}

CSS = """
@page{size:A4;margin:11mm 14mm}
*{box-sizing:border-box}
body{font:9.4pt/1.34 'Liberation Sans',Arial,Helvetica,sans-serif;color:#1a1a1a;margin:0}
h1{font-size:23pt;margin:0;letter-spacing:-.3pt}
.title{font-size:11.5pt;color:#0f766e;font-weight:700;margin:1px 0 4px}
.contact{font-size:8.6pt;color:#444}.contact span+span:before{content:" · ";color:#999}
.sub{font-size:8.6pt;color:#444;margin-top:1px}
h2{font-size:9.5pt;text-transform:uppercase;letter-spacing:1.1pt;color:#0f766e;border-bottom:1px solid #cfd8dc;padding-bottom:1.5px;margin:9px 0 4px}
.row{display:flex;justify-content:space-between;font-weight:700;margin-top:4px}.row i{font-weight:400;color:#555;font-style:normal}
.org{color:#555;font-size:8.8pt}
ul{margin:2px 0 0;padding-left:14px}li{margin:0 0 1.6px}
.sk{display:grid;grid-template-columns:92px 1fr;gap:1px 8px}.sk b{font-weight:700}
.p b{font-weight:700}.p{margin-top:2px}
"""

def page(key, public=False):
    title, summary = VARIANTS[key]
    jobs = "".join(
      f'<div class="row"><span>{e(r)}</span><i>{d}</i></div><div class="org">The Quantic Factory · Paris, France (remote)</div><ul>{"".join(f"<li>{e(b)}</li>" for b in bl)}</ul>'
      for r,d,bl in EXP[key])
    skills = "".join(f'<b>{e(a)}</b><span>{e(b)}</span>' for a,b in SKILLS[key])
    projs = "".join(f'<div class="p"><b>{e(a)}.</b> {e(b)}</div>' for a,b in PROJ[key])
    head = [h for h in HEADER if not (public and h.startswith("+216"))] + ([PORTFOLIO] if PORTFOLIO else [])
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>Khalil Rezgui — {e(title)}</title><style>{CSS}</style></head><body>
<h1>Khalil Rezgui</h1><div class="title">{e(title)}</div>
<div class="contact">{"".join(f"<span>{e(h)}</span>" for h in head)}</div><div class="sub">{e(SUB)}</div>
<h2>Summary</h2><div>{e(summary)}</div>
<h2>Experience</h2>{jobs}
<h2>Selected projects</h2>{projs}
<h2>Skills</h2><div class="sk">{skills}</div>
<h2>Education & languages</h2>
<div class="row"><span>Engineering Degree in Computer Science, Cloud Computing & IT Architecture</span><i>2024</i></div>
<div class="org">Esprit School of Engineering, Tunis · Top of the class, final-year project with highest honors</div>
<div class="row"><span>Licence in Computer Science & Multimedia</span><i>2021</i></div><div class="org">Higher Institute of Multimedia, Manouba</div>
<div style="margin-top:3px">Azure Fundamentals (AZ-900), 2023 · English (fluent) · French (fluent) · Arabic (native)</div>
</body></html>"""

for out in ("cv","cv-web"): shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
names = {"sre":"Khalil_Rezgui_CV_SRE","data":"Khalil_Rezgui_CV_Data_Engineer","gcp":"Khalil_Rezgui_CV_GCP_Cloud","go":"Khalil_Rezgui_CV_Go_Backend"}
for out,pub in (("cv",False),("cv-web",True)):
  for k,n in names.items():
    h = os.path.abspath(f"{out}/{n}.html"); open(h,"w").write(page(k,pub))
    subprocess.run(["google-chrome","--headless","--no-sandbox","--disable-gpu","--no-pdf-header-footer",f"--print-to-pdf={out}/{n}.pdf",f"file://{h}"],check=True,capture_output=True)
    os.remove(h)
print("done")
