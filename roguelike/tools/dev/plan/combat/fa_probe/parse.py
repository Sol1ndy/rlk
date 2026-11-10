"""parse.py <probe log>: the storage dump of probe.sh as tables (fix lane FA, real 26.3 server)."""
import re, sys
sys.dont_write_bytecode = True
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'sim/cb/tests/lib'))   # the SNBT reader of psim
from psim import snbt_parse
log = open(sys.argv[1], encoding='utf-8', errors='replace').read()
m = re.findall(r'Storage rvp:log has the following contents: (.*)', log)
d = snbt_parse(m[-1])
print('A-03 run 1 (fixed-UUID mannequin with the ghost NBT; per tick after rlk:tick): t sel(@e sees it) ex(uuid exists) cb DeathTime Glowing Pos')
for r in d.get('rows', []):
    pos = r.get('pos'); pos = [round(float(x), 1) for x in pos] if pos else None
    print(f"  t{r['t']:2d} sel {r['sel']} ex {r['ex']} cb {r.get('cb')} dt {r.get('dt')} glow {r.get('glow')} pos {pos}")
print('A-06:', {k: v for k, v in d.get('a06', {}).items()})
print('A-03 run 2 (the pack\'s own fx/pd ghost; per tick): t ghost-tagged, mannequins tagged rlk_cb_fx, mannequins within 32 b of the dodge start, Glowing, Pos, box')
for r in d.get('rows2', []):
    pos = r.get('pos'); pos = [round(float(x), 1) for x in pos] if pos else None
    print(f"  t{r['t']:2d} ghost {r.get('ghost')} mann {r.get('mann')} near {r.get('near')} glow {r.get('glow')} pos {pos} box {r.get('box')}")
print('A-07:', d.get('a07'))
print('A-02:', d.get('a02'))
print('A-01:', [(int(x['p']), int(x['acc'])) for x in d.get('a01', [])])
tests = re.findall(r'Test (passed|failed)', log)[-2:]
print('left at the end: any mannequin / any rlk_dgo box:', tests, '(failed = none left)')
print('tick:', re.findall(r'Average time per tick: [^\n]*', log)[-1:])
