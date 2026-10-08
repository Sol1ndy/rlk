scoreboard players remove @s frzT 1
execute if entity @s[tag=rlk_frz_fix] run function rlk:element/frz_fix
particle minecraft:snowflake ~ ~1 ~ 0.3 0.5 0.3 0 1
execute if score @s frzT matches ..0 run function rlk:element/frz_end
