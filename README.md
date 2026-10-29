# Computational materials for Linguistic reflexivity and reflective self-awareness

Version 8.3.2. These files reproduce synthetic calculations and hypothetical design simulations. They contain no participant observations and do not validate an awareness assay or recommend a trial sample size.

## Files

- `Code_S1_observational_equivalence.py`: two synthetic population constructions, checked using exact rational arithmetic.
- `independent_region_check.py` (Code S2): 29 identification scenarios, exact feasible witnesses and numerical linear-programming checks. Exact feasibility and numerical optimality are different checks; this is not a general symbolic proof.
- `Code_S3_design_simulation.py`: 144 scenarios, 4000 repetitions per scenario, seed 20261026. Assumptions are declared in `Code_S3_assumptions.json`; all parameters are hypothetical. MCAR dropout, fixed item counts and illustrated score correlations are assumptions, not empirical findings. Complete-case intervals are diagnostic illustrations rather than a final trial analysis plan. Missing-score endpoints bound the realized full-data sample contrast rather than a population causal effect.
- `draw_figure.py`: deterministic explanatory schematic; no generative-image output or participant data.
- Supplied JSON/CSV files are the expected computational outputs.

## Reproduce

Use Python 3.12. Install the pinned packages with `python -m pip install -r requirements.txt`. Run `python run_all.py`. This creates a separate `reproduced/` directory and compares scientific results with the supplied outputs. The full simulation can take several minutes. Figure files are generated in `reproduced/figure/`.

S1 uses only the standard library. S2 requires SciPy; S3 requires NumPy; figure rendering requires Matplotlib. Historical “Supplement E” labels in S1 refer to the identification analysis now in Supplement B, not the current task-evidence supplement.

The latent awareness states in the synthetic interpretation refer to access immediately before a report prompt under the specified measurement history. A prompt may affect subsequent access; no-false-positive assumptions concern that stated pre-prompt target.

## Assistance and reuse

ChatGPT (OpenAI) assisted computational development. Codex (OpenAI, gpt-6.1-sol) prepared the submission package and revised the drawing code. The authors remain responsible for the work. Earlier exact model identifiers were not consistently recorded.

The authors approved the MIT license for the project code and accompanying software documentation on 29 October 2026. This does not license cited publications or third-party material. No exclusive copyright entitlement to AI output is asserted. See LICENSE. Authorship and version metadata are provided in CITATION.cff. No repository DOI has been assigned.

Repository: https://github.com/The-Badr/Linguistic-reflexivity-and-reflective-self-awareness-A-bounded-process-proposal

For journal review, an equivalent supplementary archive omits the identifying repository link and citation metadata.

