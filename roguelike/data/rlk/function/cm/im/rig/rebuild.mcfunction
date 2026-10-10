function rlk:cm/im/rig/select
kill @e[tag=rlk_im_this]
execute as @e[tag=rlk_cmv] if score @s cmId = #imId tmp run kill @s
scoreboard players set @s cmAF 0
scoreboard players set @s cmAH 0
scoreboard players set @s cmAR 0
scoreboard players set @s cmAP -1
execute store result score @s cmAX run data get entity @s Pos[0] 1000
execute store result score @s cmAZ run data get entity @s Pos[2] 1000
function rlk:cm/im/rig/create
