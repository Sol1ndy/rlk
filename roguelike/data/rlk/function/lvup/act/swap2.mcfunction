$execute unless data storage rlk:pinv order[$(j)] run return 0
$data modify storage rlk:lvpick sw.from set from storage rlk:pinv order[$(j)]
$data modify storage rlk:lvpick sw.to set from storage rlk:lvpick choices[$(i)]
# 내려놓은 아이템은 돌아갈 때 떨군다
data modify storage rlk:lvpick dropq append from storage rlk:lvpick sw.from
function rlk:items/order_replace with storage rlk:lvpick sw
scoreboard players set @s invDirty 2
execute unless score #k2 snd matches 1 run function rlk:snd/f415
execute unless score #k350 snd matches 1 run function rlk:snd/f417
function rlk:lvup/act/resolve
