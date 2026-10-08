# 쇄빙: 자신에게 물리 피해
particle minecraft:block{block_state:"minecraft:ice"} ~ ~1 ~ 0.4 0.6 0.4 0.1 40
playsound minecraft:block.glass.break master @a ~ ~ ~ 1 0.7
scoreboard players set #qU tmp 0
function rlk:element/aoe_hit
