"""Code S1: exact synthetic reconstruction of Supplement E.

Python 3 standard library only. No participant data or random simulation.
Run: python Code_S1_observational_equivalence.py --output Code_S1_output.json
Checks remain active under Python -O. Fractions are serialized as strings.
This demonstrates one pair of observationally equivalent models, not a
universal impossibility of identifying awareness using additional assumptions.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json

WEIGHTS = (F(2, 5), F(1, 5), F(2, 5))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def emergence_model(kind, treatment):
    aware_before = kind == 0
    aware_after = aware_before or (kind == 1 and treatment == 1)
    return aware_before, aware_after, aware_before, aware_after


def reporting_model(kind, treatment):
    aware_before = kind in (0, 1)
    aware_after = aware_before
    report_before = kind == 0
    report_after = kind == 0 or (kind == 1 and treatment == 1)
    return aware_before, aware_after, report_before, report_after


def distribution(model, treatment):
    require(treatment in (0, 1), 'Assignment must be binary')
    require(all(w >= 0 for w in WEIGHTS) and sum(WEIGHTS) == 1,
            'Population masses must be nonnegative and sum to one')
    joint = {f'{a}{b}': F(0) for a in (0, 1) for b in (0, 1)}
    before = after = onset = F(0)
    for kind, weight in enumerate(WEIGHTS):
        a0, a1, r0, r1 = model(kind, treatment)
        require(all(v in (0, 1) for v in (a0, a1, r0, r1)), 'States must be binary')
        before += weight * int(a0)
        after += weight * int(a1)
        onset += weight * int(a1 and not a0)
        joint[f'{int(r0)}{int(r1)}'] += weight
    require(sum(joint.values()) == 1, 'Joint report law must normalize')
    return {'report_joint': joint, 'awareness_before': before,
            'awareness_after': after, 'new_awareness': onset}


def verify():
    expected = {
        0: {'00': F(3, 5), '01': F(0), '10': F(0), '11': F(2, 5)},
        1: {'00': F(2, 5), '01': F(1, 5), '10': F(0), '11': F(2, 5)},
    }
    results = {}
    for treatment in (0, 1):
        e = distribution(emergence_model, treatment)
        r = distribution(reporting_model, treatment)
        require(e['report_joint'] == r['report_joint'] == expected[treatment],
                'Joint report distributions differ from each other or the manuscript')
        require(e['new_awareness'] == (F(1, 5) if treatment else F(0)),
                'Emergence-model onset mismatch')
        require(r['new_awareness'] == 0, 'Reporting model must have no onset')
        require(e['awareness_before'] == F(2, 5), 'Emergence baseline mismatch')
        require(e['awareness_after'] == (F(3, 5) if treatment else F(2, 5)),
                'Emergence follow-up mismatch')
        require(r['awareness_before'] == r['awareness_after'] == F(3, 5),
                'Reporting-model latent awareness must be fixed')
        results['intervention' if treatment else 'control'] = {
            'emergence_model': e, 'reporting_model': r}
    return {'status': 'PASS', 'synthetic': True,
            'scope': 'Exact reconstruction of the two models in Supplement E only',
            'pair_order': 'baseline report, follow-up report', 'results': results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='Optional JSON output path')
    args = parser.parse_args()
    text = json.dumps(verify(), default=str, indent=2) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding='utf-8')
    print(text, end='')


if __name__ == '__main__':
    main()
