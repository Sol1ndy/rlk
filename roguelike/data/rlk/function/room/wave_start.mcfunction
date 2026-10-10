# 구역에 들어선 순간 (@s = 구역 표식, at @s): 통로는 바로 드러내고, 바닥은 플레이어가 선 자리에서 물결처럼 퍼지며 바뀜
# (지어지기만 하고 아직 안 들어간 구역 = 응회암 벽돌 바닥(지도에서 어두운 갈색), 들어가 본 구역 = 어두운 타일)
function rlk:room/zone_doors
execute if data entity @s data{boss_id:"narukami"} run return 0
execute store result score @s wx run data get entity @e[tag=rlk_body,limit=1] Pos[0]
execute store result score @s wz run data get entity @e[tag=rlk_body,limit=1] Pos[2]
scoreboard players set @s wr 0
tag @s add rlk_wave
