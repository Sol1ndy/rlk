scoreboard players set @s cmS 0
scoreboard players set @s cmAR 11
scoreboard players operation @s cmCd = #cmCd_im tmp
tag @s remove rlk_cmch
function rlk:cm/swing
scoreboard players set #rl tmp 0
execute at @e[tag=rlk_body,limit=1] positioned ~ ~2.3 ~ run function rlk:cm/im/up
execute unless score #k80 snd matches 1 run function rlk:snd/f86
