# 맞음: 3초 동안 영창 못 함(구슬이 터지는 소리 · 물보라)
scoreboard players operation @s c3I = #c3Int_cw tmp
execute if score @s cmS matches 1 run particle minecraft:splash ~ ~2.3 ~ 0.4 0.3 0.4 0.3 30 normal
execute if score @s cmS matches 1 run execute unless score #c3cwbreak snd matches 1 run function rlk:cm/c3/snd/cwbreak
scoreboard players operation #cid tmp = @s cmId
function rlk:cm/cw/stop
