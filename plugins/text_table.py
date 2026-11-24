"""Content-based numeric XAS table reader, independent of header row counts.

This reader preserves numbered columns and scan boundaries. It does not decide
whether a spectrum passes scientific QC, or evaluate expressions from a header.
"""
import csv
import re
from bisect import bisect_right
from collections import Counter
from pathlib import Path
from types import SimpleNamespace
import numpy as np


def decode_text(raw):
    if not raw:
        raise ValueError('The selected file is empty.')
    if raw[:4] == b'\x00\x05\x16\x07':
        raise ValueError('This is a filesystem metadata sidecar, not a measurement.')
    if raw.startswith((b'\xff\xfe', b'\xfe\xff')):
        return raw.decode('utf-16'), 'utf-16'
    if b'\x00' in raw[:4096]:
        if raw[:4096].count(b'\x00') > len(raw[:4096]) // 4:
            for encoding in ['utf-16-le','utf-16-be']:
                try:
                    text=raw.decode(encoding)
                    if '\n' in text and '\x00' not in text:
                        return text,encoding
                except UnicodeError: pass
        raise ValueError('This file contains binary data, not a supported numeric text table.')
    for encoding in ['utf-8-sig','cp1252','latin-1']:
        try: return raw.decode(encoding),encoding
        except UnicodeError: pass
    raise ValueError('The text encoding could not be decoded.')


def split_cells(line):
    """Support decimal-comma tables without confusing them with comma CSV."""
    line=line.strip().rstrip('\\').strip()
    if ';' in line:
        return next(csv.reader([line],delimiter=';')), ';'
    if ',' in line:
        words=line.split()
        if len(words)>1 and all(re.fullmatch(r'[+-]?(?:\d+(?:,\d*)?|,\d+)(?:[eEdD][+-]?\d+)?',w) for w in words):
            return words,'whitespace'
        return next(csv.reader([line])), ','
    return re.split(r'\s+',line),'whitespace'


def numeric_row(line):
    stripped=line.strip()
    if not stripped or stripped.startswith(('#','!',';','%','@')):
        return None
    stripped=re.split(r'\s+[#!%]',stripped,maxsplit=1)[0]
    cells,delimiter=split_cells(stripped)
    if len(cells)<2: return None
    values=[];numeric=0;unknown=0
    for cell in cells:
        token=cell.strip().strip('"\'')
        if not token or token.lower() in {'na','n/a','null','none','--','***','*****','1.#qnan','1.#ind'}:
            values.append(float('nan'));continue
        try:
            values.append(float(token.replace('D','E').replace('d','e').replace(',','.')))
            numeric+=1
        except ValueError:
            values.append(float('nan'));unknown+=1
    if numeric<1 or (unknown and (numeric<2 or numeric < len(cells)/2)):
        return None
    return values,delimiter


def normalize_label(label):
    compact=re.sub(r'\s+','',label).lower()
    if compact in {'ln(i0/i1)','log(i0/i1)'}: return 'mu_trans'
    if compact in {'ln(i1/i2)','log(i1/i2)'}: return 'mu_ref'
    cleaned=re.sub(r'\([^)]*\)|\[[^]]*\]','',label)
    cleaned=re.sub(r'\s*/\s*(?:kev|ev|a|counts|s|deg)\b.*$','',cleaned,flags=re.I)
    return re.sub(r'[^a-z0-9]+','_',cleaned.lower()).strip('_') or 'column'


def label_unit(label):
    if re.search(r'(?i)(?:\b|_)kev(?:\b|_)',label): return 'keV'
    if re.search(r'(?i)(?:\b|_)ev(?:\b|_)',label): return 'eV'
    return None


