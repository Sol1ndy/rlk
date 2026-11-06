# 하던 공격 취소 (@s = 무리 몹 두뇌, cm/cancel 에서): 빛나는 무기 · 바닥 고리 정리
execute as @e[tag=rlk_c3glow,distance=..6] if score @s cmId = #cid tmp run data merge entity @s {Glowing:0b}
execute as @e[tag=rlk_c3ring,distance=..6] if score @s cmId = #cid tmp run kill @s
execute if entity @s[tag=rlk_cm_cw] run function rlk:cm/cw/stop
scoreboard players set @s cmT 0
