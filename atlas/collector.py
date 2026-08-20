"""Bounded, robots-aware collection for approved sources; no authentication or crawling."""
from __future__ import annotations
import hashlib, json, re, time
from datetime import UTC, datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit, urlunsplit
from urllib.request import Request, urlopen
from urllib.robotparser import RobotFileParser

USER_AGENT = "AtlasOfKnowledgeBot/0.3 (+https://github.com/theworker02/atlas-of-knowledge)"
class Page(HTMLParser):
    def __init__(self): super().__init__(); self.title=""; self._tag=None; self.headings=[]; self.links=[]
    def handle_starttag(self, tag, attrs):
        values=dict(attrs); self._tag=tag if tag in {"title","h1","h2","h3"} else None
        if tag == "a" and values.get("href"): self.links.append(values["href"])
    def handle_endtag(self, tag):
        if tag == self._tag: self._tag=None
    def handle_data(self, data):
        text=" ".join(data.split())
        if self._tag == "title" and text: self.title += text
        elif self._tag in {"h1","h2","h3"} and text: self.headings.append(text)
def canonical(url: str) -> str:
    parts=urlsplit(url); return urlunsplit((parts.scheme,parts.netloc,parts.path.rstrip("/"),"",""))
def allowed_by_robots(url: str) -> bool:
    parts=urlsplit(url); robots=RobotFileParser(f"{parts.scheme}://{parts.netloc}/robots.txt")
    try: robots.read(); return robots.can_fetch(USER_AGENT,url)
    except Exception: return False
def fetch(url: str, retries: int=2, timeout: int=15) -> dict:
    if not allowed_by_robots(url): raise PermissionError("robots.txt disallows Atlas collector")
    last=None
    for attempt in range(retries+1):
        try:
            request=Request(url,headers={"User-Agent":USER_AGENT,"Accept":"text/html,application/xhtml+xml"})
            with urlopen(request,timeout=timeout) as response:
                body=response.read(2_000_000); kind=response.headers.get_content_type()
                if kind not in {"text/html","text/plain"}: raise ValueError(f"unsupported content type {kind}")
                return {"url":canonical(response.url),"content_type":kind,"body":body.decode(response.headers.get_content_charset() or "utf-8",errors="replace"),"content_hash":hashlib.sha256(body).hexdigest(),"fetched_at":datetime.now(UTC).isoformat()}
        except (HTTPError,URLError,TimeoutError,ValueError) as error:
            last=error
            if attempt < retries: time.sleep(0.5 * (2 ** attempt))
    raise RuntimeError(str(last))
def collect_course(course: dict) -> tuple[dict, list[dict]]:
    page=fetch(course["source_url"]); parser=Page(); parser.feed(page.pop("body"))
    base=course["source_url"]; resources=[]
    for link in parser.links:
        absolute=canonical(urljoin(base,link))
        if urlsplit(absolute).netloc == urlsplit(base).netloc and re.search(r"(syllabus|lecture|assignment|problem|exam|lab|schedule|\.pdf$)",absolute,re.I):
            kind=next((x for x in ("syllabus","lecture","assignment","problem_set","exam","lab","schedule") if x.replace("_"," ") in absolute.lower() or x.replace("_","") in absolute.lower()),"supplementary")
            if absolute not in {x["url"] for x in resources}: resources.append({"type":kind,"url":absolute,"status":"discovered"})
    provenance={"source_course":course["course_id"],"source_url":page["url"],"source_hash":page["content_hash"],"ingested_at":page["fetched_at"],"pipeline_version":"0.3.0","license":course["license"]}
    return {"course_id":course["course_id"],"title":parser.title or course["title"],"headings":parser.headings[:40],"resources":resources,"provenance":provenance}, resources
def records_from_outline(outline: dict, course: dict) -> list[dict]:
    # Headings are short catalog metadata. Explanations are original and deliberately do not reproduce source passages.
    labels=[]
    for heading in outline["headings"]:
        cleaned=re.sub(r"\s+"," ",heading).strip()
        if 3 <= len(cleaned) <= 100 and cleaned.lower() not in {x.lower() for x in labels}: labels.append(cleaned)
    labels=labels[:8] or [course["title"]]
    output=[]
    for index,label in enumerate(labels,1):
        slug=re.sub(r"[^a-z0-9]+","-",label.lower()).strip("-")[:45] or f"topic-{index}"
        identifier=f"{course['discipline'].lower().replace(' ','-')}:{course['course_id'].split(':')[-1].replace('_','-')[:30]}:{slug}"
        output.append({"id":identifier,"concept":label,"discipline":course["discipline"],"course":course["title"],"topic":"Collected course outline","definition":f"{label} is a curriculum topic identified from the public outline of {course['title']}.","explanation":"This initial Atlas entry records a discoverable course topic and its provenance. It is intentionally conservative: richer explanatory records require additional licensed, structurally parseable material and must pass the same validation gates.","prerequisites":[],"related_concepts":[],"core_principles":["Course-outline topics are metadata anchors, not copied instructional content."],"examples":[f"Appears in the public course outline for {course['title']}."],"applications":["Supports curriculum discovery and targeted future ingestion."],"common_misconceptions":["A course-outline topic alone is not a complete explanation of the concept."],"assumptions":["The source page is current and its headings describe the named course."],"reasoning":"The collector preserves a short topic label, ties it to a content hash and source URL, and defers deeper synthesis until sufficient eligible material is available.","questions":[f"What role does {label} play in {course['title']}?"],"answers":["The collected outline identifies it as a course topic; its detailed pedagogical role requires further licensed material."],"domain_properties":{},"provenance":outline["provenance"]})
    return output
