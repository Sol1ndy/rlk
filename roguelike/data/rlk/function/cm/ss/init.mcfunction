execute store result score @s c2T run random value 3..10
scoreboard players set @s c2T2 0
execute store result score @s cmCd run random value 16..30
function rlk:cm/ss/rig/create
tag @e[tag=rlk_c2this] remove rlk_c2this
