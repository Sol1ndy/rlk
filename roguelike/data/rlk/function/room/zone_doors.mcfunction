# 이 구역의 통로를 드러냄 (@s = 구역 표식)
scoreboard players operation #zb tmp = @s zid
execute as @e[tag=rlk_door] if score @s da = #zb tmp run function rlk:room/door_show
execute as @e[tag=rlk_door] if score @s db = #zb tmp run function rlk:room/door_show
