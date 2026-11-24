"""Presentation of Frank's integrated checks; no changes to QC calculations."""
import base64
import io


def result_context(report, criteria, plots, downloads=()):
    definitions = [
        ('edge_step', 'Edge step', 'edge step', 'a.u.'),
        ('energy_resolution', 'First energy interval (legacy criterion)', 'energy resolution', 'eV'),
        ('k_max', 'Maximum k', 'k max', 'Å⁻¹'),
        ('noise', 'Estimated noise', 'noise', 'a.u.'),
    ]
    rows = []
    for key, label, criterion, unit in definitions:
        check = report['checks'][key]
        bounds = criteria[criterion]
        rows.append(dict(label=label, value=format(check['value'], '.6g'),
                         lower=bounds['min'], upper=bounds['max'], unit=unit,
                         status='PASS' if check['passed'] else 'REVIEW'))
    return dict(report=report, checks=rows, plots=plots, downloads=downloads)


def figure_image(figure):
    buffer = io.BytesIO()
    figure.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    return 'data:image/png;base64,' + base64.b64encode(buffer.getvalue()).decode('ascii')
