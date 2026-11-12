"""The 5-segment gauge inside a gauntlet, the judge and the two fail hits of 홍련 (hr_design §1.2, §2.4; lane H1; the
gauntlets call it through api.shield()): shield/arm, shield/tick (the core's per-tick segment check), shield/take,
shield/judge, ult/fail60, ult/fatal, shield/off, and the under bar (hud/bar_shield: #buSub = #gau / 10, #buSubMax 5,
colour api.BU_SHIELD).

The gauge is api.GAUGE_FP (#gau hr, 0-50 = tenths of a segment). Outside the gauntlets the core charges it (core/gauge/*:
+3 per pattern, +5 per landed hit) and U spends it; inside:
- shield/arm (any executor): #gau = 50 in one step (lead60's tick 0, the lead-ins' refill beat #sq_sig refill), #gres 0.
  Silent: the refill effect and sound are the sequence's.
- shield/tick: run by the core every tick of a gauntlet, right after p/<g>/tick. api.PIP_RULE 'perfect_parry': a cut is a
  normal parryable hazard; when its hit on the player was judged a perfect parry the framework leaves #mbDodgeOk mb 1
  (mboss/hurt_dodge) with #parT tmp 3 - the hazard strikes after the module tick, so the module sees it one tick later
  (two for the second tick of the cut's 2-t active window). Then one segment goes (shield/take: -10, never below 0, the
  kit's pip_break at the player + its sound) and #mbDodgeOk is cleared. A perfect dodge (#mbDodgeOk 1, #parT 0), a tier
  2 / 1 parry (a landed hit: no #mbDodgeOk) and walking out take nothing. One cut = one hazard = at most one hit.
- shield/judge (@s any): #gres hr = 1 (the gauge is 0: the deflect; the core starts seq/repel in this tick and the repel's
  first frames are the gold deflect) or 2 (fail: the gauntlet's own branch follows); the gauge is 0 after either outcome.
- ult/fail60 (position = the impact point): mboss/pl_dot api.FAIL60_PM per mille of the player's max HP, Electro,
  #mbDotLethal 0 (never kills), the push ring mboss_lib.push_ring(*api.FAIL60_PUSH) there in the same tick, the impact
  effects (kit dive_impact {r:30} + light_column) and the fail_impact sound.
- ult/fatal (@s = the player; F:boss/raiden/hazard/fatal's model): nothing while the player is reviving (rnDie >= 1);
  else player/hurt_do with all current HP (Electro), curHealth 0, player/die: it bypasses mboss/hurt, so i-frames, parries
  and every shield are ignored; Ronova's one revive still applies; a death in a test ends in mboss/test/defeat.
- shield/off (any executor): #gau 0 (a cancelled gauntlet, death, cleanup).
"""
from . import api
from . import s3lib as S
from . import blade as B
from .s3lib import sset, fn, part

L, K = api.L, api.K
OBJ = api.OBJ
GAU = api.GAUGE_FP
G = api.GAUGE


FAIL_COL_W, FAIL_COL_T, FAIL_COL_TAG = 0.3, 5, 'rlk_hr_sw_col'
FAIL_COL_RGB = 0xE2B4FF                 # lilac (round V's slash colour)


