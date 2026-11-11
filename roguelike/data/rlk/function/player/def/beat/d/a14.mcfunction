# 14틱: 느린 화면이 끝나고 제 속도로 뒤로 넘는다. 시야 되돌림, 낮은 바람 소리
execute as @a[tag=player] run attribute @s minecraft:movement_speed modifier remove rlk:beat_fov
execute at @e[tag=rlk_body,limit=1] run playsound minecraft:item.trident.riptide_1 player @a[tag=player] ~ ~ ~ 0.45 0.7
execute at @e[tag=rlk_body,limit=1] run playsound minecraft:entity.phantom.flap player @a[tag=player] ~ ~ ~ 0.7 0.6
