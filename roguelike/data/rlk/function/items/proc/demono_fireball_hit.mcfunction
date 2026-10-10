# @s = 피격 몹, at @s. 서리 화살 착탄
particle minecraft:snowflake ~ ~1 ~ 0.4 0.5 0.4 0.08 30
particle minecraft:block{block_state:"minecraft:ice"} ~ ~1 ~ 0.3 0.4 0.3 0.1 14
execute unless score #k130 snd matches 1 run function rlk:snd/f194
function rlk:combat/apply
