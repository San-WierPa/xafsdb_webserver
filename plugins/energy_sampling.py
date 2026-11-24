"""Describe scan spacing separately from instrumental energy resolution."""
import numpy as np


def describe_energy_sampling(energy, edge_energy):
    energy=np.asarray(energy,dtype=float)
    intervals=np.diff(energy)
    positive=intervals[np.isfinite(intervals) & (intervals > 0)]
    midpoints=(energy[1:]+energy[:-1])/2
    near=intervals[(np.abs(midpoints-edge_energy)<=10) & np.isfinite(intervals) & (intervals>0)]
    return dict(unit='eV',
        first_interval=float(intervals[0]) if len(intervals) else None,
        minimum_positive_interval=float(positive.min()) if len(positive) else None,
        median_positive_interval=float(np.median(positive)) if len(positive) else None,
        maximum_positive_interval=float(positive.max()) if len(positive) else None,
        near_edge_window_eV=10,
        near_edge_median_interval=float(np.median(near)) if len(near) else None,
        near_edge_interval_count=int(len(near)),
        instrumental_energy_resolution='not assessed from scan spacing')
