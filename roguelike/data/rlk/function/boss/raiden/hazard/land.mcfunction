# A hit (an avoided one also consumes it). Group members share it; nododge ignores dodges and i-frames.
# Combat overhaul C: the hit context of player/def/judge (Raiden = boss class): kind 2 for the travelling kinds
# (sweep / slab / orb), 1 for the rects, else 3; unparriable = nododge (돌진, 수천수만의 염원, guard recovery, 만겁 베기)
# and the field / safe-dome kinds; reset after the call (a refused hurt leaves nothing behind). No knockback when parried.
scoreboard players add @s rdHHit 1
execute if score @s rdHGrp matches 1.. run function rlk:boss/raiden/hazard/grp
scoreboard players operation #cmDmg tmp = @s rdDamage
scoreboard players operation #cmLv tmp = @s mlv
scoreboard players set #cmEl tmp 3
scoreboard players set #dodged tmp 0
scoreboard players set #parT tmp 0
scoreboard players set #hcK tmp 3
execute if score @s rdHK matches 5..7 run scoreboard players set #hcK tmp 2
execute if score @s rdHK matches 3..4 run scoreboard players set #hcK tmp 1
scoreboard players set #hcNP tmp 0
execute if entity @s[tag=rlk_rd_nododge] run scoreboard players set #hcNP tmp 1
execute if score @s rdHK matches 9..10 run scoreboard players set #hcNP tmp 1
execute if entity @s[tag=rlk_rd_nododge] run function rlk:boss/raiden/hazard/land_nd
execute unless entity @s[tag=rlk_rd_nododge] run function rlk:boss/raiden/hurt
scoreboard players set #hcK tmp 0
scoreboard players set #hcNP tmp 0
scoreboard players set #hcND tmp 0
execute if score @s rdHKb matches 1.. unless score #dodged tmp matches 1 unless score #parT tmp matches 1.. run function rlk:boss/raiden/hazard/kb
execute if score @s rdHK matches 5..9 at @e[tag=rlk_body,limit=1] run function rlk:boss/raiden/hazard/vis/impact
