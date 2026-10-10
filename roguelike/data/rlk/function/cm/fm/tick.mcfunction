# 불 마법사: 화염구 3개를 차지(머리 위에 하나씩 생김) → 하나씩 발사. 차지/발사 중 경직 면역
execute if score @s cmS matches 1 run return run function rlk:cm/fm/charge
execute if score @s cmS matches 2 run return run function rlk:cm/fm/volley
execute if entity @e[tag=rlk_body,distance=..11] run scoreboard players set #hold tmp 1
execute if score @s cmCd matches ..0 unless score @s frzT matches 1.. if entity @e[tag=rlk_body,distance=..16] run function rlk:cm/fm/start
