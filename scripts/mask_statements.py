#!/usr/bin/env python3
"""Mask bank statement PDFs, keeping only date, amount, category and merchant/place.

Usage:
    python -I scripts/mask_statements.py [IN_DIR] [OUT_DIR] [--owner "JAN KOWALSKI" ...]

Defaults: IN_DIR=docs/Wyciągi, OUT_DIR=docs/masked. Requires: pip install pdfplumber.

Handles two layouts:
  * monthly statements ("Wyciąg ...") -> statements_masked.csv
  * operations list ("Lista_operacji ...") -> operations_list_masked.csv
Check whether the two describe the same account before combining them: in this
repo the list is a credit card, whose repayments show up in the statements.

Private persons in transfers are replaced by [OSOBA] unless the counterparty
looks like a company (see COMPANY_HINTS: extend it for new recurring payees).
Nothing from the documents is printed: only counts and a self-check result.
"""
import argparse
import csv
import re
import sys
from decimal import Decimal
from pathlib import Path

import pdfplumber

STMT_TX = re.compile(r'^(\d{2}/\d{2}/\d{4})\s+(-?\d{1,3}(?:\.\d{3})*,\d{2})\s*(.*)$')
STMT_REF = re.compile(r'^\w{2}\s+\w{3}\.?:')
LIST_TX = re.compile(r'^(\d{2}\.\d{2}\.\d{4})\s+(.*?)\s*([-+])\s*(\d[\d .]*,\d{2})\s+([A-Z]{3})$')
LIST_ACCT = re.compile(r'\(\*\d{4}\)\s*$')
PAGE_NO = re.compile(r'^\w+ \d+(?: \w+ |/)\d+$')

POSTAL = re.compile(r'\b\d{2}-\d{3}\b')
HOUSE_NO = re.compile(r'\b\d+[A-Za-z]?(?:/\d+[A-Za-z]?)?\b')
HOUSE_END = re.compile(r'\s\d+[A-Za-z]?(?:/\d+[A-Za-z]?)?$')
STREET_PREFIX = r'(?:ul|Ul|UL|al|Al|AL|pl|Pl|os|Os)\.'
STREET = re.compile(r'\b' + STREET_PREFIX + r'\s*[^\d,]*?\d+[A-Za-z]?(?:/\d+[A-Za-z]?)?')
EMAIL = re.compile(r'\S+@\S+')
FLAT = re.compile(r'(?:[^\W\d_]+\.?\s+){1,3}\d+[A-Za-z]?/\d+[A-Za-z]?(?![\d/])')   # "Street Name 6E/7"
PHONE_X = re.compile(r'\+?\d*x{4,}\d*', re.I)                                    # "+48xxxxxx877"
TRANSFER_TYPE = re.compile(r'^(PRZELEW|REALIZACJA PŁATNOŚCI PEOPAY)', re.I)
CAP_WORD = re.compile(r'(?<!^)\b[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+\b')

# A counterparty containing any of these is kept as is; anything else is treated as a private person.
COMPANY_HINTS = re.compile(
    r'S\.A|\bSP\.|Z O\.O|SPÓŁK|SPOLK|\bUAB\b|\bLTD\b|GMBH|FUNDUSZ|URZĄD|URZAD|MINISTERSTWO|BANK|CENTRALA|'
    r'SPÓŁDZIELN|\bPSM\b|UBEZPIECZ|NIERUCHOMO|FINANC|SERVICE|USŁUG|FIRMA|ZAKŁAD|'
    r'AVANQUEST|XTB|AUTOPAY|PAYU|PAYPRO|PPRO|REVOLUT|STELLANTIS|MILENIUM|HESTIA|ERGO|SHED LIVING|'
    r'ENEA|PGE|TAURON|T-MOBILE|ORANGE|MULTISPORT|PRZELEWY24|ALLEGRO|PAYPO', re.I)

# First match wins. Edit freely: (category, regex over upper-cased description).
CATEGORY_RULES = [
    ('Wynagrodzenie', r'WYNAGRODZENIE|PENSJA|SALARY'),
    ('Bankomat', r'BANKOMAT|WYPŁATA|ATM'),
    ('Spożywcze', r'BIEDRONKA|LIDL|ŻABKA|ZABKA|CARREFOUR|KAUFLAND|AUCHAN|DINO|STOKROTKA|LEWIATAN|NETTO|SPOŻYW'),
    ('Paliwo', r'ORLEN|\bBP\b|SHELL|CIRCLE K|MOYA|LOTOS|AMIC'),
    ('Transport', r'UBER|BOLT|JAKDOJADE|\bPKP\b|\bZTM\b|KOLEJE|TAXI|MPK'),
    ('Jedzenie na mieście', r'MCDONALD|\bKFC\b|STARBUCKS|PIZZA|GLOVO|WOLT|PYSZNE|BURGER|RESTAUR|KAWIARNIA|CAFE'),
    ('Subskrypcje', r'NETFLIX|SPOTIFY|HBO|DISNEY|YOUTUBE|APPLE\.COM|GOOGLE|CANVA|OPENAI|ANTHROPIC|MICROSOFT'),
    ('Zakupy online', r'ALLEGRO|AMAZON|ALIEXPRESS|ZALANDO|OLX|TEMU|EMPIK|RTV EURO|MEDIA EXPERT'),
    ('Zdrowie', r'APTEKA|\bDOZ\b|GEMINI|MEDICOVER|LUXMED|ENEL|DENTYST'),
    ('Rachunki', r'\bPGE\b|TAURON|ENEA|ORANGE|\bPLAY\b|T-MOBILE|NETIA|\bUPC\b|VECTRA|PGNIG|GAZ|CZYNSZ'),
    ('Przelew', r'PRZELEW'),
]
CATEGORY_RULES = [(c, re.compile(r, re.I)) for c, r in CATEGORY_RULES]


