# 6틱: 풀림. 공격자를 제자리로(세계의 틱보다 먼저), 별빛이 불꽃으로 깨져 날아감, 시야 되돌림
execute if score #btRk cb matches 1 run function rlk:player/def/beat/rock_off
execute at @e[type=minecraft:marker,tag=rlk_bt_pt,limit=1] run function rlk:player/def/fx/p3_shatter
execute as @a[tag=player] run attribute @s minecraft:movement_speed modifier remove rlk:beat_fov
