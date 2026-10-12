# As the boss. 0.26 block/tick: walking cannot outrun it, sprinting/dashing can.
execute as @e[tag=rlk_rd_shadow,limit=1] at @s facing entity @e[tag=rlk_body,limit=1] feet positioned ^ ^ ^0.26 unless entity @e[tag=rlk_body,distance=..0.3] run tp @s ~ 201.03 ~
scoreboard players add #rdShadowT rd 1
execute if score #rdShadowT rd matches 8.. run function rlk:boss/raiden/shadow/bite
