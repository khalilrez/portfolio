#!/usr/bin/env python3
"""Generates one portfolio page per target role from shared content. Run: python3 build.py"""
import os, html, shutil

NAME = "Khalil Rezgui"
EMAIL = "khalilrezgui0@gmail.com"
GH = "https://github.com/khalilrez"
LI = "https://linkedin.com/in/khalil-rezgui"

# ---- shared content -------------------------------------------------------
PROJECTS = {
 "incident": dict(t="Production incident detection & recovery",
   p="Recurring pipeline failures were being found by customers, not by us.",
   d="Centralized monitoring over infrastructure, application and data-quality signals, plus restart, rollback and database-recovery runbooks with post-recovery validation.",
   r="Recurring failures turned into alerts and repeatable procedures; MTTR down 65%.",
   tags=["Grafana","Prometheus","Graylog","Nomad"]),
 "finops": dict(t="Infrastructure cost & data architecture redesign",
   p="Redundant compute, storage and transfer layers, with ~20x event growth ahead.",
   d="Mapped data flows end to end, built a cost model around a 'cost per million events' KPI, and benchmarked direct ClickHouse ingestion, managed queues, self-hosted HA Nomad, optimized MySQL and DuckLake/Parquet on object storage.",
   r="A prioritized modernization roadmap built to absorb ~20x ingestion without linear cost growth.",
   tags=["GCP","BigQuery","ClickHouse","FinOps","DuckLake"]),
 "clickhouse": dict(t="MySQL to ClickHouse migration",
   p="Analytics queries on 10M+ records were too slow for real-time diagnostics.",
   d="Designed a two-node ClickHouse cluster and migrated from MySQL with a blue-green strategy and no downtime.",
   r="100x faster queries and real-time diagnostics.",
   tags=["ClickHouse","MySQL","Migration","SQL"]),
 "gcpcost": dict(t="GCP cost reduction",
   p="Cloud spend was growing faster than traffic.",
   d="Found obsolete and cost-heavy services to replace or remove, and rewrote hot production paths in Go to save memory.",
   r="50% lower GCP cost.",
   tags=["GCP","Cloud Run","Pub/Sub","Go"]),
 "tracking": dict(t="Server-side event tracking in Go",
   p="Client-side tracking lost conversions and could not feed several ad platforms reliably.",
   d="Built an event collection service in Go, containerized and run on Nomad, that processes events and routes them to multiple destinations such as Meta and Google Ads.",
   r="The foundation of the company's tracking and attribution pipeline.",
   tags=["Go","Docker","Nomad","ETL"]),
 "identity": dict(t="Identity resolution & graph validation",
   p="No objective way to trust a production identity-resolution system.",
   d="Defined KPIs (identifiable and identified sessions, hard candidate and identification rates) and compared BFS and DSU (union-find) engines across 2-day to 7-month windows.",
   r="Verified output consistency before rollout.",
   tags=["Graphs","SQL","Python","Data quality"]),
 "agent": dict(t="Multi-agent AI orchestrator",
   p="Shopify merchants needed analytical answers beyond what standard tools offer.",
   d="Designed and built an orchestrator from scratch that processes complex user queries, with OpenTelemetry tracing across the whole system.",
   r="Insight queries standard tooling could not answer, fully observable in production.",
   tags=["Python","OpenTelemetry","LLM agents"]),
 "cicd": dict(t="CI/CD pipeline for Spring Boot & Angular",
   p="One-hour manual releases.",
   d="Jenkins, SonarQube and Git pipeline with quality gates and test-driven development.",
   r="15-minute automated deploys, 85% code coverage.",
   tags=["Jenkins","SonarQube","Docker"]),
}

SKILLS = {
 "rel":  ("Reliability & observability","On-call · Incident response · Runbooks · Fluentd · Elasticsearch · Graylog · Grafana · Prometheus · OpenTelemetry"),
 "cloud":("Cloud & infrastructure","GCP (Pub/Sub, Cloud Run, Cloud Functions, BigQuery, IAM, Cloud Monitoring) · Azure · Docker · Kubernetes · HashiCorp Nomad · Ansible"),
 "data": ("Data","ClickHouse · BigQuery · MySQL · PostgreSQL · DuckDB / DuckLake · Parquet & object storage · Message queues · ETL · Data quality"),
 "code": ("Code","Go · Python · SQL · Bash · Rust · JavaScript · Java"),
 "cicd": ("Delivery","Jenkins · GitHub Actions · SonarQube · Git · TDD"),
}

REPOS = {
 "debug-practice-go": ("Go · alerting utilities","Alert dedup, severity from error rate, retries and structured log parsing, with tests and a written debug report on each bug fixed."),
 "pulse-sre": ("Go · queue writer / reader","Queue writer and reader packages with tests and a sanity-check command."),
 "etl_devops": ("Python · Docker · Bash","ETL into a Flask and Plotly dashboard with container monitoring, one-command pipeline."),
 "port_sniffer": ("Rust","Multithreaded CLI port scanner."),
}

