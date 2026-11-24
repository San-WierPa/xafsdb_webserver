"""Recover unit-bearing, multi-word table headings without reordering data."""
import re


def recover_column_labels(path, column_count, fallback):
    try:
        with open(path, encoding='utf-8-sig', errors='replace') as stream:
            lines=[]
            for index,line in enumerate(stream):
                if index >= 1000:
                    break
                lines.append(line)
    except OSError:
        return list(fallback)
    for line in reversed(lines):
        cells=re.split(r'\t+| {2,}', line.strip().lstrip('#').strip())
        if len(cells) != column_count:
            continue
        if not any(re.search(r'\benergy\b', cell, re.I) for cell in cells):
            continue
        if not any(re.search(r'\([^)]*\)', cell) for cell in cells):
            continue
        labels=[]
        for cell in cells:
            compact=re.sub(r'\s+', '', cell).lower()
            if compact in ('ln(i0/i1)', 'log(i0/i1)'):
                label='mu_trans'
            elif compact in ('ln(i1/i2)', 'log(i1/i2)'):
                label='mu_ref'
            else:
                label=re.sub(r'\([^)]*\)', '', cell)
                label=re.sub(r'[^a-zA-Z0-9]+', '_', label).strip('_').lower()
            if not label:
                break
            labels.append(label)
        if len(labels)==column_count and len(set(labels))==column_count:
            return labels
    return list(fallback)
