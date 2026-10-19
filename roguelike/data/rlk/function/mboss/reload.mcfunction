# @s = surviving body after /reload (objectives and the registry are fresh, aux entities are gone).
scoreboard players set #mbLive mb 1
execute if entity @s[tag=rlk_mb_dying] run return run function rlk:mboss/death_finish
execute in minecraft:overworld run function rlk:mboss/ar/marker
scoreboard players set #mbPause mb 0
scoreboard players set #mbNoLeash mb 0
execute unless score #mbId mb matches 1.. run return 0
# hit proxies (rlk_mb_aux: killed by init) come back in their current state set (rlk:mboss px.set)
execute if score #mbPx mb matches 1 run function rlk:mboss/px/spawn
function rlk:mboss/d/reload
