$execute unless data storage rlk:pinv order[$(j)] run return 0
$data modify storage rlk:lvpick sw.from set from storage rlk:pinv order[$(j)]
$data modify storage rlk:lvpick sw.to set from storage rlk:lvpick choices[$(i)]
# 내려놓은 아이템은 돌아갈 때 떨군다
data modify storage rlk:lvpick dropq append from storage rlk:lvpick sw.from
function rlk:items/order_replace with storage rlk:lvpick sw
scoreboard players set @s invDirty 2
playsound minecraft:entity.player.levelup master @s ~ ~ ~ 0.5 1.6
playsound minecraft:block.anvil.use master @s ~ ~ ~ 0.3 1.6
function rlk:lvup/act/resolve
