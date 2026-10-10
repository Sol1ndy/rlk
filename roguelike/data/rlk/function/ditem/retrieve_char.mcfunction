# @s = 플레이어. 바닥의 캐릭터로 교체하고, 지금 캐릭터를 몸의 발밑에 떨군다
scoreboard players set #retok tmp 1
data modify storage rlk:gv id set from storage rlk:chars cur.itemId
function rlk:ditem/kill_group with storage rlk:dtmp
function rlk:char/switch with storage rlk:dtmp ch
execute at @e[tag=rlk_body,limit=1] run function rlk:items/drop with storage rlk:gv
execute unless score #k2 snd matches 1 run function rlk:snd/f415
execute unless score #k73 snd matches 1 run function rlk:snd/f78
