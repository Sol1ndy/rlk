# The 60 % fail hit (ULT60_LETHAL false; position = the impact point, the dive on the player): 500 per mille
# of the player's max HP through mboss/pl_dot (no dodge, no position check: the failed judge is the hit; #mbDotLethal 0:
# it never kills), the push ring in the same tick (pl_dot has no knockback), the impact effects and sound.
scoreboard players set #mbDotPct mb 500
scoreboard players set #mbDotEl mb 3
scoreboard players set #mbDotLethal mb 0
function rlk:mboss/pl_dot
function rlk:mboss/push/ring {r:25,to:30,kb:3}
execute positioned ~ ~0.1 ~ run particle minecraft:dust{color:[0.79,0.49,0.87],scale:1.2} ~ ~ ~ 1.2 0.1 1.2 0 30 force @a[tag=player]
execute positioned ~ ~ ~ run particle minecraft:end_rod ~ ~ ~ 0.1 1.6 0.1 0.02 16 force @a[tag=player]
execute positioned ~ ~ ~ run playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.5 1.4 0.17
execute positioned ~ ~ ~ run playsound minecraft:block.amethyst_block.break hostile @a[tag=player] ~ ~ ~ 0.8 1 0.27
