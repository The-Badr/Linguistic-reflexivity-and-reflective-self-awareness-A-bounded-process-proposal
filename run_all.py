"""Reproduce scientific values without altering the supplied expected results."""
from pathlib import Path
import importlib, json, math, platform, shutil, subprocess, sys
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'reproduced'; OUT.mkdir(exist_ok=True)
def call(name,*args,cwd=None):
 subprocess.run([sys.executable,str(ROOT/name),*map(str,args)],check=True,cwd=cwd or ROOT)
call('Code_S1_observational_equivalence.py','--output',OUT/'Code_S1_output.json')
s2dir=OUT/'s2';s2dir.mkdir(exist_ok=True)
shutil.copy2(ROOT/'independent_region_check.py',s2dir/'independent_region_check.py')
subprocess.run([sys.executable,str(s2dir/'independent_region_check.py')],check=True)
call('Code_S3_design_simulation.py','--config',ROOT/'Code_S3_assumptions.json','--output-dir',OUT)
figdir=OUT/'figure';figdir.mkdir(exist_ok=True)
shutil.copy2(ROOT/'draw_figure.py',figdir/'draw_figure.py')
subprocess.run([sys.executable,str(figdir/'draw_figure.py')],check=True)
def compare(a,b,path=''):
 if isinstance(a,dict):
  assert isinstance(b,dict) and set(a)==set(b),path
  for k in a:
   if k not in ['environment','python','scipy','numpy','versions']:compare(a[k],b[k],path+'/'+k)
 elif isinstance(a,list):
  assert len(a)==len(b),path
  for i,(x,y) in enumerate(zip(a,b)):compare(x,y,path+'/'+str(i))
 elif isinstance(a,float):assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-12),path
 else:assert a==b,(path,a,b)
pairs=[(ROOT/'Code_S1_output.json',OUT/'Code_S1_output.json'),(ROOT/'independent_region_check.json',s2dir/'independent_region_check.json'),(ROOT/'Code_S3_output.json',OUT/'Code_S3_output.json')]
for a,b in pairs:compare(json.loads(a.read_text(encoding='utf8')),json.loads(b.read_text(encoding='utf8')))
report={'status':'PASS','scientific_outputs_compared':3,'Python':platform.python_version(),'packages':{n:importlib.import_module(n).__version__ for n in ['numpy','scipy','matplotlib']},'empirical_validation_claimed':False,'environment_metadata_excluded_from_scientific_comparison':True}
(OUT/'Reproduction_Check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
print(json.dumps(report))

