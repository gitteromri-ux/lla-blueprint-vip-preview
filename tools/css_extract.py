"""Pull the CSS rules whose selectors mention given tokens, keeping @media/@supports wrappers and @keyframes by name."""
import re


def _blocks(s):
    i, n = 0, len(s)
    while i < n:
        j = s.find('{', i)
        if j < 0:
            return
        d, k = 0, j
        while k < n:
            if s[k] == '{':
                d += 1
            elif s[k] == '}':
                d -= 1
                if d == 0:
                    break
            k += 1
        yield re.sub(r'/\*.*?\*/', '', s[i:j], flags=re.S).strip(), s[j + 1:k], s[i:k + 1]
        i = k + 1


def extract(css, tokens, keyframes=()):
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    out = []
    for sel, body, whole in _blocks(css):
        if sel.startswith('@media') or sel.startswith('@supports'):
            inner = extract(body, tokens, keyframes)
            if inner.strip():
                out.append(sel + '{' + inner + '}')
        elif sel.startswith('@keyframes') or sel.startswith('@-webkit-keyframes'):
            if any(k in sel for k in keyframes):
                out.append(whole.strip())
        elif sel.startswith('@'):
            continue
        else:
            parts = [p.strip() for p in sel.split(',') if any(t in p for t in tokens)]
            if parts:
                out.append(','.join(parts) + '{' + body.strip() + '}')
    return '\n'.join(out)
