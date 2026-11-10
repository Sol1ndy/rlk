# STUB (lane C, combat overhaul): lane B owns rlk:bal/** (wip/combat-bal, "execute as <enemy> run function rlk:bal/hit {n:<pips>}").
# Lane C calls it on a perfect parry (player/def/par3_go, @s = the attacker: a cm brain, a projectile's owner brain, the boss
# body rlk_mb_body, Raiden, or a vanilla mob). At the merge lane B's file replaces this one (keep B's); this stub only takes
# the macro argument so the call loads and does nothing.
$scoreboard players set #balN tmp $(n)
