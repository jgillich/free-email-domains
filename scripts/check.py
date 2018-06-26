import json
import sys

import dns.resolver
import dns.exception


def _load(fn, from_json=False):
    with open(fn) as f:
        if from_json:
            return json.load(f)
        else:
            return [l.strip() for l in f]


domains = _load('hubspot-free-email-domains.txt')
sorted_domains = sorted({d.lower() for d in domains if d})

if domains != sorted_domains:
    print('Hubspot domains are not sorted/unique!? Compare with /tmp/sorted-free-email-domains.txt')
    with open('/tmp/sorted-free-email-domains.txt', 'w') as f:
        for e in sorted_domains:
            f.write(e + '\n')
    sys.exit(1)

domains = _load('free-email-domains.txt')
sorted_domains = sorted({d.lower() for d in domains if d})

if domains != sorted_domains:
    print('Domains are not sorted/unique!? Compare with /tmp/sorted-free-email-domains.txt')
    with open('/tmp/sorted-free-email-domains.txt', 'w') as f:
        for e in sorted_domains:
            f.write(e + '\n')
    sys.exit(1)


disposable = set(_load('tmp/disposable-email-domains/index.json', from_json=True))
assert 'mailinator.com' in disposable
disposable = [d for d in domains if d in disposable]
if disposable:
    print('Disposable domains: %s' % disposable)
    sys.exit(2)


disposable_wildcard = _load('tmp/disposable-email-domains/wildcard.json', from_json=True)
disposable = [d for d in domains if any(w in d for w in disposable_wildcard)]
if disposable:
    print('Disposable domains (wildcards): %s' % disposable)
    sys.exit(3)


no_mx = []
for d in domains:
    try:
        dns.resolver.query(d, 'MX')
    except dns.exception.DNSException:
        no_mx.append(d)
if no_mx:
    print('Domains without MX records: %s' % no_mx)
    sys.exit(4)
