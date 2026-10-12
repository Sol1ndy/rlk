scoreboard players set #rdShadowT rd 0
execute as @e[tag=rlk_rd_shadow,limit=1] at @s if entity @e[tag=rlk_body,distance=..1.8] run function rlk:boss/raiden/shadow/hurt
