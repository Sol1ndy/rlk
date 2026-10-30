# 48틱마다 부품 수 확인(리로드 · 청크 문제로 빠진 부품이 있으면 다시 만듦)
scoreboard players set @s cmAF 0
execute store result score #c2cnt tmp if entity @e[tag=rlk_c2this]
execute if score #c2cnt tmp matches 2 run return 0
kill @e[tag=rlk_c2this]
function rlk:cm/ss/rig/create
scoreboard players set @s cmAP -1
