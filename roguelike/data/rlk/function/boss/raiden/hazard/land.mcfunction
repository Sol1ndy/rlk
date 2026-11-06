# A hit (a dodge also consumes it). Group members share it; nododge ignores the dash i-frames.
scoreboard players add @s rdHHit 1
execute if score @s rdHGrp matches 1.. run function rlk:boss/raiden/hazard/grp
scoreboard players operation #cmDmg tmp = @s rdDamage
scoreboard players operation #cmLv tmp = @s mlv
scoreboard players set #cmEl tmp 3
scoreboard players set #dodged tmp 0
execute if entity @s[tag=rlk_rd_nododge] run function rlk:boss/raiden/hazard/land_nd
execute unless entity @s[tag=rlk_rd_nododge] run function rlk:boss/raiden/hurt
execute if score @s rdHKb matches 1.. unless score #dodged tmp matches 1 run function rlk:boss/raiden/hazard/kb
execute if score @s rdHK matches 5..9 at @e[tag=rlk_body,limit=1] run function rlk:boss/raiden/hazard/vis/impact
