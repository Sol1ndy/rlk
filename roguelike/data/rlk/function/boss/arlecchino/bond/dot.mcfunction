# The bond DoT (@s = body; only while HER bond is on the player): 10 per mille every 50 t,
# Pyro (the element shield absorbs as usual), never lethal (pl_dot leaves 1 HP).
scoreboard players add #dot_t kn 1
execute if score #dot_t kn matches ..49 run return 0
scoreboard players set #dot_t kn 0
scoreboard players set #mbDotPct mb 10
scoreboard players set #mbDotEl mb 1
scoreboard players set #mbDotLethal mb 0
function rlk:mboss/pl_dot
execute at @e[tag=rlk_body,limit=1] run function rlk:boss/arlecchino/fx/snd/bond_tick
