# @s = 플레이어. 골드 차감 + 아이템 지급 + 구매 성공 표시
scoreboard players set #ol tmp 0
execute store result score #ol tmp run data get storage rlk:pinv order
execute if score #ol tmp matches 9.. run function rlk:shop/full_msg
execute if score #ol tmp matches 9.. run return 0
scoreboard players operation @s gold -= #buyprice tmp
data modify storage rlk:pinv order append from storage rlk:shop buyid
function rlk:player/inv/place_items
scoreboard players set #bought tmp 1
execute unless score #k202 snd matches 1 run function rlk:snd/f221
execute unless score #k203 snd matches 1 run function rlk:snd/f222
