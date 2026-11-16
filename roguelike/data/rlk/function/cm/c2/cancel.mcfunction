# 하던 공격 취소 (@s = 무리 몹 두뇌, cm/cancel 에서): 빛나는 무기 · 바닥 고리 정리
execute as @e[tag=rlk_c2glow,distance=..6] if score @s cmId = #cid tmp run data merge entity @s {Glowing:0b}
execute as @e[tag=rlk_c2ring,distance=..6] if score @s cmId = #cid tmp run kill @s
scoreboard players set @s cmT 0