def read_lines(path):
    with pdfplumber.open(path) as pdf:
        pages = [[l.replace('\xa0', ' ').strip() for l in (p.extract_text() or '').splitlines()] for p in pdf.pages]
    return [[l for l in page if l] for page in pages]


def to_amount(sign, digits):
    value = Decimal(digits.replace(' ', '').replace('.', '').replace(',', '.'))
    return -value if sign == '-' else value


def owner_tokens(kind, pages, extra):
    """Return (name words, address words) of the account holder, learned from the first page."""
    tokens = list(extra)
    first = pages[0]
    addr = set()
    if kind == 'stmt':
        tokens.append(' '.join(w for w in first[0].split() if w.isupper()))
        for line in first[:8]:                       # holder's street line, e.g. "Street Name 6E/7"
            if re.search(r'\d+[A-Za-z]?/\d+[A-Za-z]?', line) and not STMT_TX.match(line):
                addr |= {w.upper() for w in re.findall(r'[^\W\d_]{5,}', line)}
                break
    elif len(first) > 1 and ':' in first[1]:
        tokens.append(first[1].split(':', 1)[1])
    names = set()
    for chunk in tokens:
        for word in re.findall(r'[^\W\d_]{3,}', chunk):
            names.add(word.upper())
    return names, addr


def clean_lines(lines):
    merged = []
    for l in lines:
        postal_split = re.match(r'^-\d{3}\b', l) and re.search(r'\d{2}$', merged[-1] if merged else '')
        street_wrap = merged and re.search(STREET_PREFIX + r'[^\d]*$', merged[-1])
        if postal_split:                 # "00" / "-001"
            merged[-1] += l
        elif street_wrap:                # "ul. Long Name" / "Rest 12"
            merged[-1] += ' ' + l
        else:
            merged.append(l)
    out = []
    for i, l in enumerate(merged):
        nxt = merged[i + 1] if i + 1 < len(merged) else ''
        if '**' in l or not re.search(r'[^\W\d_]', l):   # card-number masks; a single '*' is part of a merchant name
            continue
        if re.search(r'\d(?: ?\d){7,}', l):          # IBAN / account number lines
            continue
        if POSTAL.match(nxt) and HOUSE_END.search(l):  # street line right before postal code
            continue
        m = POSTAL.search(l)
        if m:                                          # drop "street 12" prefix and the postal code, keep city
            h = HOUSE_NO.search(l[:m.start()])
            if h:
                l = l[h.end():m.start()] + ' ' + l[m.end():]
            else:
                l = l[:m.start()] + ' ' + l[m.end():]
        l = FLAT.sub('', STREET.sub('', l)).strip(' ,;')
        if l:
            out.append(l)
    return out


def anonymize_parties(parts, owner_re):
    """Transfers: replace a private counterparty by [OSOBA] and the capitalised words (names) in its title."""
    if len(parts) < 2 or not TRANSFER_TYPE.match(parts[0]):
        return parts
    own = owner_re is not None and len(owner_re.findall(parts[1])) >= 2
    if own or COMPANY_HINTS.search(parts[1]):
        return parts
    return [parts[0], '[OSOBA]'] + [CAP_WORD.sub('[..]', p) for p in parts[2:]]


def mask(text, owner_re, addr_re=None):
    text = EMAIL.sub('', text)
    text = PHONE_X.sub('', text)
    text = re.sub(r'\+\d[\d ]{7,}\d|\b\d{3}[ -]?\d{3}[ -]?\d{3}\b', '', text)
    text = re.sub(r'\d{5,}', '', text)
    text = text.replace('*', ' ')
    if owner_re:
        text = owner_re.sub('[WŁAŚCICIEL]', text)
    if addr_re:
        text = addr_re.sub('[ADRES]', text)
    return re.sub(r'\s+', ' ', text).strip(' |-')


def guess_category(text):
    for category, rx in CATEGORY_RULES:
        if rx.search(text):
            return category
    return 'Inne'


