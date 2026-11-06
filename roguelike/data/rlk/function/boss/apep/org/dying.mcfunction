# @s = a dying organism: its death clip plays (om/tick); removed at the clip end. A 파괴 that blew is flung 2.5 b
# away from the Heart over its first 5 t.
execute if entity @s[tag=rlk_mb_ap_spent] if score @s apT matches ..5 facing entity @e[type=minecraft:marker,tag=rlk_mb_ap_heart,limit=1] feet rotated ~180 0 run function rlk:mboss/mv/step_flat {spd:0.5}
execute if score @s apK matches 1 if score @s apT matches 10.. run return run function rlk:boss/apep/org/remove
execute if score @s apK matches 2 if score @s apT matches 17.. run return run function rlk:boss/apep/org/remove
execute if score @s apK matches 3 if score @s apT matches 17.. run return run function rlk:boss/apep/org/remove
execute if score @s apK matches 4 if score @s apT matches 12.. run return run function rlk:boss/apep/org/remove
execute if score @s apK matches 5 if score @s apT matches 10.. run return run function rlk:boss/apep/org/remove
execute if score @s apK matches 6 if score @s apT matches 12.. run return run function rlk:boss/apep/org/remove
