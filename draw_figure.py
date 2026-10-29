"""Deterministic explanatory figure for submission 8.3.2.
ChatGPT-assisted conceptual development; drawing code revised with Codex (OpenAI, gpt-6.1-sol), 29 October 2026.
No primary observed data or generative-image model output is represented.
"""
from pathlib import Path
import platform
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch,FancyArrowPatch
from matplotlib.path import Path as MPath
OUT=Path(__file__).resolve().parent
def draw():
 plt.rcParams.update({'font.family':'DejaVu Sans','pdf.fonttype':42,'svg.fonttype':'none'})
 fig,axes=plt.subplots(2,1,figsize=(7.5,6.4),gridspec_kw={'height_ratios':[1.15,1]})
 for ax in axes:ax.set_xlim(0,10);ax.set_ylim(0,5.5);ax.axis('off')
 def node(ax,x,y,w,h,t,fs=9,dash=False):
  ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.06,rounding_size=0.06',facecolor='white',edgecolor='#333333',linewidth=.85,linestyle='--' if dash else '-'))
  ax.text(x+w/2,y+h/2,t,ha='center',va='center',fontsize=fs,linespacing=1.22)
 def arrow(ax,start,end,dash=False):ax.annotate('',end,start,arrowprops={'arrowstyle':'->','lw':.85,'color':'#333333','linestyle':'--' if dash else '-'})
 ax=axes[0];ax.text(.05,5.23,'A  Candidate process',fontsize=11,fontweight='bold')
 node(ax,.08,2.8,2.12,1.1,'Available semantic\nrelations',9.5)
 node(ax,2.85,2.25,3.52,1.9,'Linguistic formulation of own use\n\nSelection / relational formulation\nself and time anchoring\nmaintenance or re-entry',9)
 node(ax,7.08,2.8,2.72,1.1,'Candidate conscious\nreflective content',9.3,True)
 node(ax,7.08,.32,2.72,1.0,'Observed report or\nattribution response',9.4)
 arrow(ax,(2.2,3.35),(2.78,3.35));arrow(ax,(6.42,3.35),(7.0,3.35),True);arrow(ax,(8.44,2.71),(8.44,1.4),True)
 loop=MPath([(6.0,4.21),(6.45,4.98),(3.0,4.98),(3.35,4.21)],[MPath.MOVETO,MPath.CURVE4,MPath.CURVE4,MPath.CURVE4])
 ax.add_patch(FancyArrowPatch(path=loop,arrowstyle='->',mutation_scale=10,lw=.85,linestyle='--',color='#333333'))
 ax.text(4.68,4.99,'Further selection / formulation',ha='center',fontsize=8.3)
 node(ax,3.0,1.12,3.2,.62,'Memory or reconstruction',8.8);arrow(ax,(6.26,1.4),(7.01,1.0),True)
 ax.text(.1,.82,'Instruction and\nresponse demands',fontsize=9.1,va='center');arrow(ax,(2.42,.81),(7.0,.81),True)
 ax.text(4.73,.2,'Possible direct report routes',fontsize=8.1,ha='center')
 ax=axes[1];ax.text(.05,5.1,'B  Primary study sequence',fontsize=11,fontweight='bold')
 node(ax,.08,2.3,2.12,1.15,'Bank and criterion lock\ncommon baseline',8.7)
 node(ax,2.8,2.3,1.85,1.15,'Participant-level\nrandom assignment',8.7)
 node(ax,5.3,3.25,2.02,1.0,'Own-use\nreflection',9.4);node(ax,5.3,1.25,2.02,1.0,'First-order\nrelational work',9.4)
 node(ax,8.02,2.3,1.83,1.15,'Common held-out\nattribution test',8.9)
 arrow(ax,(2.2,2.87),(2.73,2.87));arrow(ax,(4.65,3.02),(5.23,3.75));arrow(ax,(4.65,2.72),(5.23,1.75));arrow(ax,(7.32,3.75),(7.95,3.1));arrow(ax,(7.32,1.75),(7.95,2.63))
 ax.text(6.31,.72,'Both arms linguistic and relational',fontsize=8.5,ha='center')
 ax.text(.1,.15,'Common procedures may elicit reflection; independent validation precedes confirmation.',fontsize=8)
 fig.subplots_adjust(left=.03,right=.985,bottom=.025,top=.98,hspace=.1)
 for ext in ['png','svg','pdf']:fig.savefig(OUT/('Figure_1.'+ext),dpi=300,facecolor='white')
 plt.close(fig)
 caption="Figure 1. Candidate process and primary study sequence. In Panel A, the dashed return represents optional further formulation of an earlier characterization; it implies neither fixed stages nor guaranteed semantic reorganization. Dashed links to conscious content and observed responding are hypotheses, and memory, reconstruction and response demands can also affect reports. The diagram is not an exhaustive causal model. Panel B shows the primary randomized comparison after common procedures; the bank and determinate test items are fixed before allocation, and both arms use the participant's own materials and a common response-format reminder before testing. ChatGPT (OpenAI; historical model unrecorded) assisted the concept and drawing code; Codex (OpenAI, gpt-6.1-sol) revised the code for submission. The schematic is generated deterministically with Python and Matplotlib and contains no participant data."
 (OUT/'Figure_1_Caption.txt').write_text(caption+'\n',encoding='utf8')
if __name__=='__main__':draw()

