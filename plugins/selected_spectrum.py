"""Shared validation for web previews and selected spectra passed to QC."""
import numpy as np


def calculate_spectrum(raw_data, labels, selection, declared_energy_unit=None):
    raw = np.asarray(raw_data, dtype=float)
    if raw.ndim != 2:
        raise ValueError('Column selection requires a two-dimensional data table')
    if raw.shape[0] != len(labels) and raw.shape[1] == len(labels):
        raw = raw.T
    if len(labels) != raw.shape[0]:
        raise ValueError('Column labels do not match the uploaded data table')

    def column(key, chosen=None):
        value = (selection if chosen is None else chosen).get(key)
        if value is None or value == '':
            raise ValueError('Please select ' + key.replace('_', ' '))
        try:
            index = int(value)
        except (TypeError, ValueError):
            matches = [i for i, label in enumerate(labels)
                       if str(label).strip().lower() == str(value).strip().lower()]
            if len(matches) != 1:
                raise ValueError('Column name is missing or ambiguous; select its numbered column')
            index = matches[0]
        if index < 0 or index >= raw.shape[0]:
            raise ValueError('Selected column is outside the data table')
        return raw[index].copy(), str(labels[index])

    def signal(chosen):
        a,a_label=column('signal_a',chosen)
        formula=chosen.get('formula','raw')
        if formula not in ('raw','ratio','log_ratio','negative_log_ratio'):
            raise ValueError('Unsupported spectrum calculation')
        b_label=None
        with np.errstate(divide='ignore',invalid='ignore',over='ignore'):
            if formula=='raw':mu=a
            else:
                b,b_label=column('signal_b',chosen)
                ratio=a/b
                mu=ratio if formula=='ratio' else np.where(ratio>0,np.log(ratio),np.nan)
                if formula=='negative_log_ratio':mu=-mu
        return mu,a_label,b_label,formula

    energy, energy_label = column('energy')
    mu,a_label,b_label,formula=signal(selection)
    reference_enabled=selection.get('reference_enabled') in (True,'true','yes','1',1)
    if reference_enabled:
        reference,ref_a,ref_b,ref_formula=signal(dict(signal_a=selection.get('reference_a'),
            signal_b=selection.get('reference_b'),formula=selection.get('reference_formula','raw')))
        reference_meta=dict(enabled=True,signal_a=ref_a,signal_b=ref_b,formula=ref_formula)
    else:
        reference=mu.copy()
        reference_meta=dict(enabled=False,note='No separate reference supplied; the sample signal fills both QC inputs.')
    # Keep sample and reference from the same original rows before sorting or
    # removing duplicate energies. Neither channel can shift against the other.
    valid = np.isfinite(energy) & np.isfinite(mu) & np.isfinite(reference)
    dropped = int(len(energy) - valid.sum())
    energy, mu, reference = energy[valid], mu[valid], reference[valid]
    if len(energy) < 10:
        raise ValueError('Selected columns produce fewer than 10 finite data points; check zeros and logarithm inputs')
    # Preserve the existing eV/keV convention, using the median of finite values.
    requested_unit=selection.get('energy_unit','auto') or 'auto'
    if requested_unit not in ('auto','eV','keV'):
        raise ValueError('Energy units must be auto, eV or keV')
    effective_unit=declared_energy_unit if requested_unit=='auto' else requested_unit
    converted = effective_unit=='keV' or (effective_unit not in ('eV','keV') and bool(0 < np.median(energy) < 100))
    if converted:
        energy *= 1000
    order = np.argsort(energy, kind='stable')
    energy, mu, reference = energy[order], mu[order], reference[order]
    # Larch splines require strictly increasing energy. Keep the first reading
    # at an exactly duplicated energy; record how many were omitted.
    unique = np.r_[True, np.diff(energy) > 0]
    duplicates = int(len(energy) - unique.sum())
    energy, mu, reference = energy[unique], mu[unique], reference[unique]
    if len(energy) < 10 or energy[-1] <= energy[0]:
        raise ValueError('Select an energy column with at least 10 distinct energies')
    metadata = dict(energy=energy_label, signal_a=a_label, signal_b=b_label,
                    formula=formula, dropped_nonfinite=dropped,
                    dropped_duplicate_energy=duplicates, converted_keV_to_eV=converted,
                    input_energy_unit=effective_unit or ('keV' if converted else 'eV'),
                    energy_unit_source='selection' if requested_unit!='auto' else 'file header' if declared_energy_unit else 'value convention',
                    reference=reference_meta)
    return np.array([energy, reference, mu]), metadata
