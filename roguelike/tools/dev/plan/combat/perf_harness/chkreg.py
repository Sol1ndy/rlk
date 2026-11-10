"""chkreg.py <dp>: the item registry after the real rlk:load — ids unique, registry keys outside ids (the character
entries char_*), every def `stats` value an int (B3: data get of the stat = the old macro substitution)."""
import sys, collections
sys.path.insert(0, '.')
from pworld import new_sim
from psim import Byte
s, pl = new_sim(sys.argv[1])
it = s.storage['rlk:items']
ids, reg = it['ids'], it['registry']
print('ids', len(ids), 'unique', len(set(ids)), 'registry keys', len(reg), 'same set', set(ids) == set(reg))
types = collections.Counter()
bad = []
for i in ids:
    st = reg[i].get('stats', None)
    if st is None:
        types['no stats'] += 1
        continue
    for k, v in st.items():
        types[(k in ('atkPct','atkFlat','hpPct','hpFlat','defPct','defFlat','elemMastery','critChance','critDamage','moveSpeed','atkSpeed','energyRecharge','physBonus','pyroBonus','hydroBonus','electroBonus','cryoBonus','geoBonus','anemoBonus','dendroBonus'), type(v).__name__)] += 1
        if type(v) is not int:
            bad.append((i, k, v))
print(types)
print('non-int stats', bad[:10])
print('engraving ids', len(s.storage['rlk:engravings']['ids']), len(set(s.storage['rlk:engravings']['ids'])))
extra = sorted(set(reg) - set(ids))
print('registry-only', extra)
for e in extra:
    print('  ', e, {k: (v if not isinstance(v, (dict, list)) else type(v).__name__) for k, v in reg[e].items()})
