"""Extract the pages.dev enrollment popup (markup, CSS rules, scripts) from a pages.dev index.html snapshot.
Source: gitteromri-ux/lla-course-checkout, branch master, dist/index.html. Run: python3 extract.py <pagesdev index.html> <outdir>"""
import re, sys, json
src, out = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()

def element(s, i):
    tag = re.match(r'<(\w+)', s[i:]).group(1); depth = 0
    for m in re.finditer(r'<(/?)%s\b[^>]*>' % tag, s[i:]):
        depth += -1 if m.group(1) else 1
        if depth == 0: return s[i:i + m.end()]
i = s.find('id="enrollModal"'); st = s.rfind('<', 0, i)
open(out + '/modal.html', 'w').write(element(s, st))

SEL = re.compile(r'\.em-|#enrollModal|#em[A-Z]|\.pp-|lla-em-open|#dp[A-Z]|\.dp-|lla-r15|\.lla-hide|#pp\b|\.em\b')
def rules(css):
    """yield (prelude, body, is_at) at top level with brace matching"""
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S); i = 0; n = len(css)
    while i < n:
        j = css.find('{', i)
        if j < 0: break
        pre = css[i:j].strip(); depth = 0; k = j
        while k < n:
            if css[k] == '{': depth += 1
            elif css[k] == '}':
                depth -= 1
                if depth == 0: break
            k += 1
        yield pre, css[j + 1:k]
        i = k + 1
def pick(css):
    outp = []
    for pre, body in rules(css):
        if pre.startswith('@media') or pre.startswith('@supports'):
            inner = pick(body)
            if inner: outp.append(pre + '{' + inner + '}')
        elif pre.startswith('@keyframes'):
            name = pre.split()[1] if len(pre.split()) > 1 else ''
            outp.append(('KF', name, pre + '{' + body + '}'))
        elif SEL.search(pre):
            outp.append(pre + '{' + body + '}')
    # keyframes kept only if referenced later
    return '\n'.join(x for x in outp if isinstance(x, str))
blocks = [m.group(1) for m in re.finditer(r'<style\b[^>]*>(.*?)</style>', s, flags=re.S)]
css = '\n'.join(pick(b) for b in blocks)
# keyframes referenced by the picked rules
kf_all = {}
for b in blocks:
    for m in re.finditer(r'@keyframes\s+([\w-]+)\s*\{', b):
        st2 = m.start(); depth = 0; k = m.end() - 1
        while k < len(b):
            if b[k] == '{': depth += 1
            elif b[k] == '}':
                depth -= 1
                if depth == 0: break
            k += 1
        kf_all[m.group(1)] = b[st2:k + 1]
used = [n for n in kf_all if re.search(r'animation[^;{}]*\b' + re.escape(n) + r'\b', css)]
css += '\n' + '\n'.join(kf_all[n] for n in used)
# custom properties used by the picked rules, scoped to the popup with their pages.dev :root values
root_vars = {}
for b in blocks:
    for m in re.finditer(r':root\s*\{([^}]*)\}', b):
        for d in m.group(1).split(';'):
            if ':' in d and d.strip().startswith('--'):
                k, v = d.split(':', 1); root_vars[k.strip()] = v.strip()
need = sorted(set(re.findall(r'var\((--[\w-]+)', css)))
scoped = '#enrollModal{' + ';'.join(f'{k}:{root_vars[k]}' for k in need if k in root_vars) + '}'
open(out + '/modal.css', 'w').write(scoped + '\n' + css)
scripts = [(m.group(1), m.group(2)) for m in re.finditer(r'<script\b([^>]*)>(.*?)</script>', s, flags=re.S)]
keep = []
for a, b in scripts:
    if 'src=' in a: continue
    if re.search(r"getElementById\('(emCcDial|emDate|enrollModal)'\)|id\('pp'\)|__llaPaintPlan", b) and not re.search(r"DEADLINE|lla-slider|sliders|Safari fallbacks|heroWatch|real-user tap audit|lla_promo_seen", b):
        keep.append(b)
open(out + '/modal-scripts.json', 'w').write(json.dumps(keep, indent=0))
print('modal', len(open(out + '/modal.html').read()), 'css', len(css), 'vars', len(need), 'missing vars', [k for k in need if k not in root_vars], 'keyframes', used, 'scripts', [len(x) for x in keep])
