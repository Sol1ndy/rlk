# @s = 플레이어. 회수: 보유 목록(order)에 추가 후 재배치, 드롭 그룹 제거
scoreboard players set #retok tmp 1
function rlk:ditem/retrieve_getid with storage rlk:dtmp
data modify storage rlk:pinv order append from storage rlk:dtmp id
function rlk:player/inv/place_items
function rlk:ditem/kill_group with storage rlk:dtmp
playsound minecraft:entity.item.pickup master @s ~ ~ ~ 1 1.2
playsound minecraft:entity.experience_orb.pickup master @s ~ ~ ~ 0.6 1.4
