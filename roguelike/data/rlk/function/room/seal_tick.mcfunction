# @s = 봉인 무늬의 선 하나 (매 틱). sph: 0 대기 → 1 그어짐/수축 → 2 부풂 → (1 ↔ 2 맥동) / 9 사라지는 중
scoreboard players add @s sT 1
execute if score @s sph matches 0 if score @s sT >= @s sdelay run return run function rlk:room/seal_grow
execute if score @s sph matches 9 if score @s sT matches 7.. run return run kill @s
execute if entity @s[tag=rlk_spulse] if score @s sph matches 1 if score @s sT matches 22.. run return run function rlk:room/seal_swell
execute if entity @s[tag=rlk_spulse] if score @s sph matches 2 if score @s sT matches 18.. run return run function rlk:room/seal_rest