def build(W):
    w = W.w
    w('shield/arm', [f'# The gauge full ({G["max"]} = 5 segments) in one step (lead60 tick 0, a lead-in\'s refill beat); the last judge',
                     '# result gone.', sset(GAU, G['max']), sset('#shb', 1), sset('#gres', 0)])
    w('shield/off', ['# The gauge empty (a cancelled gauntlet, death, cleanup).', sset(GAU, 0), sset('#shb', 0)])
    w('shield/tick', [
        '# Every gauntlet tick after p/<g>/tick (the core): a cut\'s hit judged a perfect parry (#mbDodgeOk mb 1 from',
        '# mboss/hurt_dodge with #parT tmp 3) takes one segment; a perfect dodge (#parT 0) takes none. The event is cleared.',
        'execute unless score #mbDodgeOk mb matches 1 run return 0',
        'scoreboard players set #mbDodgeOk mb 0',
        'execute unless score #parT tmp matches 3 run return 0',
        f'execute if score #pipoff {OBJ} matches 1 run return 0',
        fn('shield/take')])
    w('shield/take', [f'# One segment goes (-{G["seg"]}, never below 0): the shards and the crack at the player.',
                      f'execute if score {GAU} {OBJ} matches ..0 run return 0',
                      f'scoreboard players remove {GAU} {OBJ} {G["seg"]}',
                      f'execute if score {GAU} {OBJ} matches ..-1 run {sset(GAU, 0)}']
      + S.fx('pip_break', [part(S.DUST['lilac'], 0.4, 0.5, 0.4, 0.1, 14), part('minecraft:end_rod', 0.3, 0.4, 0.3, 0.06, 6)],
             pos=f'at {S.PLAYER} positioned ~ ~1.1 ~')
      + S.snd('pip_break', pos=f'at {S.PLAYER}'))
    w('shield/judge', [
        '# The judge (the final dive\'s contact; the gauntlet at api.JUDGE_T): #gres hr 1 = the gauge is 0 (the deflect: the',
        '# core starts seq/repel in this tick), 2 = fail (the gauntlet\'s own branch follows). The gauge is 0 afterwards.',
        sset('#gres', 1),
        f'execute if score {GAU} {OBJ} matches 1.. run {sset("#gres", 2)}',
        sset(GAU, 0), 'scoreboard players set #mbDodgeOk mb 0'])
    w('ult/fail60', [
        f'# The 60 % fail hit (ULT60_LETHAL false; position = the impact point, the dive on the player): {api.FAIL60_PM} per mille',
        '# of the player\'s max HP through mboss/pl_dot (no dodge, no parry, no position check: the failed judge is the hit;',
        '# #mbDotLethal 0: it never kills), the push ring in the same tick (pl_dot has no knockback), the impact effects and sound.']
      + L.pl_dot(api.FAIL60_PM, api.ELEC, 0)
      + [L.push_ring(*api.FAIL60_PUSH)]
      + S.fx('dive_impact', [part(S.DUST['lilac'], 1.2, 0.1, 1.2, 0, 30)], pos='positioned ~ ~0.1 ~', r=30)
      # round V (v_brief §3 VB 4; review v G2: the kit's 9 b light column - two crossed quads over a block wide on the player's own
      # spot - filled over half the screen for 7 frames when the push carried the lens through it): a thin column instead (a
      # blade.py lance card, FAIL_COL_W wide, 6 b tall; p/<g>/fail's caller removes it FAIL_COL_T t later)
      + [f'execute positioned ~ ~0.1 ~ rotated 0 -90 run ' + B.card('a8', 'sw_rib_0', (0, 0, 0), (0, 0, 0, 1), (FAIL_COL_W, FAIL_COL_W, 6.0),
                                                                  FAIL_COL_RGB, (FAIL_COL_TAG,), tpd=0),
         f'execute positioned ~ ~0.1 ~ rotated 0 -90 run tp {B.SEL.format(B.TAG_NEW)} ~ ~ ~ ~ ~', f'tag {B.SEL.format(B.TAG_NEW)} remove {B.TAG_NEW}']
      + S.snd('fail_impact', pos='positioned ~ ~ ~'))
    w('ult/fatal', [
        '# The 5 % instant death (ULT5_LETHAL true; @s = the player; F:boss/raiden/hazard/fatal\'s model): skipped while the player',
        '# revives; else all current HP as the hit (the number, Electro), curHealth 0, player/die. It bypasses mboss/hurt (i-frames,',
        '# parries and every shield are ignored); Ronova\'s one revive still applies; in a test the death ends in test/defeat.',
        'execute if score @s rnDie matches 1.. run return 0',
        'scoreboard players operation #hurtDmg tmp = @s curHealth',
        f'scoreboard players set #elem tmp {api.ELEC}',
        'function rlk:player/hurt_do',
        'scoreboard players set @s curHealth 0',
        'function rlk:player/die'])
    w('hud/bar_shield', [f'# The under bar = the 5-segment gauge (bars hook): #gau / {G["seg"]} of {api.PIPS}, electro.',
                         f'scoreboard players operation #buSub bu = {GAU} {OBJ}',
                         f'scoreboard players operation #buSub bu /= #c10 {OBJ}',
                         f'scoreboard players set #buSubMax bu {api.PIPS}', f'scoreboard players set #buSubCol bu {api.BU_SHIELD}',
                         # round V (v_brief §3 VB 5): the under bar cut into its 5 segments (bossui: dividers)
                         f'scoreboard players set #buSubSeg bu {api.PIPS}'])
