# own cicins (not brains of their own: no rlk_cmb, linked by rlk_cmlink, so they die with the caster):
# tick each one, count (#ccN), any ram in progress (#ccR), idle ones tagged for the next ram, pass the haste on
scoreboard players set #ccN tmp 0
scoreboard players set #ccR tmp 0
scoreboard players operation #c2es tmp = #eStep tmp
scoreboard players set #c2hs tmp 0
execute if entity @s[tag=rlk_cm_haste] run scoreboard players set #c2hs tmp 1
execute as @e[tag=rlk_cm_ci] if score @s c2eOw = #cid tmp at @s run function rlk:cm/cc/flock_one
scoreboard players operation #eStep tmp = #c2es tmp
execute if score #ccN tmp matches 0 if score @s c2eF matches 1 run function rlk:cm/cc/flock_gone
execute if score @s cmD matches 1.. run scoreboard players operation @s cmD -= #eStep tmp
execute if score #ccR tmp matches 0 if score @s cmD matches ..0 if entity @e[tag=rlk_ci_idle,limit=1] run function rlk:cm/cc/flock_ram
tag @e[tag=rlk_ci_idle] remove rlk_ci_idle