def parse_stmt(pages):
    flat = [l for page in pages for l in page]
    k = next((i for i, l in enumerate(flat) if STMT_TX.match(l)), None)
    if k is None:
        return []
    header = set(flat[:k])
    rows, cur = [], None
    for line in flat[k:]:
        if line in header or PAGE_NO.match(line):
            continue
        m = STMT_TX.match(line)
        if m:
            cur = {'date': m.group(1), 'amount': to_amount('-' if m.group(2).startswith('-') else '+', m.group(2).lstrip('-')),
                   'lines': [m.group(3)] if m.group(3) else [], 'done': False}
            rows.append(cur)
        elif cur and not cur['done']:
            if STMT_REF.match(line):
                cur['done'] = True
            else:
                cur['lines'].append(line)
    out = []
    for r in rows:
        d, mo, y = r['date'].split('/')
        out.append({'date': f'{y}-{mo}-{d}', 'amount': r['amount'], 'currency': 'PLN', 'category': '', 'lines': r['lines']})
    return out


def parse_list(pages):
    first = pages[0]
    k = next((i for i, l in enumerate(first) if LIST_TX.match(l)), None)
    if k is None:
        return []
    last_acct = max(i for i, l in enumerate(first) if LIST_ACCT.search(l))
    drop = set(first[:max(k - 1, 0)]) | set(first[last_acct + 1:])
    rows, buf = [], []
    for page in pages:
        for line in page:
            if line in drop or PAGE_NO.match(line):
                continue
            m = LIST_TX.match(line)
            if m:
                d, mo, y = m.group(1).split('.')
                rows.append({'date': f'{y}-{mo}-{d}', 'amount': to_amount(m.group(3), m.group(4)), 'currency': m.group(5),
                             'category': m.group(2).strip(), 'lines': buf})
                buf = []
            elif LIST_ACCT.search(line):
                buf = []
            else:
                buf.append(line)
    return rows


def words_re(words):
    return re.compile(r'\b(?:' + '|'.join(map(re.escape, sorted(words))) + r')\b', re.I) if words else None


def collect(files, parser, kind, extra_owner):
    parsed, owners, addr = [], set(), set()
    for f in files:
        pages = read_lines(f)
        names, street = owner_tokens(kind, pages, extra_owner)
        owners |= names
        addr |= street
        parsed.append((f, parser(pages)))
    return parsed, owners, addr


def build_rows(parsed, owners, addr):
    rows, report = [], []
    owner_re, addr_re = words_re(owners), words_re(addr)
    for f, items in parsed:
        persons = 0
        for r in items:
            parts = anonymize_parties(clean_lines(r['lines']), owner_re)
            persons += '[OSOBA]' in parts
            desc = mask(' | '.join(parts), owner_re, addr_re)
            cat = mask(r['category'], owner_re, addr_re) or guess_category(desc)
            rows.append({'source': f.name, 'date': r['date'], 'amount': r['amount'], 'currency': r['currency'],
                         'category': cat, 'description': desc})
        report.append((f.name, len(items), persons))
    return rows, report


def self_check(rows, owners, addr):
    checks = {
        '5+ digits': re.compile(r'\d{5,}'), 'email': re.compile(r'@'), 'star': re.compile(r'\*'),
        'postal code': POSTAL, 'street': STREET, 'flat number': FLAT, 'masked phone': PHONE_X,
    }
    if owners:
        checks['owner'] = words_re(owners)
    if addr:
        checks['owner address'] = words_re(addr)
    bad = {name: sum(1 for r in rows if rx.search(r['description'] + ' ' + r['category'])) for name, rx in checks.items()}
    return {k: v for k, v in bad.items() if v}


def write(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8-sig') as fh:
        w = csv.DictWriter(fh, fieldnames=['source', 'date', 'amount', 'currency', 'category', 'description'])
        w.writeheader()
        w.writerows(sorted(rows, key=lambda r: (r['date'], r['source'])))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('in_dir', nargs='?', default='docs/Wyciągi')
    ap.add_argument('out_dir', nargs='?', default='docs/masked')
    ap.add_argument('--owner', action='append', default=[], help='extra name/word to mask (repeatable)')
    args = ap.parse_args()

    files = sorted(Path(args.in_dir).glob('*.pdf'))
    lists = [f for f in files if f.name.startswith('Lista')]
    stmts = [f for f in files if f not in lists]
    groups = [('wyciągi', stmts, parse_stmt, 'stmt', 'statements_masked.csv'),
              ('lista operacji', lists, parse_list, 'list', 'operations_list_masked.csv')]
    collected, owners, addr = [], set(), set()
    for label, group, parser, kind, name in groups:
        if group:
            parsed, found, street = collect(group, parser, kind, args.owner)
            owners |= found
            addr |= street
            collected.append((label, group, parsed, name))
    failed = False
    for label, group, parsed, name in collected:
        rows, report = build_rows(parsed, owners, addr)
        write(Path(args.out_dir) / name, rows)
        print(f'[{label}] pliki: {len(group)}, transakcje: {len(rows)}, tokeny właściciela: {len(owners)}, słowa adresu: {len(addr)}')
        for fname, n, persons in report:
            print(f'    {n:4d}  (osoby zamaskowane: {persons:3d})  {fname}')
        problems = self_check(rows, owners, addr)
        if problems or not rows:
            failed = True
            print(f'    UWAGA: test kontrolny wykrył resztki danych: {problems or "brak transakcji"}')
        else:
            print('    test kontrolny: OK')
    sys.exit(1 if failed else 0)


if __name__ == '__main__':
    main()
