# Solar ↔ HRV Correlation — toy study

This sim creates synthetic solar activity and HRV/coherence time series,
then computes a cross-correlation to illustrate possible lagged coupling.

---

## What it shows
- Time series of synthetic solar index and HRV-like coherence.
- Cross-correlation revealing lag windows where influence is strongest.

## Run it
```bash
pip install -r sims/requirements.txt   # add scipy if needed
python sims/solar_hrv_correlation.py
Output
	•	sims/figures/solar_hrv_timeseries.png
	•	sims/figures/solar_hrv_xcorr.png

Notes
	•	Replace synthetic solar with real indices (sunspot number, F10.7, Kp) for analysis.
	•	Replace synthetic HRV with group HRV if you have recorded data.
