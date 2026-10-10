# 대쉬가 1칸 단차에 막힘 (@s = 플레이어, 위치 = 몸): 한 칸 위가 비어 있으면 올라선다. 대쉬 한 번에 한 번만
execute if score @s dashUpN matches 1.. run return 0
scoreboard players set #dblk tmp 0
$execute if score @s dashDX matches 1.. positioned ~$(dx) ~1 ~ run function rlk:player/dash_chk_xp
$execute if score @s dashDX matches ..-1 positioned ~$(dx) ~1 ~ run function rlk:player/dash_chk_xn
$execute if score #dblk tmp matches 0 run tp @e[tag=rlk_body,limit=1] ~$(dx) ~1 ~
execute if score #dblk tmp matches 0 run scoreboard players set @s dashUpN 1
execute if score #dblk tmp matches 1 run return 0
