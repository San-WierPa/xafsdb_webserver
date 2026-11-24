"""Existing automated QC applied to automatic or corrected file columns."""
import logging
import hashlib
from pathlib import Path
import numpy as np
from plugins.qc_presentation import figure_image, result_context
from plugins.read_data import ReadData
from plugins.energy_sampling import describe_energy_sampling
from quality_control.quality_check import CheckQuality


def original_file_qc(path, source='SYNCHROTRON', column_selection=None, element=None, edge=None):
    """The same integrated QC for automatic or explicitly corrected inputs."""
    reader = ReadData(source=source,column_selection=column_selection)
    try:
        input_digest=hashlib.sha256(Path(path).read_bytes()).hexdigest()
        reader.process_data(path)
        qc = CheckQuality(Path(__file__).resolve().parents[1] / 'quality_control/Criteria.json',element=element or None,edge=edge or None)
        qc.load_data(reader.data.copy(), source=reader.source, name=Path(path).name)
        try:
            qc.preprocess_data(take_first=not bool(column_selection))
        except IndexError as exc:
            raise ValueError(
                'QC preprocessing could not finish with these inputs. '
                'Check the energy and detector columns or restore automatic selection.'
            ) from exc
        checks = {key: dict(passed=bool(value[0]), value=float(value[1])) for key,value in [
            ('edge_step',qc.check_edge_step()), ('energy_resolution',qc.check_energy_resolution()),
            ('k_max',qc.check_k()), ('noise',qc.estimate_noise())]}
        if any(not np.isfinite(item['value']) for item in checks.values()):
            raise ValueError('QC returned a non-finite result.')
        report = dict(file=Path(path).name, checks=checks,
                      status='PASS' if all(item['passed'] for item in checks.values()) else 'REVIEW',
                      energy_sampling=describe_energy_sampling(reader.data[0],qc.data.e0))
        import matplotlib.pyplot as plt
        plots = []
        for kind,label in [('RAW','Raw absorption'),('NORMALIZED','Normalized edge'),
                           ('k','EXAFS k²χ(k)'),('R','Fourier magnitude · not phase corrected')]:
            figure = qc.plot_data(data_type=kind)
            plots.append(dict(label=label, url=figure_image(figure)))
            plt.close(figure)
        result = result_context(report, qc.quality_criteria_sample, plots)
        result.update(available=True, energy_min=float(reader.data[0,0]),
                      energy_max=float(reader.data[0,-1]),
                      element=qc.data.element_n_edge[0], edge=qc.data.element_n_edge[1],
                      source=reader.source,selection=reader.meta_data_dict.get('Column_selection'),
                      input_digest=input_digest,
                      input_label='Corrected columns' if column_selection else 'Automatic columns')
        selection=result['selection'] or {}
        ref=selection.get('reference',{})
        result['reference_note']=('A separate reference signal was selected.' if ref.get('enabled') else
            ref.get('note','Sample and reference follow the automatic file mapping.'))
        return result
    except Exception as exc:
        logging.getLogger(__name__).exception('Original-file QC could not be completed for %s',path)
        return dict(available=False, error='QC could not be completed: '+str(exc)+'. Review the energy, sample and reference columns, then apply them.')
    finally:
        import matplotlib.pyplot as plt
        plt.close('all')
