"""Display the stored A6k physical failures. Adityavardhan Mishra."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1];d=json.loads((R/'analysis/results/reconciled_wire_field.json').read_text());rows=[]
for p,key,band,title in [(d['placements'][0],'slot_to_slot_flux_imbalance_fraction','maximum_slot_to_slot_flux_imbalance_fraction','Lower winding / slot imbalance'),(d['placements'][1],'stationary_core_maximum_field_t','maximum_stationary_core_field_t','Upper winding / core field')]:
 limit=p['parameters']['bands'][band];values=[v[key] for v in p['result']['mesh_results'].values()];rows.append((title,max(values),limit))
plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none'})
fig,axs=plt.subplots(1,2,figsize=(11,4.8),facecolor='#101e2b');fig.subplots_adjust(top=.73,bottom=.22,wspace=.35)
fig.text(.045,.9,'The geometry fits. The magnetic candidate fails.',fontsize=19,color='white',weight='bold')
for ax,(title,value,limit) in zip(axs,rows):
 ax.set_facecolor('#101e2b');ax.barh([0],[value/limit],color='#ed8d7a',height=.35);ax.axvline(1,color='#e5eef3',ls='--');ax.set_yticks([]);ax.set_xlim(0,2.05);ax.set_title(title,color='white',fontsize=12);ax.set_xlabel('Worst sampled value / acceptance limit',color='#ccdce5');ax.tick_params(colors='#ccdce5');ax.spines[['top','right','left']].set_visible(False);ax.text(.04,.83,f'{value:.6f} / {limit:g}',color='#ed8d7a',transform=ax.transAxes,fontsize=14)
fig.text(.045,.055,'A6k stored results · All three meshes counted · Numerical convergence is not physical acceptance.',color='#ccdce5',fontsize=10)
(R/'docs/assets').mkdir(exist_ok=True);fig.savefig(R/'docs/assets/field-decision.svg',facecolor=fig.get_facecolor());plt.close(fig)
print(rows)
