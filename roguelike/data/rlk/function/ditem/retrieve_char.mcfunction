# @s = 플레이어. 바닥의 캐릭터로 교체하고, 지금 캐릭터를 몸의 발밑에 떨군다
scoreboard players set #retok tmp 1
data modify storage rlk:gv id set from storage rlk:chars cur.itemId
function rlk:ditem/kill_group with storage rlk:dtmp
function rlk:char/switch with storage rlk:dtmp ch
execute at @e[tag=rlk_body,limit=1] run function rlk:items/drop with storage rlk:gv
playsound minecraft:entity.player.levelup master @s ~ ~ ~ 0.5 1.6
playsound minecraft:block.beacon.power_select master @s ~ ~ ~ 0.5 1.4
