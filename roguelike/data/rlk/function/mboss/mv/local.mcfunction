# As the anchor (the body; cm.md 13.2): #mbLf / #mbLs mb = the player's body in the anchor frame, milliblocks (f forward
# along the anchor yaw, s = the anchor's left), the hz/hit projection on an exact forward axis (no trigonometry).
scoreboard players set #mbLf mb 0
scoreboard players set #mbLs mb 0
execute unless entity @e[tag=rlk_body,limit=1] run return fail
execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^1 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_lcax"]}
execute store result score #ox mb run data get entity @s Pos[0] 1000
execute store result score #oz mb run data get entity @s Pos[2] 1000
execute store result score #fx mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_lcax,limit=1] Pos[0] 1000
execute store result score #fz mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_lcax,limit=1] Pos[2] 1000
kill @e[type=minecraft:marker,tag=rlk_mb_lcax]
scoreboard players operation #fx mb -= #ox mb
scoreboard players operation #fz mb -= #oz mb
execute store result score #dx mb run data get entity @e[tag=rlk_body,limit=1] Pos[0] 1000
execute store result score #dz mb run data get entity @e[tag=rlk_body,limit=1] Pos[2] 1000
scoreboard players operation #dx mb -= #ox mb
scoreboard players operation #dz mb -= #oz mb
scoreboard players operation #mbLf mb = #dx mb
scoreboard players operation #mbLf mb *= #fx mb
scoreboard players operation #t mb = #dz mb
scoreboard players operation #t mb *= #fz mb
scoreboard players operation #mbLf mb += #t mb
scoreboard players operation #mbLf mb /= #c1000 mb
scoreboard players operation #mbLs mb = #dx mb
scoreboard players operation #mbLs mb *= #fz mb
scoreboard players operation #t mb = #dz mb
scoreboard players operation #t mb *= #fx mb
scoreboard players operation #mbLs mb -= #t mb
scoreboard players operation #mbLs mb /= #c1000 mb
return 1
