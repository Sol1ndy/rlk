# The 60 % fail hit (ULT60_LETHAL false; position = the impact point, the dive on the player): 500 per mille
# of the player's max HP through mboss/pl_dot (no dodge, no position check: the failed judge is the hit; #mbDotLethal 0:
# it never kills), the push ring in the same tick (pl_dot has no knockback), the impact effects and sound.
scoreboard players set #mbDotPct mb 500
scoreboard players set #mbDotEl mb 3
scoreboard players set #mbDotLethal mb 0
function rlk:mboss/pl_dot
function rlk:mboss/push/ring {r:25,to:30,kb:3}
execute positioned ~ ~0.1 ~ run function rlk:boss/scarlet/fx/p/dive_impact {r:30}
execute positioned ~ ~ ~ run function rlk:boss/scarlet/fx/p/light_column
execute positioned ~ ~ ~ run function rlk:boss/scarlet/fx/snd/fail_impact
