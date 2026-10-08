# macro: i, j = 보유 목록의 순번. 목록에서 둘을 맞바꾸고 실물(inventory.9~17)을 다시 놓는다
scoreboard players set @s pkSel -1
scoreboard players set @s pkRedraw 1
$execute unless data storage rlk:pinv order[$(i)] run return 0
$execute unless data storage rlk:pinv order[$(j)] run return 0
$data modify storage rlk:lvpick sw.a set from storage rlk:pinv order[$(i)]
$data modify storage rlk:pinv order[$(i)] set from storage rlk:pinv order[$(j)]
$data modify storage rlk:pinv order[$(j)] set from storage rlk:lvpick sw.a
function rlk:player/inv/place_items
scoreboard players set @s invDirty 2
playsound minecraft:item.armor.equip_leather master @s ~ ~ ~ 0.8 1.3
