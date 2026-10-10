# 얼음 마법사: 차지 → 몸 위에 고드름 → 잠시 뒤 떨어짐(직격+폭발 / 바닥이면 폭발만, 한 번만)
execute if score @s cmS matches 1 run return run function rlk:cm/im/charge
execute if entity @e[tag=rlk_body,distance=..12] run scoreboard players set #hold tmp 1
execute if score @s cmCd matches ..0 unless score @s frzT matches 1.. if entity @e[tag=rlk_body,distance=..18] run function rlk:cm/im/start
