function rlk:char/motion/cleanup
scoreboard players set #bcStep view 0
function rlk:view/burst_camera_apply
# 숄더뷰 정리 (@s = 플레이어): 아바타가 있던 자리로 돌아와 다시 1인칭
execute if score @s vMap matches 1 run function rlk:view/map_close
execute unless score @s pkMode matches 1.. unless score @s dead matches 1 at @e[tag=rlk_av,limit=1] run tp @s ~ ~ ~ ~ ~
function rlk:view/ride_off
kill @e[tag=rlk_view]
effect clear @s minecraft:invisibility
attribute @s minecraft:movement_speed modifier remove rlk:view_sprint
scoreboard players set #spr view 0
attribute @s minecraft:gravity base set 0.08
attribute @s minecraft:camera_distance base reset
team join rlk_stun @s
team leave @e[tag=rlk_mob]
tag @s add rlk_body
kill @e[tag=rlk_shfx]
