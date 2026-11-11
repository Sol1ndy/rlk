# 2틱: 쳐낸 자세로 얼어붙는 순간. 접점에 별빛(멈춘 4틱 동안 그대로), 화면에 따뜻한 빛 + 가로 줄, 울림 소리, 공격자가 뒤로 젖혀짐,
# 화면이 살짝 당겨짐(시야 −5%: 이동 속도 수정자, 달리기 시야와 같은 길; 6틱에 그대로 되돌아감 — 시점은 건드리지 않는다)
execute at @e[type=minecraft:marker,tag=rlk_bt_pt,limit=1] run function rlk:player/def/fx/p3_star
function rlk:player/def/fx/ovl {g:"parry",in:0,hold:4,out:3,t:7}
execute as @e[tag=rlk_bt_atk,limit=1] at @s run function rlk:player/def/beat/rock_on
execute as @a[tag=player,limit=1] unless score @s devMode matches 1 run attribute @s minecraft:movement_speed modifier add rlk:beat_fov -0.1 add_multiplied_total
