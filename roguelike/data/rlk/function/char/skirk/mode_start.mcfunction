# 일곱빛 섬광 시작
scoreboard players operation @s skM = #skModeDur tmp
scoreboard players set #skMode tmp 1
scoreboard players set @s buShown -1
attribute @s minecraft:knockback_resistance modifier add rlk:skirk 1 add_value
playsound minecraft:block.beacon.activate master @a ~ ~ ~ 0.7 1.8
playsound minecraft:block.glass.break master @a ~ ~ ~ 0.6 0.7
particle minecraft:snowflake ~ ~1 ~ 0.6 0.8 0.6 0.08 40
particle minecraft:dust{color:[0.62f,0.91f,0.96f],scale:1.6f} ~ ~1 ~ 0.7 0.9 0.7 0 25
particle minecraft:reverse_portal ~ ~1 ~ 0.4 0.6 0.4 0.05 30