REMOTE = [
 ("I already do it, across a border.","I work remotely from Tunis with managers and a team based in Paris. Tunisia is on UTC+1 all year, so I overlap France's working day almost entirely."),
 ("Carrying a pager from a distance.","I took on-call and overnight pager duty for production systems, so I know that remote reliability means alerts, runbooks and clear handoffs, not being in the room."),
 ("Written by default.","Post-mortems, runbooks, architecture decision notes and benchmark reports. I leave a trail someone else can pick up without a call."),
 ("Trusted with ownership.","Promoted to Technical Project Lead to run five-plus workstreams and coordinate priorities and deadlines, all remotely."),
 ("Easy to hire in Europe.","Italian citizenship: no visa or sponsorship needed to work in the EU."),
]

# ---- role variants --------------------------------------------------------
ROLES = {
 "": dict(slug="", label="SRE / Platform", cv="Khalil_Rezgui_CV_SRE.pdf",
   title="Site Reliability & Platform Engineer",
   h1="I keep production <em>reliable, observable</em> and cheap to run.",
   lead="SRE and DataOps engineer with two years of on-call experience on GCP and HashiCorp Nomad. I cut incident resolution time, migrate databases without downtime, and design infrastructure that costs less per event.",
   stats=[("99.9","%","uptime on GCP and Nomad"),("65","%","lower mean time to resolution"),("100","x","faster queries after ClickHouse migration"),("50","%","lower GCP cost")],
   projects=["incident","finops","clickhouse","gcpcost","cicd"], skills=["rel","cloud","data","code","cicd"],
   repos=["debug-practice-go","pulse-sre","etl_devops"]),
 "data": dict(slug="data", label="Data Engineering", cv="Khalil_Rezgui_CV_Data_Engineer.pdf",
   title="Data Engineer",
   h1="I build data pipelines that <em>run predictably</em> at scale.",
   lead="Data engineer who owns pipelines end to end: ingestion, ClickHouse and BigQuery storage, data-quality monitoring and cost per event. I migrated critical analytics from MySQL to ClickHouse and designed the roadmap for ~20x more events.",
   stats=[("100","x","faster queries on 10M+ records"),("20","x","ingestion growth architected for"),("5","+","production data workstreams owned"),("65","%","lower mean time to resolution")],
   projects=["clickhouse","finops","identity","tracking","agent","incident"], skills=["data","code","cloud","rel","cicd"],
   repos=["etl_devops","debug-practice-go","pulse-sre"]),
 "gcp": dict(slug="gcp", label="GCP / Cloud", cv="Khalil_Rezgui_CV_GCP_Cloud.pdf",
   title="Cloud Engineer (GCP)",
   h1="I run GCP workloads <em>reliably</em> and at half the cost.",
   lead="Cloud and SRE engineer who operates production on Google Cloud: Pub/Sub, Cloud Run, Cloud Functions and BigQuery. I led a 50% cost reduction and built the FinOps model that turns cloud spend into an engineering metric.",
   stats=[("50","%","GCP cost reduction"),("99.9","%","uptime on GCP and Nomad"),("65","%","lower mean time to resolution"),("20","x","growth the new architecture absorbs")],
   projects=["gcpcost","finops","clickhouse","incident","agent","cicd"], skills=["cloud","rel","data","code","cicd"],
   repos=["pulse-sre","etl_devops","debug-practice-go"]),
 "go": dict(slug="go", label="Go / Backend", cv="Khalil_Rezgui_CV_Go_Backend.pdf",
   title="Go Backend & Infrastructure Engineer",
   h1="I write <em>Go services</em> that stay up and stay cheap.",
   lead="Engineer who builds production Go: a server-side event collection service routing to multiple ad platforms, memory-optimized hot paths that helped halve cloud cost, and ETL running on Nomad. I operate what I build, including the pager.",
   stats=[("50","%","lower GCP cost, partly via Go rewrites"),("99.9","%","uptime on what I ship"),("100","x","faster queries on the data layer I built"),("65","%","lower mean time to resolution")],
   projects=["tracking","gcpcost","clickhouse","agent","incident","cicd"], skills=["code","cloud","data","rel","cicd"],
   repos=["debug-practice-go","pulse-sre","port_sniffer"]),
}

# ---- rendering ------------------------------------------------------------
e = html.escape
def render(role, root):
    r = ROLES[role]
    sw = "".join(f'<a href="{root}{k}{"/" if k else ""}" class="{"on" if k==role else ""}">{v["label"]}</a>' for k,v in ROLES.items())
    stats = "".join(f'<div class="stat"><b data-to="{n}" data-dec="{1 if "." in n else 0}">{n}</b><i>{u}</i><span>{e(l)}</span></div>' for n,u,l in r["stats"])
    cards = "".join(
      f'<article class="card"><h3>{e(p["t"])}</h3><p><b>Problem:</b> {e(p["p"])}</p><p><b>What I did:</b> {e(p["d"])}</p>'
      f'<p class="result">{e(p["r"])}</p><div class="tags">{"".join(f"<span>{e(t)}</span>" for t in p["tags"])}</div></article>'
      for p in (PROJECTS[k] for k in r["projects"]))
    skills = "".join(f'<div><h4>{e(SKILLS[k][0])}</h4><p>{e(SKILLS[k][1])}</p></div>' for k in r["skills"])
    repos = "".join(f'<a class="repo" href="{GH}/{k}"><b>{k}</b><small>{e(v[0])}</small><span>{e(v[1])}</span></a>' for k,v in ((k,REPOS[k]) for k in r["repos"]))
    remote = "".join(f'<div class="rm"><h4>{e(h)}</h4><p>{e(t)}</p></div>' for h,t in REMOTE)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{NAME} — {r["title"]}</title>
