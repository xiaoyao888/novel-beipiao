import os, re

files = sorted([f for f in os.listdir('.') if f.startswith('chapter-') and f.endswith('.md') and int(f.split('-')[1].split('.')[0]) > 20])

for fname in files:
    with open(fname, 'r', encoding='utf-8') as fh:
        t = fh.read()

    # Split merged sentences: 。 followed by Chinese char -> 。\n\nChinese
    t = re.sub(r'。([一-鿿])', r'。\n\n\1', t)

    # Split after ！ followed by Chinese
    t = re.sub(r'！([一-鿿])', r'！\n\n\1', t)

    # Split ？ followed by Chinese (real question marks)
    t = re.sub(r'？([一-鿿])', r'？\n\n\1', t)

    # Split after closing quote followed by Chinese (dialogue ending)
    t = re.sub(r'"([一-鿿])', r'"\n\n\1', t)

    # Split before opening quote (dialogue starting)
    t = re.sub(r'([。！？])(\s*)"', r'\1\n\n"', t)

    # Fix chapter title - remove merged content after title
    # Pattern: ## 第XX章 标题内容。more content -> ## 第XX章 标题
    for i in range(2, min(5, len(t.split('\n')))):
        line = t.split('\n')[i]
        if line.startswith('## 第') and '章 ' in line:
            # Find the chapter title end - first 。 or first sentence break
            title_end = re.search(r'章 (.+?)[。]', line)
            if title_end:
                new_title = f'## 第{title_end.group(1)}章 {title_end.group(1).split("章")[-1].strip()}'
                # Actually simpler: just keep up to first period in title
                idx = line.find('。')
                if idx > 0:
                    t = t.replace(line, line[:idx] + '。', 1)

    # Clean up excessive blank lines
    t = re.sub(r'\n{3,}', '\n\n', t)

    with open(fname, 'w', encoding='utf-8') as fh:
        fh.write(t)

print(f'Done: {len(files)} files')
