# 쇄빙: 자신에게 물리 피해
particle minecraft:block{block_state:"minecraft:ice"} ~ ~1 ~ 0.4 0.6 0.4 0.1 40
execute unless score #k57 snd matches 1 run function rlk:snd/f71
scoreboard players set #qU tmp 0
function rlk:element/aoe_hit
