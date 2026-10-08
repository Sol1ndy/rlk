# macro: id → #price tmp
scoreboard players set #price tmp 0
$data modify storage rlk:io rarity set from storage rlk:items registry.$(id).rarity
function rlk:ditem/sell_price2 with storage rlk:io
