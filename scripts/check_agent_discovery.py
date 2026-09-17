#!/usr/bin/env python3
"""Check a Hugo production build's public discovery contracts, without dependencies.

Usage: python3 scripts/check_agent_discovery.py [public] [--base-url URL]
This inspects built files; it does not make network requests or assess search rank.
"""

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
from urllib.robotparser import RobotFileParser


PROJECTS = ("arched", "conformal-predictors", "siftom", "uncertain-defer")
SAMPLE_PREFIXES = ("/post/", "/teaching/", "/event/")
SAMPLE_TITLES = (
    "Example Talk", "Learn JavaScript", "Learn Python", "Teach academic courses",
    "Manage your projects", "Easily create your own simple yet highly customizable blog",
    "Sharpen your thinking with a second brain",
    "Communicate your results effectively with the best data visualizations",
)


def normalized(value):
    return " ".join(str(value).split())


def nodes(value):
    """Support individual schema objects, @graph, arrays, and nested objects."""
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from nodes(child)
    elif isinstance(value, list):
        for child in value:
            yield from nodes(child)


def has_type(node, expected):
    actual = node.get("@type", [])
    return expected in (actual if isinstance(actual, list) else [actual])


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.canonicals = []
        self.markdown_alternates = []
        self.bibtex_alternates = []
        self.metadata = defaultdict(list)
        self.links = []
        self.anchors = []
        self.footer_anchors = []
        self.schemas = []
        self.headings = []
        self.section_headings = []
        self.abstracts = []
        self.visible = []
        self.alias = False
        self.refresh_targets = []
        self._schema = None
        self._heading = None
        self._section_heading = None
        self._abstract = None
        self._abstract_depth = 0
        self._anchor = None
        self._hidden = 0
        self._in_footer = False
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id") == "paper-abstract":
            self._abstract = []
            self._abstract_depth = 1
        elif self._abstract is not None and tag not in ("area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"):
            self._abstract_depth += 1
        if tag == "link" and "canonical" in attrs.get("rel", "").lower().split():
            self.canonicals.append(attrs.get("href", ""))
        if tag == "link" and "alternate" in attrs.get("rel", "").lower().split() and attrs.get("type", "").lower().split(";")[0] == "text/markdown":
            self.markdown_alternates.append(attrs.get("href", ""))
        if tag == "link" and "alternate" in attrs.get("rel", "").lower().split() and attrs.get("type", "").lower().split(";")[0] == "application/x-bibtex":
            self.bibtex_alternates.append(attrs.get("href", ""))
        if tag == "meta":
            name = attrs.get("name", "").lower()
            self.metadata[name].append(attrs.get("content", ""))
            self.alias |= attrs.get("http-equiv", "").lower() == "refresh"
            if attrs.get("http-equiv", "").lower() == "refresh":
                target = re.search(r"(?:^|;)\s*url\s*=\s*(.+)$", attrs.get("content", ""), re.I)
                if target:
                    self.refresh_targets.append(target.group(1).strip("\"' "))
        if tag == "footer":
            self._in_footer = True
        if tag == "a":
            self._anchor = [attrs.get("href", ""), [], self._in_footer]
            self.links.append(attrs.get("href", ""))
        if tag == "h1":
            self._heading = []
        if tag in ("h2", "h3", "h4", "h5", "h6"):
            self._section_heading = []
        if tag in ("script", "style"):
            self._hidden += 1
        if tag == "script" and attrs.get("type", "").lower() == "application/ld+json":
            self._schema = []

    def handle_endtag(self, tag):
        if self._abstract is not None:
            self._abstract_depth -= 1
            if self._abstract_depth == 0:
                self.abstracts.append(normalized("".join(self._abstract)))
                self._abstract = None
        if tag == "script" and self._schema is not None:
            self.schemas.append("".join(self._schema))
            self._schema = None
        if tag in ("script", "style"):
            self._hidden = max(0, self._hidden - 1)
        if tag == "h1" and self._heading is not None:
            self.headings.append(normalized("".join(self._heading)))
            self._heading = None
        if tag in ("h2", "h3", "h4", "h5", "h6") and self._section_heading is not None:
            self.section_headings.append(normalized("".join(self._section_heading)))
            self._section_heading = None
        if tag == "a" and self._anchor is not None:
            anchor = (self._anchor[0], normalized("".join(self._anchor[1])))
            self.anchors.append(anchor)
            if self._anchor[2]:
                self.footer_anchors.append(anchor)
            self._anchor = None
        if tag == "footer":
            self._in_footer = False

    def handle_data(self, data):
        if self._schema is not None:
            self._schema.append(data)
        if self._heading is not None:
            self._heading.append(data)
        if self._section_heading is not None:
            self._section_heading.append(data)
        if self._anchor is not None:
            self._anchor[1].append(data)
        if not self._hidden:
            self.visible.append(data)
            if self._abstract is not None:
                self._abstract.append(data)


