"""Shared raw-column preview and transparent defaults for every upload reader."""
import numpy as np
from plugins.text_table import suggest_columns


def build_column_preview(reader,max_points=4000):
    group=getattr(reader,'larch_data',None)
    raw=getattr(group,'data',None)
    labels=list(getattr(group,'array_labels',[]) or [])
    if raw is None:
        raw=reader.data
        labels=['energy','reference_mu','sample_mu']
    raw=np.asarray(raw,dtype=float)
    if raw.ndim!=2: return None
    if len(labels)==raw.shape[1] and len(labels)!=raw.shape[0]: raw=raw.T
    if len(labels)!=raw.shape[0]: labels=['column_'+str(i+1) for i in range(raw.shape[0])]
    step=max(1,int(np.ceil(raw.shape[1]/max_points)))
    sampled=raw[:,::step]
    choice=suggest_columns(labels,getattr(reader,'beamline',None))
    names=[str(label).lower() for label in labels]
    reference=dict(reference_enabled='no',reference_a=choice['signal_a'],reference_b=choice['signal_b'],reference_formula='raw')
    ref=next((names.index(name) for name in ('mu_ref','murefer','muref','reference_mu') if name in names),None)
    if ref is not None:
        reference.update(reference_enabled='yes',reference_a=ref,reference_b=ref)
    else:
        for a,b in [('i1','i2'),('itrans','irefer'),('ion1','ion2')]:
            if a in names and b in names:
                reference.update(reference_enabled='yes',reference_a=names.index(a),reference_b=names.index(b),reference_formula='log_ratio')
                break
    if (reference['reference_formula']==choice['formula'] and reference['reference_a']==choice['signal_a']
            and (choice['formula']=='raw' or reference['reference_b']==choice['signal_b'])):
        reference['reference_enabled']='no'
    units=getattr(group,'column_units',[None]*len(labels))
    scans=getattr(group,'scans',[dict(index=0,label='Table 1',points=int(raw.shape[1]),columns=len(labels))])
    return dict(labels=labels,columns=[[float(v) if np.isfinite(v) else None for v in row] for row in sampled],
                defaults=dict({key:choice[key] for key in ['energy','signal_a','signal_b','formula']},**reference),
                profile=choice['profile'],confident=choice['confident'],
                original_points=int(raw.shape[1]),displayed_points=int(sampled.shape[1]),
                units=units,scans=scans,scan_index=int(getattr(reader,'scan_number',0) or 0),
                header=list(getattr(group,'header',[]) or []),
                reading=getattr(group,'read_info',{}))
