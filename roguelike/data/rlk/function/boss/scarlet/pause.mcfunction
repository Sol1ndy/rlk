# Hook pause (the fight froze: dead, reviving, a menu, no player; @s = body): the kit cards go; a pattern's own pause;
# a running gauntlet is cancelled (hazards, discs, ghost, the banner off, the darkness lifted) and restarts at resume
# through lead_stand {g} from T0 with 5/5 (PLAN §3.8 / §5.6); after its fatal: the revive stance; after a judged
# deflect: the counter cinematic; after the judged A8 fail: P2 at once (#grs 4, F1 HR-01); a lethal gauntlet paused
# past its last counting cut with pips left: its fail at the resume (#grs 5, core/g/fail_now, F1 HR-07).
function rlk:boss/scarlet/fx/clear
execute if score #pat hr matches 21.. run function rlk:boss/scarlet/core/g/pause
