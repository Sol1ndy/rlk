scoreboard players operation #fn tmp = @s cmN
scoreboard players set @s cmAR 11
function rlk:cm/swing
execute as @e[tag=rlk_cmfbh,distance=..6] if score @s cmId = #cid tmp if score @s cmN = #fn tmp at @s facing entity @e[tag=rlk_cmaim,limit=1] feet run function rlk:cm/fm/launch
scoreboard players add @s cmN 1
scoreboard players operation @s cmT = #cmW_fmG tmp
execute if score @s cmN matches 4.. run function rlk:cm/fm/done
