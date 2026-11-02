# The forced bond (api.BOND_CALLS force; E70 / F1 / Q5 at their brand tick; any executor): +18 % max HP, no damage, no
# dodge; the brand X and the red flash on the player; the heal orbs.
# skipped while the player is dead, reviving (로노바), on a selection screen or in the map (as the butterfly cocoon)
execute unless entity @a[tag=player,scores={dead=0},limit=1] run return 0
execute if entity @a[tag=player,scores={rnDie=1..}] run return 0
execute if entity @a[tag=player,scores={pkMode=1..}] run return 0
execute if entity @a[tag=player,scores={vMap=1..}] run return 0
scoreboard players set #bolPct tmp 18
execute as @a[tag=player,limit=1] run function rlk:boss/arlecchino/bond/add
execute at @e[tag=rlk_body,limit=1] positioned ~ ~1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.3 0.5 0.3 0 40 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] positioned ~ ~1 ~ run particle minecraft:crimson_spore ~ ~ ~ 0.4 0.6 0.4 0 30 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] run playsound minecraft:block.respawn_anchor.set_spawn hostile @a[tag=player] ~ ~ ~ 0.7 1.4 0.23
execute at @e[tag=rlk_body,limit=1] run playsound minecraft:entity.wither.shoot hostile @a[tag=player] ~ ~ ~ 0.4 0.6 0.13
execute at @e[tag=rlk_body,limit=1] run playsound minecraft:block.respawn_anchor.charge hostile @a[tag=player] ~ ~ ~ 0.6 0.7 0.2
function rlk:boss/arlecchino/bond/orbs
