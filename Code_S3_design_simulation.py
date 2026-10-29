"""Code S3: assumed operating characteristics, not an empirical pilot.

The latent beta variable creates exchangeable correlated binary item scores.
All persons in a scenario have the same pre-fixed K. Participants have equal
weight. Missingness is independent of scores (MCAR) at the participant level.
The complete-case Welch interval is an illustrative diagnostic under this model,
not a proposed solution to MNAR dropout or the real trial's final analysis plan.
The sample missingness bounds concern the realized full-data arm difference;
they are not confidence intervals for a population causal parameter.
"""
from pathlib import Path
import argparse,csv,itertools,json,platform
import numpy as np
from scipy.stats import t as student_t

def simulate(cfg):
 rng=np.random.default_rng(cfg['seed']);out=[]
 repetitions=cfg['replications']
 for n,k,p0,delta,rho,missing in itertools.product(cfg['persons_per_arm'],cfg['items_per_person'],cfg['control_mean'],cfg['observed_mean_difference'],cfg['item_ICC'],cfg['MCAR_dropout']):
  means=[p0,p0+delta];scores=[];observed=[]
  for p in means:
   if rho:
    concentration=1/rho-1
    q=rng.beta(p*concentration,(1-p)*concentration,size=(repetitions,n))
   else:q=np.full((repetitions,n),p)
   y=rng.binomial(k,q)/k
   scores.append(y)
   observed.append(rng.random((repetitions,n))>=missing)
  nobs=[x.sum(axis=1) for x in observed]
  assert all(np.all(x>=2) for x in nobs)
  observed_sum=[np.where(m,y,0).sum(axis=1) for y,m in zip(scores,observed)]
  observed_mean=[s/count for s,count in zip(observed_sum,nobs)]
  observed_variance=[np.where(m,(y-avg[:,None])**2,0).sum(axis=1)/(count-1) for y,m,avg,count in zip(scores,observed,observed_mean,nobs)]
  estimate=observed_mean[1]-observed_mean[0]
  v=[s/count for s,count in zip(observed_variance,nobs)]
  se=np.sqrt(v[0]+v[1]);assert np.all(se>0)
  df=(v[0]+v[1])**2/(v[0]**2/(nobs[0]-1)+v[1]**2/(nobs[1]-1))
  critical=student_t.ppf(.975,df)
  lower=estimate-critical*se;upper=estimate+critical*se
  covered=(lower<=delta)&(delta<=upper)
  rejection=(lower>0)|(upper<0)
  benefit=lower>0
  # Scores are bounded in [0,1]. These endpoints include every value
  # for each missing person's *scheduled* Y; no missing outcome is scored zero.
  misses=[n-x for x in nobs]
  missing_lower=observed_sum[1]/n-(observed_sum[0]+misses[0])/n
  missing_upper=(observed_sum[1]+misses[1])/n-observed_sum[0]/n
  realized=scores[1].mean(axis=1)-scores[0].mean(axis=1)
  assert np.all(realized>=missing_lower-1e-12) and np.all(realized<=missing_upper+1e-12)
  analytic_full_variance=sum(p*(1-p)/k*(1+(k-1)*rho)/n for p in means)
  if missing==0:
   assert abs(estimate.mean()-delta)<=6*np.sqrt(analytic_full_variance/repetitions)
   assert .80<=estimate.var(ddof=1)/analytic_full_variance<=1.20
  rate=float(rejection.mean())
  out.append(dict(persons_per_arm=n,items_per_person=k,control_mean=p0,true_observed_difference=delta,item_ICC=rho,MCAR_dropout=missing,
   replications=repetitions,mean_estimate=float(estimate.mean()),bias=float(estimate.mean()-delta),empirical_SD=float(estimate.std(ddof=1)),
   mean_model_SE=float(se.mean()),mean_95_interval_width=float((upper-lower).mean()),coverage_95=float(covered.mean()),
   two_sided_zero_rejection_rate=rate,positive_lower_bound_rate=float(benefit.mean()),rejection_rate_MCSE=float(np.sqrt(rate*(1-rate)/repetitions)),
   coverage_MCSE=float(np.sqrt(covered.mean()*(1-covered.mean())/repetitions)),mean_missingness_bound_width=float((missing_upper-missing_lower).mean()),
   realized_full_data_difference_within_missing_bounds=True,analytic_full_data_variance=analytic_full_variance,
   complete_case_analysis_is_illustrative_not_final_SAP=True))
 return out

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--config',type=Path,default=Path(__file__).with_name('Code_S3_assumptions.json'))
 parser.add_argument('--output-dir',type=Path,default=Path(__file__).resolve().parent);args=parser.parse_args()
 cfg=json.loads(args.config.read_text(encoding='utf8'));rows=simulate(cfg)
 args.output_dir.mkdir(parents=True,exist_ok=True)
 payload={'scope':cfg['scope'],'assumptions':cfg,'scenario_count':len(rows),'environment':{'python':platform.python_version(),'numpy':np.__version__},'results':rows,
 'limits':['No empirical pilot estimates or recommended sample size','No awareness-state or linguistic-mechanism validation','Fixed K and exchangeable positive ICC are illustrative','MCAR dropout is not a claim about actual missingness','95% two-sided zero testing is not the trial\'s meaningful-effect or multiplicity decision','Worst/best-case endpoints bound the realized sample contrast, not population sampling uncertainty']}
 (args.output_dir/'Code_S3_output.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 with (args.output_dir/'Code_S3_output.csv').open('w',encoding='utf8',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
 print(json.dumps({'scenarios':len(rows),'replications_per_scenario':cfg['replications'],'seed':cfg['seed'],'empirical_data_used':False,'missing_score_bounds_all_verified':True}))
if __name__=='__main__':main()
