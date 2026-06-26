import os, re

files = sorted([f for f in os.listdir('.') if f.startswith('chapter-') and f.endswith('.md') and int(f.split('-')[1].split('.')[0]) > 20])

for fname in files:
    ch = int(fname.split('-')[1].split('.')[0])
    with open(fname, 'r', encoding='utf-8') as fh:
        t = fh.read()

    # Fix garbled section headers
    if ch <= 100:
        t = re.sub(r'^# .+$', '# 第一部：初入京城', t, flags=re.MULTILINE)
    elif ch <= 150:
        t = re.sub(r'^# .+$', '# 第二部：浮沉', t, flags=re.MULTILINE)
    elif ch <= 250:
        t = re.sub(r'^# .+$', '# 第三部：而立之年', t, flags=re.MULTILINE)
    else:
        t = re.sub(r'^# .+$', '# 第四部：AI时代', t, flags=re.MULTILINE)

    # Fix chapter number: if header doesn't have 第XX章, add it
    lines = t.split('\n')
    if len(lines) > 2:
        h2 = lines[2]
        if h2.startswith('## ') and '第' not in h2:
            title = h2[3:].strip()
            lines[2] = f'## 第{ch}章 {title}'
        # Fix 第0章
        if '第0章' in lines[2]:
            lines[2] = lines[2].replace('第0章', '第100章')
        t = '\n'.join(lines)

    # Split long paragraphs - add breaks after period+Chinese
    t = re.sub(r'([。])([一-鿿])', r'\1\n\n\2', t)
    t = re.sub(r'\n{3,}', '\n\n', t)

    with open(fname, 'w', encoding='utf-8') as fh:
        fh.write(t)

print(f'Fixed {len(files)} files')
