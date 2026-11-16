# Knock-back through the engine push path (player/knockback: 0.1-block steps with block checks), away from the
# hazard origin; #cmKB = rdHKb steps (k steps push 0.05 k (k+1) blocks). The engine stops it at the wall.
kill @e[tag=rlk_plkb_source]
execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_plkb_source","rlk_rd_kbsrc"]}
execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~180 0 run tp @e[tag=rlk_rd_kbsrc,limit=1] ~ ~ ~ ~ 0
scoreboard players operation #cmKB tmp = @s rdHKb
execute as @a[tag=player,limit=1] run function rlk:player/knockback/start
kill @e[tag=rlk_rd_kbsrc]