def column_headings(header,count):
    numbered={};declared=[]
    for line in header:
        match=re.match(r'^\s*#\s*Column\.(\d+)\s*:\s*(.+)$',line,re.I)
        if match:
            parts=match.group(2).strip().split()
            numbered[int(match.group(1))-1]=(parts[0],label_unit(match.group(2)))
        match=re.match(r'^\s*#\s*#?\s*(\d+)\s*-\s*(.+?)\s*$',line)
        if match: numbered[int(match.group(1))]=(match.group(2),label_unit(match.group(2)))
    if numbered and set(numbered)==set(range(count)):
        return [normalize_label(numbered[i][0]) for i in range(count)],[numbered[i][1] for i in range(count)],'numbered header',[]
    candidates=[]
    for order,line in enumerate(header):
        cleaned=re.sub(r'^\s*[#!%;]+\s*','',line).strip()
        if not cleaned: continue
        is_spec=bool(re.match(r'^L\s+',cleaned))
        if is_spec: cleaned=re.sub(r'^L\s+','',cleaned)
        if re.match(r'^[PONSDHUM]\d*\s+[-+\d]',cleaned): continue
        if re.match(r'^[A-Za-z][\w. ]*\s*[:=]',cleaned): continue
        alternatives=[]
        if '\t' in cleaned: alternatives.append(re.split(r'\t+',cleaned))
        if ';' in cleaned: alternatives.append(next(csv.reader([cleaned],delimiter=';')))
        if ',' in cleaned: alternatives.append(next(csv.reader([cleaned])))
        alternatives.append(re.split(r' {2,}',cleaned))
        compact_units=re.sub(r'\s+(?=[(\[])','',cleaned)
        compact_units=re.sub(r'\s*/\s*(keV|eV)\b',r'/\1',compact_units,flags=re.I)
        alternatives.append(compact_units.split())
        alternatives.append(cleaned.split())
        for cells in alternatives:
            cells=[cell.strip() for cell in cells if cell.strip()]
            if len(cells)<2 or not any(re.search(r'[A-Za-z]',c) for c in cells):continue
            normalized=[normalize_label(cell) for cell in cells]
            looks_like_table=is_spec or any(re.search(r'(?i)energy|energies|eneenc|zapenergy|\bi0\b|\bi1\b|\bmu\b|\bposx\b|^e\s*/',c) for c in cells)
            if not looks_like_table: continue
            if len(cells)!=count:
                if is_spec: declared.append(len(cells))
                continue
            score=100*int(is_spec)+20*int(any(label_unit(c) for c in cells))+order/1000
            candidates.append((score,normalized,[label_unit(c) for c in cells]))
    if candidates:
        _,labels,units=max(candidates,key=lambda item:item[0])
        warnings=[]
        if len(set(labels))!=len(labels): warnings.append('Duplicate column names are preserved; select numbered columns.')
        return labels,units,'table header',warnings
    warnings=['Column labels could not be matched reliably; use the numbered columns and the original header.']
    if declared: warnings.append('Declared column count differs from the numeric table.')
    return ['column_'+str(i+1) for i in range(count)],[None]*count,'numbered columns',warnings


def _scan_chunks(lines):
    starts=[i for i,line in enumerate(lines) if re.match(r'^\s*#S\s+\S+',line)]
    if not starts:
        numeric=[(i,len(parsed[0])) for i,line in enumerate(lines) if (parsed:=numeric_row(line)) is not None]
        positions=[i for i,_ in numeric]
        headings=[]
        for i,line in enumerate(lines):
            if not re.search(r'(?i)energy|energies|eneenc|zapenergy|^\s*#?L\s',line):continue
            next_row=bisect_right(positions,i)
            if next_row>=len(numeric):continue
            if column_headings([line],numeric[next_row][1])[2]=='numbered columns':continue
            if headings and numeric[bisect_right(positions,headings[-1])][0]>i:headings[-1]=i
            else:headings.append(i)
        if len(headings)>1:
            prefix=lines[:headings[0]]
            return [('Table '+str(index+1),prefix+lines[start:(headings[index+1] if index+1<len(headings) else len(lines))],start-len(prefix))
                    for index,start in enumerate(headings)]
        return [(None,lines,0)]
    global_header=lines[:starts[0]]
    return [(lines[start].strip(),global_header+lines[start:(starts[index+1] if index+1<len(starts) else len(lines))],start-len(global_header))
            for index,start in enumerate(starts)]


