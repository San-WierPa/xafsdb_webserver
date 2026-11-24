"""One column mapping for QC preview and final submission."""
import hashlib
from pathlib import Path
from django.core import signing

FIELD_MAP=(('energy','QC Energy Column'),('signal_a','QC Signal A'),('signal_b','QC Signal B'),
    ('formula','QC Formula'),('scan','QC Scan'),('energy_unit','QC Energy Unit'),
    ('reference_enabled','QC Reference Enabled'),('reference_a','QC Reference A'),
    ('reference_b','QC Reference B'),('reference_formula','QC Reference Formula'))
DEFAULTS=dict(scan='0',energy_unit='auto',reference_enabled='no',reference_formula='raw')
SALT='refxas.confirmed-columns.v1'

def selection_from_form(form):
    if form.get('Use Column Selection')!='yes':return None
    return {key:form.get(field,DEFAULTS.get(key,'')) for key,field in FIELD_MAP}

def selection_from_request(form):
    return {key:form.get(key,DEFAULTS.get(key,'')) for key,_ in FIELD_MAP}

def _canonical(form):
    selection=selection_from_form(form)
    fields={'selection':selection,'Source':form.get('Source','SYNCHROTRON'),
            'Element':form.get('Element',''),'Edge':form.get('Edge','')}
    for key in ('E_range_min','E_range_max'):
        value=form.get(key)
        try:fields[key]=float(value) if value not in (None,'') else None
        except (ValueError,TypeError):raise ValueError('The energy range is invalid. Apply columns again.')
    return fields

def sign_qc_result(path,result,selection=None):
    form={field:str(selection.get(key,DEFAULTS.get(key,''))) for key,field in FIELD_MAP} if selection else {}
    form.update({'Use Column Selection':'yes' if selection else 'no','Source':result['source'],
        'Element':result['element'],'Edge':result['edge'],'E_range_min':result['energy_min'],'E_range_max':result['energy_max']})
    payload=dict(filename=Path(path).name,digest=result.get('input_digest') or hashlib.sha256(Path(path).read_bytes()).hexdigest(),fields=_canonical(form))
    return signing.dumps(payload,salt=SALT,compress=True)

def initial_qc_state(path,result):
    if not result['available']:return {'ready':False}
    return dict(ready=True,confirmation=sign_qc_result(path,result),source=result['source'],
        element=result['element'],edge=result['edge'],energy_min=result['energy_min'],energy_max=result['energy_max'])

def validate_applied_qc(form, *, path=None):
    """Reject unconfirmed edits and files replaced since the displayed QC."""
    try:payload=signing.loads(form.get('QC Confirmation',''),salt=SALT,max_age=86400)
    except signing.BadSignature:
        raise ValueError('QC confirmation is missing or expired. Reload the measurement or apply columns again.')
    filename=Path(form.get('dataset_name','')).name
    path=Path(path) if path is not None else Path('temp')/filename
    if filename!=payload.get('filename') or not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=payload.get('digest'):
        raise ValueError('The measurement file has changed. Upload it again before submitting.')
    if _canonical(form)!=payload['fields']:
        raise ValueError('The columns or QC choices have changed. Apply columns again before submitting.')
    verified=form.copy();verified['dataset_name']=filename
    return verified


def pending_upload_path(request, filename):
    from pathlib import Path
    from uuid import UUID

    pending = request.session.get("refxas_pending_upload")
    if not isinstance(pending, dict) or pending.get("filename") != filename:
        raise ValueError("Upload the measurement again in this browser session.")
    key = pending.get("key", "")
    if not isinstance(key, str):
        raise ValueError("Invalid upload identifier.")
    try:
        valid_key = UUID(hex=key).hex == key
    except ValueError:
        valid_key = False
    if not valid_key or not filename or filename in (".", "..") or "/" in filename or chr(92) in filename:
        raise ValueError("Invalid measurement filename.")
    path = Path("temp") / key / filename
    if not path.is_file():
        raise ValueError("The temporary measurement is missing. Upload it again.")
    return path


def store_pending_upload(request, uploaded_file):
    from pathlib import Path
    from uuid import uuid4

    filename = uploaded_file.name
    if not uploaded_file.size:
        raise ValueError("The selected measurement file is empty.")
    if not filename or filename in (".", "..") or "/" in filename or chr(92) in filename or chr(0) in filename:
        raise ValueError("Invalid measurement filename.")
    key = uuid4().hex
    folder = Path("temp") / key
    folder.mkdir(parents=True, mode=0o700)
    path = folder / filename
    with path.open("xb") as output:
        for chunk in uploaded_file.chunks():
            output.write(chunk)
    request.session["refxas_pending_upload"] = {"filename": filename, "key": key}
    return path
