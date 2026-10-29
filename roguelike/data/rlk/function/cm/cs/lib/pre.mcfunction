# every tick, first: haste (tag rlk_cm_haste set by a drumming 북잡이) -> #eStep 1 or 2
execute if entity @s[tag=rlk_cm_haste,tag=!rlk_c2_hs] run function rlk:cm/cs/lib/haste_on
execute if entity @s[tag=!rlk_cm_haste,tag=rlk_c2_hs] run function rlk:cm/cs/lib/haste_off
scoreboard players set #eStep tmp 1
execute if entity @s[tag=rlk_c2_hs] run function rlk:cm/cs/lib/haste_step
execute unless score @s c2eQ matches 1 run function rlk:cm/cs/lib/first
