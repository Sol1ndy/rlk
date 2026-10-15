# @s = 플레이어. 골드 차감 + 아이템 지급 + 구매 성공 표시
# 상점 노드의 회복(아이템이 아님): 보유 칸과 상관없이 체력 회복
execute if data storage rlk:shop {buyid:"heal_s"} run return run function rlk:shop/node/heal {id:"heal_s"}
execute if data storage rlk:shop {buyid:"heal_l"} run return run function rlk:shop/node/heal {id:"heal_l"}
scoreboard players set #ol tmp 0
execute store result score #ol tmp run data get storage rlk:pinv order
execute if score #ol tmp >= @s invCap run return run function rlk:shop/full_msg
scoreboard players operation @s gold -= #buyprice tmp
data modify storage rlk:pinv order append from storage rlk:shop buyid
function rlk:player/inv/place_items
scoreboard players set #bought tmp 1
execute unless score #k202 snd matches 1 run function rlk:snd/f221
execute unless score #k203 snd matches 1 run function rlk:snd/f222
