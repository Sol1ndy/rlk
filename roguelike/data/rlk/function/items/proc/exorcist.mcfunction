scoreboard players set @s infuse 4
# 부여 지속 시간 = #exoDur (강화 단계로 조정)
scoreboard players operation @s infuseT = #exoDur tmp
data modify storage rlk:hud inf set from storage rlk:elem byid."ice".tag
execute at @e[tag=rlk_body,limit=1] run particle minecraft:snowflake ~ ~1 ~ 0.3 0.5 0.3 0.03 10
