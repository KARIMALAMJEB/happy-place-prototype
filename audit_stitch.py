#!/usr/bin/env python3
"""Audit des maquettes Stitch Happy Place (charte Corporate).

Usage :  python3 audit_stitch.py DOSSIER_EXPORT [rapport.md]
Parcourt tous les code.html du dossier (sous-dossiers compris), ne depend que de
la bibliotheque standard. Produit un rapport texte court a coller dans Claude.
"""
import re
import sys
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path

# Palette de la charte (hex en majuscules, sans #)
PALETTE = {
    "F5F4F1", "CDCDD1", "232428", "68686D", "28282D", "F9F8F5", "C99695",
    "F5D5D4", "F8DDDC", "F0D0BC", "482A1D", "C2272D", "FED2CD", "72020E",
    "298646", "DCEFE1", "14522A", "55555A", "EEEDEA", "E6E4E1", "D9822B",
    "FFFFFF", "000000",
}
DARK = {"28282D", "232428", "000000"}
BANNED = [
    "cockpit", "intranet", "point bloquant", "points bloquants", "sla",
    "ldap", "[!]", "[…]", "[✓]", "[✕]", "[×]", "[x]", "a. lefebvre",
    "product design", "réf.", "luxembourg", "benelux", "poste 412",
    "mode lecture seule", "gestion contenus", "signaler comme bloquante",
    "ce n'est plus bloquant", "critique", "standard",
]
EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2705\u274c\u2728\u2b50]")
HEX = re.compile(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")


def norm_hex(h):
    h = h.upper()
    return "".join(c * 2 for c in h) if len(h) == 3 else h


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []          # (tag, class, skip_text)
        self.controls = []       # dict(label, cls)
        self.cur = None
        self.skip = 0
        self.imgs = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get("class", "") or ""
        if tag == "img":
            self.imgs.append(a.get("alt", ""))
        void = tag in ("img", "br", "input", "meta", "link", "hr")
        is_icon = "material" in cls
        if tag in ("button", "a") and self.cur is None:
            self.cur = {"cls": cls, "label": [], "tag": tag, "depth": len(self.stack)}
        if not void:
            self.stack.append((tag, cls, is_icon))
            if is_icon:
                self.skip += 1

    def handle_endtag(self, tag):
        if not self.stack:
            return
        # depile jusqu'au tag correspondant
        while self.stack:
            t, cls, is_icon = self.stack.pop()
            if is_icon:
                self.skip -= 1
            if self.cur is not None and len(self.stack) == self.cur["depth"] and t == self.cur["tag"]:
                label = re.sub(r"\s+", " ", " ".join(self.cur["label"])).strip().upper()
                self.cur["label"] = label
                self.controls.append(self.cur)
                self.cur = None
            if t == tag:
                break

    def handle_data(self, data):
        if "<script" in data or self.skip:
            return
        d = data.strip()
        if not d:
            return
        # ignore le contenu de <script>/<style> (heuristique simple)
        if self.stack and self.stack[-1][0] in ("script", "style"):
            return
        self.text.append(d)
        if self.cur is not None:
            self.cur["label"].append(d)


BRAND = {"anthracite": "28282D", "rose": "C99695", "ecru": "F5F4F1", "red": "C2272D",
         "white": "FFFFFF", "black": "000000"}


def resolve(tok):
    m = re.search(r"\[#([0-9a-fA-F]{3,6})\]", tok)
    if m:
        return norm_hex(m.group(1))
    m = re.search(r"brand-([a-z]+)", tok)
    if m and m.group(1) in BRAND:
        return BRAND[m.group(1)]
    if tok.endswith("-white"):
        return "FFFFFF"
    if tok.endswith("-black"):
        return "000000"
    if "transparent" in tok:
        return "aucun"
    return tok.split("-", 1)[-1]


def signature(cls):
    """Fond + bordure d'un bouton (hors survol), en hex."""
    fill, border = "aucun", "aucune"
    for tok in cls.split():
        if ":" in tok:
            continue
        if tok.startswith("bg-"):
            fill = resolve(tok)
        elif tok.startswith("border-") and not re.match(r"border-(\d|\[\d|[xytblr]-|[xytblr]$)", tok):
            border = resolve(tok)
    return f"fond {fill} / bordure {border}"


NAV = ("TABLEAU DE BORD", "ACTUALITÉS", "DEMANDES", "INDICATEURS", "BOÎTE À OUTILS", "ANNUAIRE",
       "ENTREPRISE", "MON ÉQUIPE", "MON SUIVI", "TOUTES", "BLOQUANTES", "NON BLOQUANTES",
       "À VALIDER", "SUPERVISION", "BLOQUANTE", "NON BLOQUANTE")


def is_nav(label):
    return any(label.startswith(n) for n in NAV) or bool(re.search(r"\d", label))


def audit(path):
    src = path.read_text(encoding="utf-8", errors="ignore")
    page = Page()
    page.feed(src)
    issues = []

    body = re.sub(r"<script.*?</script>", "", src, flags=re.S | re.I)
    # couleurs hors charte
    hexes = defaultdict(int)
    for m in HEX.finditer(body):
        hexes[norm_hex(m.group(1))] += 1
    off = {h: n for h, n in hexes.items() if h not in PALETTE}
    if off:
        issues.append(("A corriger", "Couleurs hors charte : " + ", ".join(f"#{h} x{n}" for h, n in sorted(off.items(), key=lambda x: -x[1])[:12])))

    # boutons a fond sombre
    dark_btn = []
    for c in page.controls:
        hs = [norm_hex(m.group(1)) for m in re.finditer(r"bg-\[#([0-9a-fA-F]{3,6})\]", " ".join(t for t in c["cls"].split() if ":" not in t))]
        if any(h in DARK for h in hs) or re.search(r"(^|\s)bg-(black|brand-anthracite)(\s|$)", c["cls"]):
            dark_btn.append(c["label"] or "(sans libelle)")
    if len(dark_btn) > 1:
        issues.append(("Bloquant jury", f"{len(dark_btn)} elements cliquables a fond noir (1 seul autorise) : " + " | ".join(sorted(set(dark_btn))[:10])))

    if re.search(r"(^|[\s\"'])rounded(-(sm|md|lg|xl|2xl|3xl|full))?(?=[\s\"'])", body):
        issues.append(("A corriger", "Angles arrondis (rounded-*) : charte = angles droits"))
    if re.search(r"(^|[\s\"'])shadow(-[a-z0-9\[\]#,_]+)?(?=[\s\"'])", body):
        issues.append(("A corriger", "Ombres (shadow-*) : interdites"))
    if re.search(r"bg-gradient|linear-gradient|radial-gradient", body):
        issues.append(("A corriger", "Degrades : interdits"))
    small = sorted(set(re.findall(r"text-\[(\d+(?:\.\d+)?)px\]", body)), key=float)
    small = [s for s in small if float(s) < 12]
    if small:
        issues.append(("A corriger", "Texte sous 12 px : " + ", ".join(s + "px" for s in small)))

    alltext = " ".join(page.text).lower()
    found = [w for w in BANNED if w in alltext]
    if found:
        issues.append(("A corriger", "Mots a verifier : " + ", ".join(found)))
    if EMOJI.search(" ".join(page.text)):
        issues.append(("A corriger", "Emoji present"))
    if re.search(r"\bimg\b", " ".join(page.text).lower()):
        issues.append(("A corriger", "Le mot « img » est affiche (image absente)"))
    if any(a for a in page.imgs):
        issues.append(("Detail", "Images avec texte alternatif (verifier qu'il ne s'affiche pas si l'image manque)"))
    nb_buttons = len(page.controls)
    return issues, page.controls, nb_buttons


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    root = Path(sys.argv[1])
    files = sorted(root.rglob("code.html"))
    if not files:
        print("Aucun code.html trouve dans", root)
        sys.exit(1)
    out = [f"# Audit Stitch : {len(files)} ecran(s)\n"]
    by_label = defaultdict(lambda: defaultdict(set))
    summary = []
    for f in files:
        name = f.parent.name
        issues, controls, nb = audit(f)
        for c in controls:
            if c["label"] and len(c["label"]) < 45 and not is_nav(c["label"]):
                by_label[c["label"]][signature(c["cls"])].add(name)
        order = {"Bloquant jury": 0, "A corriger": 1, "Detail": 2}
        issues.sort(key=lambda x: order[x[0]])
        summary.append((name, issues, nb))
    out.append("## 1. Problemes par ecran\n")
    for name, issues, nb in summary:
        out.append(f"### {name} ({nb} boutons/liens)")
        if not issues:
            out.append("- RAS sur les controles automatiques")
        for sev, msg in issues:
            out.append(f"- [{sev}] {msg}")
        out.append("")
    out.append("## 2. Un meme libelle de bouton avec des couleurs differentes\n")
    n = 0
    for label, sigs in sorted(by_label.items()):
        if len(sigs) > 1:
            n += 1
            out.append(f"- **{label}**")
            for sig, screens in sigs.items():
                out.append(f"  - {sig}  ->  {', '.join(sorted(s[:28] for s in screens))}")
    if n == 0:
        out.append("- Aucun (a verifier visuellement quand meme)")
    report = "\n".join(out)
    dest = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("rapport_audit_stitch.md")
    dest.write_text(report, encoding="utf-8")
    print(report)
    print(f"\n(rapport enregistre dans {dest})")


if __name__ == "__main__":
    main()
