# The Empathetic Fitting Room: Supporting Material

**Author:** Agnese Enrica Picchio
**Supervisor:** Dr Fabrizio Smeraldi

## Included files
**Main system**
* `empathetic_fitting_room_controller.ipynb`: main adaptive-condition controller (PID loop, sensor/light/audio pipeline);
* `static_condition.py`: used to evaluate the static control condition (fixed lighting, constant audio);
* `live_monitor.py`: live monitoring interface (Tkinter), runs independently.

**Analysis notebooks**
* `analyse_results_final.ipynb`: main results analysis (RR-interval and SAM changes, Bayesian t-tests, latency);
* `rq2_proportionality.ipynb`: PID/RR-interval correlation analysis (RQ2);
* `PID_score_plot.ipynb`: PID reaction score plot (Fig. 5);
* `plot_comparison_graphs.ipynb`: control strategy comparison (Fig. 4).

**Audio files**
* `stem_1_drone.wav`, `chords_24s.wav`, `rhythm_24s.wav`, `stem_4_melody.wav`: the four-stem audio layers.

**Test data**
* `testing_session.csv`: the researcher's own self-testing session data, used by `plot_comparison_graphs.ipynb` to produce the control-strategy comparison (Fig. 4). Not participant data, so not subject to consent-based access restrictions.


## Files NOT included
The session CSVs (per-participant adaptive/static logs), interview transcripts, completed SAM questionnaire sheets, and `participant_info.csv` are **not included**, consistent with the data access terms agreed with participants.

All analysis notebooks retain their originally executed output cells, so results remain visible and verifiable by inspection without requiring the raw data.


## How to run

All code, notebook and data files should be kept in a single flat folder (no subfolders): every notebook/script reads its input files using relative paths, so it expects them to sit alongside it. Specifically: 
* the four audio stem `.wav` files must be in the same folder as `empathetic_fitting_room_controller.ipynb` and `static_condition.py`, which load them directly.
* `testing_session.csv` must be in the same folder as `plot_comparison_graphs.ipynb`, which reads it to produce Fig. 4.

Moreover, `empathetic_fitting_room_controller.ipynb` must be run inside a live Jupyter server, as it cannot be run as a plain `.py` script or via a non-interactive execution tool as the main function is launched with `await main()`.

Install dependencies:
```
pip install -r requirements.txt
```

The core system notebooks (`empathetic_fitting_room_controller.ipynb`, `static_condition.py`) require a paired Polar H10 sensor and Philips Hue BLE light strip; Bluetooth addresses must be set in each file.

The analysis notebooks require the session CSVs and `participant_info.csv`, which are excluded per the note above.


## Generative AI use

See the dissertation's Appendix F (Generative AI: Student Accountability Statement) for full disclosure. AI-assisted files are individually marked with a header comment.


