# 카메라 자리 찾기 (@s = 플레이어, 위치 = 아바타 머리에서 카메라 쪽으로 가는 중, 방향 = 플레이어 시선). 벽에 막히면 그 앞에서 멈춤
scoreboard players set #cb view 0
$execute positioned ^$(lx) ^$(ly) ^$(lz) unless block ~ ~ ~ #rlk:view_pass run scoreboard players set #cb view 1
# 다음 자리의 네 귀퉁이(눈 주위 상자)가 벽에 닿으면 멈춤: 문틀·모서리에 끼어 질식 피해를 받지 않게
$execute positioned ^$(x) ^$(y) ^$(z) positioned ~0.3 ~ ~0.3 unless block ~ ~ ~ #rlk:view_pass run scoreboard players set #cb view 1
$execute positioned ^$(x) ^$(y) ^$(z) positioned ~0.3 ~ ~-0.3 unless block ~ ~ ~ #rlk:view_pass run scoreboard players set #cb view 1
$execute positioned ^$(x) ^$(y) ^$(z) positioned ~-0.3 ~ ~0.3 unless block ~ ~ ~ #rlk:view_pass run scoreboard players set #cb view 1
$execute positioned ^$(x) ^$(y) ^$(z) positioned ~-0.3 ~ ~-0.3 unless block ~ ~ ~ #rlk:view_pass run scoreboard players set #cb view 1
execute if score #ci view matches 14.. run scoreboard players set #cb view 1
execute if score #cb view matches 1 run return run function rlk:view/cam_put
scoreboard players add #ci view 1
$execute positioned ^$(x) ^$(y) ^$(z) run function rlk:view/cam_step with storage rlk:view st
