# 궁수: 사거리(11칸) 안이면 멈춤. 쿨이 되면(경직 중이어도) 차지 시작 → 빨간 궤적 → 일자 화살
execute if score @s cmS matches 1 run return run function rlk:cm/ar/charge
execute if entity @e[tag=rlk_body,distance=..11] run scoreboard players set #hold tmp 1
execute if score @s cmCd matches ..0 unless score @s frzT matches 1.. if entity @e[tag=rlk_body,distance=..17] run function rlk:cm/ar/start