class Audit:
    def __init__(self, root, base):
        self.root = root.resolve()
        self.base = base.rstrip("/") + "/"
        self.origin = urlsplit(self.base)
        self.errors = []
        self.pages = {}
        self.schema_nodes = {}
        self.papers = {}

    def require(self, condition, message):
        if not condition:
            self.errors.append(message)

    def url(self, path):
        return urljoin(self.base, path.lstrip("/"))

    def local_file(self, url):
        parsed = urlsplit(url)
        prefix = self.origin.path.rstrip("/")
        path = unquote(parsed.path)
        if prefix and not (path == prefix or path.startswith(prefix + "/")):
            return None
        relative = path[len(prefix):].lstrip("/")
        target = (self.root / relative).resolve()
        if not target.is_relative_to(self.root):
            return None
        if target.is_dir() or path.endswith("/"):
            target /= "index.html"
        elif not target.exists() and not target.suffix:
            target /= "index.html"
        return target if target.is_file() else None

    def same_origin(self, url):
        parsed = urlsplit(url)
        return (parsed.scheme, parsed.netloc) == (self.origin.scheme, self.origin.netloc)

    def check_local_link(self, source, target, context):
        if not target or target.startswith("#"):
            return
        resolved = urljoin(source, target)
        parsed = urlsplit(resolved)
        if parsed.scheme not in ("http", "https"):
            return
        if self.same_origin(resolved):
            self.require(self.local_file(resolved), f"{context}: missing local target {resolved}")
        elif parsed.hostname in {self.origin.hostname, "www." + str(self.origin.hostname), "localhost", "127.0.0.1", "yizirui.github.io"}:
            self.require(False, f"{context}: use the configured canonical origin instead of {resolved}")

    def read(self, relative):
        path = self.root / relative
        if not path.is_file():
            self.errors.append(f"Missing required discovery file: {relative}")
            return ""
        return path.read_text(encoding="utf-8")

    def check_html(self):
        for path in sorted(self.root.rglob("*.html")):
            relative = path.relative_to(self.root).as_posix()
            page = Page(path.read_text(encoding="utf-8"))
            if page.alias or relative == "404.html" or re.search(r"(?:^|/)page/\d+/", relative):
                continue
            route = relative[:-10] if relative.endswith("index.html") else relative
            expected = self.url(route)
            self.pages[route] = page
            self.require(page.canonicals == [expected], f"{relative}: expected exactly one canonical {expected}; found {page.canonicals}")
            descriptions = page.metadata["description"]
            self.require(len(descriptions) == 1 and bool(descriptions[0].strip()), f"{relative}: expected one nonempty meta description")
            schema_nodes = []
            for index, raw in enumerate(page.schemas, 1):
                try:
                    value = json.loads(raw)
                    self.require(isinstance(value, (dict, list)), f"{relative}: JSON-LD #{index} must contain an object or array")
                    schema_nodes.extend(nodes(value))
                except json.JSONDecodeError as error:
                    self.errors.append(f"{relative}: invalid JSON-LD #{index}: {error}")
            self.schema_nodes[route] = schema_nodes

        home = self.pages.get("")
        self.require(home is not None, "Missing rendered homepage index.html")
        if home:
            for kind in ("Person", "WebSite"):
                matches = [n for n in self.schema_nodes[""] if has_type(n, kind)]
                self.require(matches, f"index.html: missing {kind} JSON-LD")
                for node in matches:
                    self.require(node.get("name"), f"index.html: {kind} needs a name")
                    self.require(node.get("url") == self.base, f"index.html: {kind}.url must equal {self.base}")
                    if kind == "Person":
                        self.require(normalized(node.get("name", "")) in normalized(" ".join(home.visible)), "index.html: Person.name is absent from visible text")

        publications = {route: page for route, page in self.pages.items() if re.fullmatch(r"publication/[^/]+/", route)}
        self.publication_count = len(publications)
        self.require(len(publications) >= 5, f"Expected at least 5 public paper pages, found {len(publications)}")
        for route, page in publications.items():
            articles = [n for n in self.schema_nodes[route] if has_type(n, "ScholarlyArticle")]
            self.require(len(articles) == 1, f"{route}: expected one ScholarlyArticle, found {len(articles)}")
            titles = page.metadata["citation_title"]
            authors = page.metadata["citation_author"]
            pdfs = page.metadata["citation_pdf_url"]
            self.require(len(titles) == 1 and bool(titles[0].strip()), f"{route}: missing or duplicate citation_title")
            self.require(authors and all(name.strip() for name in authors), f"{route}: missing citation_author metadata")
            if titles:
                self.require(normalized(titles[0]) in page.headings, f"{route}: citation_title must match the visible H1")
            visible_pdfs = [href for href, label in page.anchors if re.search(r"\bPDF\b", label, re.I)]
            visible_pdf_urls = [urljoin(self.url(route), href) for href in visible_pdfs]
            if any(self.same_origin(pdf) for pdf in visible_pdf_urls):
                self.require(pdfs, f"{route}: a local PDF link needs citation_pdf_url")
            for pdf in pdfs:
                self.require(urlsplit(pdf).scheme in ("http", "https"), f"{route}: citation_pdf_url must be an absolute URL: {pdf}")
                same_directory = urlsplit(pdf).path.rsplit("/", 1)[0] == urlsplit(self.url(route)).path.rstrip("/")
                self.require(self.same_origin(pdf) and same_directory, f"{route}: citation_pdf_url must be hosted in the abstract page's directory: {pdf}")
                if visible_pdfs:
                    self.require(pdf in visible_pdf_urls, f"{route}: citation_pdf_url differs from visible PDF links")
            for article in articles:
                self.papers[route] = article
                self.require(article.get("url") == self.url(route), f"{route}: ScholarlyArticle.url must match its canonical")
                headline = article.get("headline") or article.get("name")
                self.require(titles and normalized(headline) == normalized(titles[0]), f"{route}: ScholarlyArticle title disagrees with citation_title")
                schema_authors = article.get("author", [])
                if not isinstance(schema_authors, list):
                    schema_authors = [schema_authors]
                names = [a.get("name", "") if isinstance(a, dict) else a for a in schema_authors]
                self.require([normalized(a) for a in names] == [normalized(a) for a in authors], f"{route}: ScholarlyArticle authors disagree with citation_author order or names")
                for encoding in nodes(article.get("encoding", {})):
                    if encoding.get("encodingFormat") == "application/pdf":
                        content_url = encoding.get("contentUrl", "")
                        self.require(content_url in visible_pdf_urls, f"{route}: schema PDF differs from visible PDF links")
                        if self.same_origin(content_url):
                            self.require(content_url in pdfs, f"{route}: local schema PDF differs from citation_pdf_url")
                abstract = article.get("abstract", "")
                self.require(isinstance(abstract, str) and len(abstract.split()) > 50, f"{route}: ScholarlyArticle.abstract must contain the full abstract (more than 50 words)")
                self.require(page.section_headings.count("Abstract") == 1, f"{route}: expected one visible Abstract heading")
                self.require(page.abstracts == [normalized(abstract)], f"{route}: visible #paper-abstract text differs from ScholarlyArticle.abstract")
            bibtex = self.url(f"{route}cite.bib")
            self.require(page.bibtex_alternates == [bibtex], f"{route}: missing canonical application/x-bibtex alternate {bibtex}")
            self.require(self.local_file(bibtex), f"{route}: citation file does not exist: {bibtex}")
            for pdf in pdfs:
                if self.same_origin(pdf):
                    file = self.local_file(pdf)
                    self.require(file, f"{route}: citation_pdf_url has no local PDF: {pdf}")
                    if file:
                        with file.open("rb") as stream:
                            self.require(stream.read(5) == b"%PDF-", f"{route}: citation_pdf_url does not contain PDF bytes: {pdf}")

    def check_markdown(self):
        required = ["index.md", "projects/index.md", "experience/index.md", "research/index.md"]
        required += [f"project/{slug}/index.md" for slug in PROJECTS]
        required += [f"{route}index.md" for route in self.pages if re.fullmatch(r"publication/[^/]+/", route)]
        llms = self.read("llms.txt")
        texts = {"llms.txt": llms}
        for relative in required:
            texts[relative] = self.read(relative)
        for path in self.root.rglob("*.md"):
            relative = path.relative_to(self.root).as_posix()
            if relative not in texts:
                texts[relative] = path.read_text(encoding="utf-8")
            if relative.endswith("index.md"):
                route = relative[:-8]
                page = self.pages.get(route)
                if page:
                    target = self.url(relative)
                    self.require(page.markdown_alternates == [target], f"{route or 'index.html'}: expected one rel=alternate text/markdown link to {target}")
                    footer_urls = {urljoin(self.url(route), href) for href, label in page.footer_anchors if label}
                    self.require(target in footer_urls, f"{route or 'index.html'}: missing labeled footer link to {target}")
                else:
                    self.require(False, f"{relative}: Markdown has no corresponding canonical HTML page")
        llms_targets = set()
        for relative, body in texts.items():
            self.require(bool(body.strip()), f"{relative}: must contain useful text")
            inline = re.findall(r"!?\[[^\]\n]*\]\(\s*(<[^>\n]+>|[^\s)]+)", body)
            references = re.findall(r"^\s{0,3}\[[^\]\n]+\]:\s*(<[^>\n]+>|\S+)", body, re.M)
            html_links = re.findall(r"(?:href|src)=[\"']([^\"']+)[\"']", body)
            for target in inline + references + html_links:
                target = target.strip("<>")
                self.check_local_link(self.url(relative), target, relative)
                if relative == "llms.txt":
                    llms_targets.add(urljoin(self.url(relative), target))
        for relative in required:
            self.require(self.url(relative) in llms_targets, f"llms.txt: missing Markdown entry {self.url(relative)}")
        for relative in ("research/", "papers.json"):
            self.require(self.url(relative) in llms_targets, f"llms.txt: missing research discovery entry {self.url(relative)}")
        self.markdown = texts
        for slug in PROJECTS:
            target = self.url(f"project/{slug}/")
            for route in ("", "projects/"):
                page = self.pages.get(route)
                links = {urljoin(self.url(route), href) for href in page.links} if page else set()
                self.require(target in links, f"{route or 'index.html'}: missing internal project detail link {target}")
            self.require(target in llms_targets, f"llms.txt: missing canonical project page {target}")

    def check_paper_content(self):
        for route, article in self.papers.items():
            body = self.markdown.get(f"{route}index.md", "")
            sections = re.findall(r"^#{1,6}\s+Abstract\s*\n(.*?)(?=^#{1,6}\s|\Z)", body, re.M | re.S)
            self.require(len(sections) == 1, f"{route}index.md: expected one Abstract section")
            if sections:
                abstract = normalized(article.get("abstract", ""))
                # Source attribution may follow the prose, separated by a blank line.
                paragraphs = re.split(r"\n\s*\n", sections[0].strip())
                abstract_paragraphs = []
                for paragraph in paragraphs:
                    if re.search(r"\[[^\]]+\]\(https?://", paragraph) or paragraph.strip() == "---":
                        break
                    abstract_paragraphs.append(paragraph)
                self.require(normalized(" ".join(abstract_paragraphs)) == abstract, f"{route}index.md: Abstract text differs from ScholarlyArticle.abstract")

        research = self.pages.get("research/")
        self.require(research is not None, "Missing research/index.html topic guide")
        if research:
            research_urls = {urljoin(self.url("research/"), href) for href, label in research.anchors if label}
            for route in self.papers:
                self.require(self.url(route) in research_urls, f"research/index.html: missing labeled paper link {self.url(route)}")

        try:
            catalog = json.loads(self.read("papers.json"))
        except json.JSONDecodeError as error:
            self.errors.append(f"papers.json: invalid JSON: {error}")
            return
        if not isinstance(catalog, dict):
            self.errors.append("papers.json: expected an object with owner, url, and papers")
            return
        self.require(isinstance(catalog.get("owner"), str) and bool(catalog["owner"].strip()), "papers.json: missing owner name")
        catalog_url = catalog.get("url", "")
        self.require(isinstance(catalog_url, str) and self.same_origin(catalog_url) and self.local_file(catalog_url), "papers.json: url must identify an existing canonical local resource")
        records = catalog.get("papers")
        if not isinstance(records, list):
            self.errors.append("papers.json: papers must be an array")
            return
        by_url = {}
        for index, record in enumerate(records):
            if not isinstance(record, dict) or not isinstance(record.get("url"), str):
                self.errors.append(f"papers.json: paper #{index + 1} must be an object with a URL")
                continue
            url = record["url"]
            self.require(url not in by_url, f"papers.json: duplicate paper URL {url}")
            by_url[url] = record
        expected = {self.url(route) for route in self.papers}
        self.require(set(by_url) == expected, f"papers.json: paper URLs must match rendered publications; missing={sorted(expected - set(by_url))}, extra={sorted(set(by_url) - expected)}")
        for route, article in self.papers.items():
            url = self.url(route)
            record = by_url.get(url)
            if record is None:
                continue
            page = self.pages[route]
            context = f"papers.json ({route})"
            self.require(normalized(record.get("title", "")) == normalized(article.get("headline") or article.get("name")), f"{context}: title differs from ScholarlyArticle")
            self.require(normalized(record.get("abstract", "")) == normalized(article.get("abstract", "")), f"{context}: abstract differs from ScholarlyArticle")
            self.require(record.get("authors") == page.metadata["citation_author"], f"{context}: authors differ from citation metadata")
            self.require(str(record.get("year", "")) == str(article.get("datePublished", ""))[:4], f"{context}: year differs from ScholarlyArticle.datePublished")
            venue = article.get("isPartOf", {})
            self.require(normalized(record.get("venue", "")) == normalized(venue.get("name", "")), f"{context}: venue differs from ScholarlyArticle.isPartOf")
            topics = record.get("topics")
            self.require(isinstance(topics, list) and topics and all(isinstance(topic, str) and topic.strip() for topic in topics), f"{context}: topics must be a nonempty list of labels")
            self.require(topics == article.get("keywords"), f"{context}: topics differ from ScholarlyArticle.keywords")
            visible_urls = {urljoin(url, href) for href, label in page.anchors if label}
            source = record.get("abstract_source", "")
            for field in ("abstract_source", "pdf", "bibtex"):
                target = record.get(field, "")
                valid = isinstance(target, str) and urlsplit(target).scheme in ("http", "https") and bool(urlsplit(target).netloc)
                self.require(valid, f"{context}: {field} must be an absolute HTTP(S) URL")
                if valid:
                    self.check_local_link(url, target, context)
            self.require(isinstance(source, str) and source in visible_urls, f"{context}: abstract_source has no labeled link in the HTML paper page")
            source_label = record.get("abstract_source_label")
            if source_label is not None:
                self.require(any(urljoin(url, href) == source and normalized(label) == normalized(source_label) for href, label in page.anchors), f"{context}: abstract_source_label differs from the visible source link")
            self.require(isinstance(source, str) and source and source in self.markdown.get(f"{route}index.md", ""), f"{context}: abstract_source is absent from the Markdown paper page")
            schema_pdfs = [encoding.get("contentUrl") for encoding in nodes(article.get("encoding", {})) if encoding.get("encodingFormat") == "application/pdf"]
            self.require(record.get("pdf") in schema_pdfs and record.get("pdf") in visible_urls, f"{context}: pdf differs from the schema or visible PDF link")
            if page.metadata["citation_pdf_url"]:
                self.require(record.get("pdf") in page.metadata["citation_pdf_url"], f"{context}: pdf differs from citation_pdf_url")
            self.require(record.get("bibtex") == self.url(f"{route}cite.bib"), f"{context}: bibtex must point to the canonical local citation file")

    def check_aliases(self):
        aliases = {
            "projects/siftom/index.html": "project/siftom/",
            "projects/conformal_l2d/index.html": "project/uncertain-defer/",
        }
        for relative, destination in aliases.items():
            page = Page(self.read(relative))
            target = self.url(destination)
            self.require(page.canonicals == [target], f"{relative}: legacy alias canonical must be {target}")
            self.require(page.refresh_targets == [target], f"{relative}: legacy alias must redirect to {target}")
            self.require(self.local_file(target), f"{relative}: alias destination has no built page: {target}")

    def check_crawling(self):
        robots_text = self.read("robots.txt")
        robots = RobotFileParser()
        robots.parse(robots_text.splitlines())
        self.require(bool(re.search(r"^\s*User-agent:\s*\*\s*$", robots_text, re.M | re.I)), "robots.txt: missing wildcard User-agent group")
        discovery_routes = ["", "llms.txt", "sitemap.xml", "projects/", "experience/", "research/", "papers.json"]
        discovery_routes += [route for route in self.pages if route.startswith(("project/", "publication/"))]
        discovery_routes += [path.relative_to(self.root).as_posix() for path in self.root.rglob("*.md")]
        for agent in ("OAI-SearchBot", "Claude-SearchBot", "Claude-User"):
            for route in discovery_routes:
                self.require(robots.can_fetch(agent, self.url(route)), f"robots.txt: {agent} cannot fetch {self.url(route)}")
        self.require(self.url("sitemap.xml") in (robots.site_maps() or []), "robots.txt: missing canonical Sitemap declaration")
        sitemap_text = self.read("sitemap.xml")
        try:
            sitemap = ET.fromstring(sitemap_text)
            locations = [e.text.strip() for e in sitemap.iter() if e.tag.endswith("}loc") and e.text]
            self.require(locations, "sitemap.xml: no URLs found")
            for element in sitemap.iter():
                if element.tag.endswith("}lastmod") and element.text:
                    try:
                        modified = date.fromisoformat(element.text.strip()[:10])
                        self.require(modified <= date.today(), f"sitemap.xml: future lastmod date {element.text}")
                    except ValueError:
                        self.errors.append(f"sitemap.xml: invalid lastmod date {element.text}")
            for url in locations:
                self.require(self.same_origin(url), f"sitemap.xml: noncanonical origin in {url}")
                self.require(self.local_file(url), f"sitemap.xml: URL has no built file: {url}")
                path = urlsplit(url).path
                self.require(not path.startswith(SAMPLE_PREFIXES), f"sitemap.xml: template content leaked into {url}")
                file = self.local_file(url)
                if file and file.suffix == ".html":
                    page = Page(file.read_text(encoding="utf-8"))
                    self.require(page.canonicals == [url] and not page.alias, f"sitemap.xml: {url} is not a canonical page")
            expected_routes = ["", "projects/", "experience/", "research/"]
            expected_routes += [route for route in self.pages if re.fullmatch(r"(?:project|publication)/[^/]+/", route)]
            for route in expected_routes:
                self.require(self.url(route) in locations, f"sitemap.xml: missing {self.url(route)}")
        except ET.ParseError as error:
            self.errors.append(f"sitemap.xml: invalid XML: {error}")
        rss_text = self.read("index.xml")
        try:
            rss = ET.fromstring(rss_text)
            for item in rss.findall("./channel/item"):
                link = item.findtext("link", default="")
                title = item.findtext("title", default="")
                self.require(not urlsplit(link).path.startswith(SAMPLE_PREFIXES), f"index.xml: sample-content item {link}")
                self.require(not any(sample.lower() in title.lower() for sample in SAMPLE_TITLES), f"index.xml: template title {title!r}")
                if link:
                    self.require(self.same_origin(link), f"index.xml: noncanonical item URL {link}")
                    self.check_local_link(self.base, link, "index.xml")
        except ET.ParseError as error:
            self.errors.append(f"index.xml: invalid XML: {error}")

    def run(self):
        self.check_html()
        self.check_markdown()
        self.check_paper_content()
        self.check_aliases()
        self.check_crawling()
        if self.errors:
            print(f"Agent discovery audit FAILED ({len(self.errors)} issues):", file=sys.stderr)
            for error in self.errors:
                print(f"  - {error}", file=sys.stderr)
            return 1
        print(f"Agent discovery audit PASSED: {len(self.pages)} canonical pages, {self.publication_count} papers, 4 projects; full abstract parity, research guide, paper catalog, JSON-LD, citations, Markdown links, legacy aliases, robots, sitemap and RSS checked.")
        return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", nargs="?", default="public", type=Path, help="Hugo production output directory (default: public)")
    parser.add_argument("--base-url", default="https://yiziruifang.com/", help="Expected canonical deployment URL")
    args = parser.parse_args()
    if not args.directory.is_dir():
        parser.error(f"Build directory does not exist: {args.directory}. Run a production Hugo build first.")
    origin = urlsplit(args.base_url)
    if origin.scheme not in ("http", "https") or not origin.netloc or origin.query or origin.fragment:
        parser.error("--base-url must be an absolute HTTP(S) URL without query or fragment")
    return Audit(args.directory, args.base_url).run()


if __name__ == "__main__":
    sys.exit(main())
