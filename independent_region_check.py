"""Independent audit of the uploaded S1b, using 24 compatible types rather than its 64-type construction.

The exact zero cells in Box 1 force three possible report histories (baseline,
control follow-up, treated follow-up): 111, 001, and 000, with masses 2/5, 1/5,
and 2/5. Each history may contain any of eight latent-awareness histories.
This is an audit of synthetic identification claims, not empirical analysis.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import platform
import scipy
from scipy.optimize import linprog

REPORT_MASSES = {(1, 1, 1): F(2, 5), (0, 0, 1): F(1, 5), (0, 0, 0): F(2, 5)}
STATES = [(a, r) for r in REPORT_MASSES for a in product((0, 1), repeat=3)]
SOLVED_SCENARIOS = 0

def solve(nofp=False, invariant=False, baseline_s=None, constant_s=None,
          no_exit_t=False, no_exit_c=False, objective='onset_t'):
    global SOLVED_SCENARIOS
    rows = [[F(int(r == history)) for a, r in STATES] for history in REPORT_MASSES]
    rhs = list(REPORT_MASSES.values())
    if baseline_s is not None:
        if not F(2, 5) <= baseline_s <= 1:
            raise ValueError('invalid baseline sensitivity')
        rows.append([F(a[0]) for a, r in STATES]); rhs.append(F(2, 5) / baseline_s)
    if constant_s is not None:
        if not F(3, 5) <= constant_s <= 1:
            raise ValueError('invalid constant sensitivity')
        for k, q in enumerate((F(2, 5), F(2, 5), F(3, 5))):
            rows.append([F(a[k]) for a, r in STATES]); rhs.append(q / constant_s)
    def allowed(a, r):
        if nofp and any(r[k] > a[k] for k in range(3)): return False
        if invariant and not any(all(r[k] == d * a[k] for k in range(3)) for d in (0, 1)): return False
        if no_exit_t and a[0] > a[2]: return False
        if no_exit_c and a[0] > a[1]: return False
        return True
    bds = [(0, None) if allowed(a, r) else (0, 0) for a, r in STATES]
    def score(a):
        et = int(a[0] == 0 and a[2] == 1)
        ec = int(a[0] == 0 and a[1] == 1)
        if objective == 'onset_t': return et
        if objective == 'onset_difference': return et - ec
        if objective == 'prevalence_difference': return a[2] - a[1]
        raise ValueError(objective)
    scores = [F(score(a)) for a, r in STATES]
    answers = []
    for sign in (1, -1):
        fit = linprog([sign * float(c) for c in scores],
                      A_eq=[[float(v) for v in row] for row in rows],
                      b_eq=[float(v) for v in rhs], bounds=bds, method='highs')
        if not fit.success: raise RuntimeError(fit.message)
        weights = [F(float(x)).limit_denominator(10**7) if abs(x) > 1e-9 else F(0) for x in fit.x]
        if any(w < 0 for w in weights): raise AssertionError('negative witness mass')
        for (a, r), w in zip(STATES, weights):
            if w and not allowed(a, r): raise AssertionError('invalid witness state')
        for row, target in zip(rows, rhs):
            if sum(v*w for v, w in zip(row, weights)) != target:
                raise AssertionError('exact witness constraint failed')
        val = sum(c*w for c, w in zip(scores, weights))
        if abs(float(val) - sign * fit.fun) > 1e-8: raise AssertionError('objective mismatch')
        answers.append({'value': str(val), 'exact_feasible_witness': [
            {'mass': str(w), 'awareness': a, 'reports': r}
            for (a, r), w in zip(STATES, weights) if w]})
    SOLVED_SCENARIOS += 1
    return {'lower': answers[0]['value'], 'upper': answers[1]['value'], 'witnesses': answers}

def pair(x): return F(x['lower']), F(x['upper'])

def interpretation_examples():
    def describe(rows):
        if sum(w for w,a,r in rows) != 1: raise AssertionError('model normalization')
        joints={}
        for label,col in [('control',1),('intervention',2)]:
            joints[label]={str(i)+str(j):sum(w for w,a,r in rows if (r[0],r[col])==(i,j))
                           for i,j in product((0,1),repeat=2)}
        prevalence=[sum(w*a[k] for w,a,r in rows) for k in range(3)]
        sensitivity=[sum(w*r[k] for w,a,r in rows)/prevalence[k] for k in range(3)]
        return {'report_joint':joints,'awareness_prevalence':prevalence,'sensitivity':sensitivity,
                'onset_t':sum(w for w,a,r in rows if a[0]==0 and a[2]==1),
                'onset_c':sum(w for w,a,r in rows if a[0]==0 and a[1]==1)}
    imperfect=[]
    for a in product((0,1),repeat=3):
        latent_mass=F(1,2)*F(1,2)*(F(3,4) if a[2] else F(1,4))
        for d in (0,1):
            w=latent_mass*(F(4,5) if d else F(1,5))
            imperfect.append((w,a,tuple(d*v for v in a)))
    perfect=[(w,r,r) for w,a,r in imperfect]
    m1,m2=describe(perfect),describe(imperfect)
    if m1['report_joint'] != m2['report_joint']: raise AssertionError('nonzero pair mismatch')
    if not all(x>0 for j in m1['report_joint'].values() for x in j.values()):
        raise AssertionError('nonzero pair has zero report cells')
    if m1['sensitivity'] != [F(1)]*3 or m2['sensitivity'] != [F(4,5)]*3:
        raise AssertionError('nonzero pair invariance')
    net_zero=describe([(F(2,5),(1,1,1),(1,1,1)),
                      (F(1,5),(0,0,1),(0,0,1)),
                      (F(1,5),(0,1,0),(0,0,0)),
                      (F(1,5),(0,0,0),(0,0,0))])
    if net_zero['onset_t'] != net_zero['onset_c'] or net_zero['report_joint']['intervention']['01'] != F(1,5):
        raise AssertionError('onset estimand distinction')
    return {'nonzero_report_cells_nonidentification':{'perfect':m1,'imperfect':m2},
            'Box1_person_invariant_net_zero_awareness_effect':net_zero}

def main():
    out = {'unrestricted': solve(), 'no_false_positives': solve(nofp=True),
           'person_invariant': solve(nofp=True, invariant=True)}
    if pair(out['unrestricted']) != (F(0), F(1)): raise AssertionError('unrestricted')
    if pair(out['no_false_positives']) != (F(0), F(3,5)): raise AssertionError('no false positives')
    if pair(out['person_invariant']) != (F(1,5), F(3,5)): raise AssertionError('invariance')
    grid = []
    for k in range(8, 21):
        sb = F(k, 20)
        result = solve(nofp=True, baseline_s=sb)
        expected = max(F(0), F(3,5) - F(2,5)/sb), 1-F(2,5)/sb
        if pair(result) != expected: raise AssertionError(('baseline sensitivity',sb))
        grid.append({'s_b':str(sb),'region':list(map(str,expected))})
        if sb in (F(1), F(4,5), F(2,3)):
            out['known_baseline_'+str(sb)] = result
    # The tipping point 2/3 is not on the 1/20 grid.
    out['known_baseline_2/3'] = solve(nofp=True, baseline_s=F(2,3))
    if pair(out['known_baseline_2/3']) != (F(0), F(2,5)): raise AssertionError('tipping point')
    constant_grid = []
    for k in range(12, 21):
        s = F(k, 20)
        result = solve(nofp=True, constant_s=s, no_exit_t=True)
        target = F(1,5)/s
        if pair(result) != (target,target): raise AssertionError(('constant sensitivity no exit',s))
        constant_grid.append({'s':str(s),'point':str(target)})
    out['constant_s_4/5_allow_exit'] = solve(nofp=True, constant_s=F(4,5))
    if pair(out['constant_s_4/5_allow_exit']) != (F(1,4),F(7,20)): raise AssertionError('allow exits')
    out['person_invariant_onset_difference'] = solve(nofp=True,invariant=True,objective='onset_difference')
    out['person_invariant_prevalence_difference'] = solve(nofp=True,invariant=True,objective='prevalence_difference')
    # Deliberately malformed parameter: verifies meaningful rejection of invalid inputs.
    try:
        solve(nofp=True,baseline_s=F(6,5))
    except ValueError:
        invalid_rejected=True
    else:
        raise AssertionError('invalid sensitivity accepted')
    result = {'status':'PASS','scope':'independent synthetic audit; feasible endpoint witnesses exact, LP optimality numeric',
              'python':platform.python_version(),'scipy':scipy.__version__,
              'compatible_type_count':len(STATES),'regions':out,
              'successful_lp_scenarios':SOLVED_SCENARIOS,
              'baseline_grid':grid,'constant_sensitivity_grid':constant_grid,
              'invalid_parameter_rejected':invalid_rejected,
              'interpretation_examples':interpretation_examples()}
    target=Path(__file__).with_name('independent_region_check.json')
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2,default=str)+'\n',encoding='utf-8')
    print(json.dumps({'status':'PASS','cases':SOLVED_SCENARIOS,
                      'core_regions':{n:{k:v for k,v in d.items() if k != 'witnesses'} for n,d in out.items()},
                      'saved':str(target)},indent=2))

if __name__=='__main__': main()
