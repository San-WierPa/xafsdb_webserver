# QC regression check

`run_examples.py` runs the full read-out + quality-control path over every file in
`quality_control/example data/SYNCHROTRON/` and writes one JSON record per file:
detected beamline, `e0`, edge step, k-range, estimated noise, the three quality
verdicts, and whether `raw_energy`/`raw_mu` reached `meta_data_dict`.

It is meant for before/after comparison. Run it once against the image you have
deployed, once against the candidate, and diff the two JSON files — a changed
beamline or a verdict flip is what you are looking for.

```bash
# baseline
docker run --rm -v "$PWD/out:/out" \
  registry.hzdr.de/daphne4nfdi/xafsdb/refxas_beta2_test:<deployed-tag> \
  python /app/quality_control/regression/run_examples.py /out/baseline.json

# candidate: same, with the changed QC files mounted over /app
docker run --rm -v "$PWD/out:/out" \
  -v "$PWD/plugins/read_data.py:/app/plugins/read_data.py:ro" \
  -v "$PWD/quality_control/quality_check.py:/app/quality_control/quality_check.py:ro" \
  registry.hzdr.de/daphne4nfdi/xafsdb/refxas_beta2_test:<deployed-tag> \
  python /app/quality_control/regression/run_examples.py /out/candidate.json

diff <(jq -S . out/baseline.json) <(jq -S . out/candidate.json)
```

A `"beamline": "None"` entry means detection failed and the generic `np.loadtxt`
fallback was used. The numbers that follow it are then unreliable even though
they look plausible — that is exactly how the double-space marker bug stayed
invisible.
