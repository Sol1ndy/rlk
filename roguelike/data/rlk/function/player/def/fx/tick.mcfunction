# @s = 효과 엔티티, at @s. cb = 남은 틱
scoreboard players remove @s cb 1
execute if score @s cb matches ..0 run return run kill @s
execute if entity @s[tag=rlk_cb_star] run return run function rlk:player/def/fx/t_star
execute if entity @s[tag=rlk_cb_glint] run return run function rlk:player/def/fx/t_glint
execute if entity @s[tag=rlk_cb_arc] run return run function rlk:player/def/fx/t_arc
execute if entity @s[tag=rlk_cb_jolt] if score @s cb matches 1 run rotate @a[tag=player,limit=1] ~-1.5 ~1
