"""Run the QC over every SYNCHROTRON example file and dump the results as JSON.

Usage (inside the app image, /app on sys.path):
    python quality_control/regression/run_examples.py results.json

Compare two runs (e.g. before/after a QC change) with `diff` or jq. Reports
per file: detected beamline, e0, edge step, k-range, noise, the three quality
verdicts, and whether raw_energy/raw_mu were exported for the preview plot.
"""
import sys, json, warnings, os, glob
warnings.filterwarnings("ignore")
import matplotlib; matplotlib.use("Agg")
sys.path.insert(0,"/app")
from plugins.read_data import read_data
from quality_control.quality_check import check_quality
base="/app/quality_control/example data/SYNCHROTRON"
files=sorted(f for f in glob.glob(base+"/*") if os.path.isfile(f) and not f.endswith(('.zip','.gitkeep')))
out={}
for f in files:
    name=os.path.basename(f)
    try:
        rd=read_data(update_erange="")
        rd.process_data(f)
        cq=check_quality(quality_criteria_json="/app/quality_control/Criteria.json")
        cq.load_data(rd.data, source="SYNCHROTRON", name=name)
        cq.preprocess_data(take_first=True)
        for dt in ("RAW","NORMALIZED","k","R"):
            fig=cq.plot_data(data_type=dt); assert len(cq.encode_base64_figure(fig))>500, dt
        r={"beamline":str(getattr(rd,"beamline",None)),
           "e0":round(float(cq.data.e0),3),
           "edge_step":round(float(cq.data.edge_step),5),
           "kmin":round(float(cq.kmin),3),"kmax":round(float(cq.kmax),3),
           "edge_ok":bool(cq.check_edge_step()[0]),
           "eres_ok":bool(cq.check_energy_resolution()[0]),
           "k_ok":bool(cq.check_k()[0]),
           "noise":round(float(cq.estimate_noise()[1]),5),
           "raw_in_meta": bool({"raw_energy","raw_mu"} <= set(getattr(rd,"meta_data_dict",{}))),
           "n_pts": int(len(cq.data.energy))}
    except Exception as e:
        r={"ERROR":f"{type(e).__name__}: {str(e)[:110]}"}
    out[name]=r
dest = sys.argv[1] if len(sys.argv) > 1 else "/out/result.json"
open(dest, "w").write(json.dumps(out, indent=0, sort_keys=True))