def read_text_table(path,scan=0):
    path=Path(path)
    text,encoding=decode_text(path.read_bytes())
    lines=text.splitlines()
    tables=[]
    skipped=[]
    for title,chunk,offset in _scan_chunks(lines):
        rows=[];mca=False
        for number,line in enumerate(chunk):
            stripped=line.strip()
            if mca:
                mca=stripped.endswith('\\');continue
            if stripped.startswith('@'):
                mca=stripped.endswith('\\');continue
            parsed=numeric_row(line)
            if parsed is not None: rows.append((number,parsed[0],parsed[1]))
        if not rows:
            skipped.append(title or 'table');continue
        widths=Counter(len(values) for _,values,_ in rows)
        width=max(widths,key=lambda n:(widths[n],n))
        valid=[row for row in rows if len(row[1])==width]
        if len(valid)<2:
            skipped.append(title or 'table');continue
        first=valid[0][0]
        header=chunk[:first]
        labels,units,label_method,warnings=column_headings(header,width)
        if label_method=='numbered columns':
            runs=[]
            for row in valid:
                if not runs or row[0]>runs[-1][-1][0]+1: runs.append([])
                runs[-1].append(row)
            main=max(runs,key=len)
            if main[0][0]>first:
                candidate=column_headings(chunk[:main[0][0]],width)
                if candidate[2]!='numbered columns':
                    first=main[0][0];header=chunk[:first]
                    valid=[row for row in valid if row[0]>=first]
                    labels,units,label_method,warnings=candidate
                    warnings.append('Numeric preamble lines before the table heading were kept as header metadata.')
        inconsistent=len(rows)-len(valid)
        if inconsistent: warnings.append(str(inconsistent)+' inconsistent-width rows were excluded; no values were shifted between columns.')
        data=np.asarray([row[1] for row in valid],dtype=float).T
        tables.append(dict(data=data,labels=labels,units=units,header=header,title=title or 'Table 1',
                           first_line=offset+first+1,label_method=label_method,warnings=warnings,
                           inconsistent_rows=inconsistent,delimiter=Counter(row[2] for row in valid).most_common(1)[0][0]))
    if not tables:
        raise ValueError('No numeric measurement table was found. The file may be an empty capture, a header-only file, or ordinary text.')
    try: index=int(scan or 0)
    except (ValueError,TypeError): raise ValueError('Choose a numbered scan from the file.')
    if index<0 or index>=len(tables): raise ValueError('The selected scan is outside this file.')
    chosen=tables[index]
    scans=[dict(index=i,label=item['title'],points=item['data'].shape[1],columns=item['data'].shape[0]) for i,item in enumerate(tables)]
    info=dict(format='SPEC' if any(re.match(r'^\s*#S\s+\S+',line) for line in lines) else 'numeric text',
              encoding=encoding,delimiter=chosen['delimiter'],first_data_line=chosen['first_line'],
              header_lines=len(chosen['header']),label_method=chosen['label_method'],
              warnings=chosen['warnings'],excluded_inconsistent_rows=chosen['inconsistent_rows'],
              skipped_empty_scans=len(skipped),scan_index=index,scan_label=chosen['title'])
    group=SimpleNamespace(data=chosen['data'],array_labels=chosen['labels'],header=chosen['header'],
                          column_units=chosen['units'],scans=scans,read_info=info)
    for label,values in zip(group.array_labels,group.data):
        if not hasattr(group,label): setattr(group,label,values)
    return group


def suggest_columns(labels,beamline=None):
    """Suggest named signals; ambiguous tables remain available for review."""
    names=[str(label).lower().replace('-','_') for label in labels]
    def find(*aliases):
        return next((names.index(alias) for alias in aliases if alias in names),None)
    energy=find('energy_cenc','energy_enc','e_enc','enc_energy','eneenc','zapenergy','energy','energies_ev','energy_ev','photon_energy','mono_energy','emono','energy_step','shifted_energy','shifted','e','enrgy')
    if energy is None and beamline in {'PETRA III Extension Beamline P64','SLS'}:energy=find('position','posx')
    mu=find('mu_trans','mutrans','xmu','mu','absorption','absorption_coeff','absorpion_coeff','normalized','normalised','mux','xas_trans')
    i0=find('i0','incident','incident_intensity');i1=find('i1','itrans','it','transmission');i2=find('i2','irefer','iref')
    if energy is None and len(labels)==2: energy=0
    if mu is not None:
        a,b,formula,profile=mu,mu,'raw','Absorption column'
    elif i0 is not None and i1 is not None:
        a,b,formula,profile=i0,i1,'log_ratio','Transmission: ln(I0 / I1)'
    elif find('mon') is not None and find('ion1') is not None:
        a,b,formula,profile=find('mon'),find('ion1'),'log_ratio','Transmission: ln(Mon / Ion1)'
    elif find('vfc02') is not None and find('vfc03') is not None:
        a,b,formula,profile=find('vfc02'),find('vfc03'),'log_ratio','Legacy transmission channels: review the header'
    elif i1 is not None and i2 is not None:
        a,b,formula,profile=i1,i2,'log_ratio','Reference transmission: ln(I1 / I2)'
    elif find('mu_ref','murefer','muref') is not None:
        a=find('mu_ref','murefer','muref');b=a;formula='raw';profile='Reference absorption column'
    else:
        a=next((i for i in range(len(labels)) if i!=energy),0);b=a;formula='raw'
        profile='Choose the energy and signal columns from the header'
    confident=energy is not None and (mu is not None or (i0 is not None and i1 is not None) or
                                      (find('mon') is not None and find('ion1') is not None) or len(labels)==2)
    used=[energy,a]+([b] if formula!='raw' else [])
    confident=confident and all(index is not None and names.count(names[index])==1 for index in used)
    return dict(energy=energy if energy is not None else 0,signal_a=a,signal_b=b,formula=formula,
                profile=profile,confident=confident)
