# @s = a new aux made with #auxShW mb (aux/setup, cm.md 13.12): its click shield made now, #auxShW x #auxShH tenths of a
# block (#auxShH unset = 22), linked by msid and marked synced, so mob/shield_ensure keeps it (no 1.2 x 2.2 default).
execute unless score @s msid matches 1.. run scoreboard players add #msidC tmp 1
execute unless score @s msid matches 1.. run scoreboard players operation @s msid = #msidC tmp
summon minecraft:interaction ~ ~ ~ {Tags:["rlk_mshield","rlk_msync","rlk_mb_shnew"],width:1.2f,height:2.2f,response:false}
scoreboard players operation @e[type=minecraft:interaction,tag=rlk_mb_shnew,limit=1] msid = @s msid
execute store result entity @e[type=minecraft:interaction,tag=rlk_mb_shnew,limit=1] width float 0.1 run scoreboard players get #auxShW mb
execute if score #auxShH mb matches 1.. store result entity @e[type=minecraft:interaction,tag=rlk_mb_shnew,limit=1] height float 0.1 run scoreboard players get #auxShH mb
tag @e[type=minecraft:interaction,tag=rlk_mb_shnew] remove rlk_mb_shnew