<meta name="description" content="{e(r["lead"][:155])}">
<meta property="og:title" content="{NAME} — {r["title"]}"><meta property="og:description" content="{e(r["lead"][:155])}"><meta property="og:type" content="website">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='22' fill='%230b0f14'/><text x='50' y='68' font-size='56' text-anchor='middle' font-family='monospace' fill='%2334d399'>K</text></svg>">
<link rel="stylesheet" href="{root}style.css"></head><body>
<header class="nav"><a class="brand" href="#top">khalil<span>.rezgui</span></a>
<nav><a href="#impact">Impact</a><a href="#experience">Experience</a><a href="#projects">Work</a><a href="#remote">Remote</a><a class="btn small" href="#contact">Contact</a></nav></header>
<div class="switch"><span>Viewing as</span>{sw}</div>
<main id="top">
<section class="hero"><p class="eyebrow"><span class="dot"></span> Open to remote roles · Tunis, UTC+1 · EU work authorization</p>
<h1>{r["h1"]}</h1><p class="lead">{e(r["lead"])}</p>
<div class="cta"><a class="btn" href="mailto:{EMAIL}">Get in touch</a><a class="btn ghost" href="{root}{r["cv"]}" download>Download CV</a><a class="link" href="{GH}">GitHub</a><a class="link" href="{LI}">LinkedIn</a></div></section>
<section id="impact" class="stats">{stats}</section>
<section id="experience"><h2><span>01</span> Experience</h2>
<div class="job"><div class="when">Jan 2026 — Present</div><div><h3>Technical Project Lead</h3><p class="org">The Quantic Factory · Paris, remote</p><ul>
<li>Own reliability and delivery for 5+ production data workstreams: CRM, tracking, monitoring, attribution and identity resolution.</li>
<li>Led a company-wide FinOps and data architecture redesign across GCP, BigQuery, MySQL, ClickHouse, Hetzner and Scaleway, with a roadmap for ~20x ingestion growth without proportional cost.</li>
<li>Built post-production validation in SQL and ClickHouse that catches event-volume anomalies and identifier gaps before customers notice.</li></ul></div></div>
<div class="job"><div class="when">Jan 2024 — Jan 2026</div><div><h3>DataOps &amp; Site Reliability Engineer</h3><p class="org">The Quantic Factory · Paris, remote</p><ul>
<li>On-call and overnight pager duty: resolved live incidents such as MySQL crashes and pipeline bugs by rollback or in-incident debugging.</li>
<li>Built the observability stack (Fluentd, Elasticsearch, Graylog, Grafana, Prometheus) across 100+ daily jobs, cutting MTTR by 65%.</li>
<li>Migrated critical infrastructure from MySQL to ClickHouse: 100x faster queries on 10M+ records.</li>
<li>Led a team optimizing GCP infrastructure for a 50% cost reduction.</li>
<li>Shipped a Python AI agent to production with 85% prediction accuracy.</li></ul></div></div></section>
<section id="projects"><h2><span>02</span> Selected work</h2><p class="note">Client and company code is private, so these are described by problem and outcome.</p><div class="cards">{cards}</div></section>
<section id="code"><h2><span>03</span> Public code</h2><div class="repos">{repos}</div><p class="note"><a class="link" href="{GH}">More on GitHub</a></p></section>
<section id="remote"><h2><span>04</span> Why I work well remotely</h2><div class="rms">{remote}</div></section>
<section id="skills"><h2><span>05</span> Toolbox</h2><div class="skills">{skills}</div>
<p class="meta">Languages: English (fluent) · French (fluent) · Arabic (native)<br>Education: Engineering degree in Computer Science (Cloud Computing &amp; IT Architecture), Esprit School of Engineering, 2024 · Azure Fundamentals, 2023</p></section>
<section id="contact" class="contact"><h2>Let's talk</h2><p>Looking for a remote {e(r["title"].lower())} role with a European team.</p><a class="btn big" href="mailto:{EMAIL}">{EMAIL}</a></section>
</main><footer>© <span id="y"></span> {NAME}</footer><script src="{root}main.js"></script></body></html>'''

out = "dist"
shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
for f in ("style.css","main.js"): shutil.copy(f, out)
for f in os.listdir("cv-web"):
    if f.endswith(".pdf"): shutil.copy(os.path.join("cv-web",f), out)
for k in ROLES:
    d = os.path.join(out, k); os.makedirs(d, exist_ok=True)
    open(os.path.join(d,"index.html"),"w").write(render(k, "/" if False else ("../" if k else "")))
print("built", list(ROLES))
