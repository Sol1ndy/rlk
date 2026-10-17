# @s = surviving body after /reload (objectives and the registry are fresh, aux entities are gone).
scoreboard players set #mbLive mb 1
execute if entity @s[tag=rlk_mb_dying] run return run function rlk:mboss/death_finish
execute in minecraft:overworld run summon minecraft:marker 200 201 8 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_arena"],Rotation:[180.0f,0.0f]}
scoreboard players set #mbPause mb 0
scoreboard players set #mbNoLeash mb 0
execute unless score #mbId mb matches 1.. run return 0
function rlk:mboss/d/reload
