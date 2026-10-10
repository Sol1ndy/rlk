# macro: i = 보유 목록의 순번. 목록에서 빼고 실물을 다시 놓은 뒤 골드를 준다
scoreboard players set @s pkConf 0
scoreboard players set @s pkSel -1
scoreboard players set @s pkRedraw 1
$execute unless data storage rlk:pinv order[$(i)] run return 0
$data modify storage rlk:io id set from storage rlk:pinv order[$(i)]
function rlk:invd/price with storage rlk:io
$data remove storage rlk:pinv order[$(i)]
function rlk:player/inv/place_items
scoreboard players set @s invDirty 2
scoreboard players operation @s gold += #price tmp
execute store result storage rlk:sell amt int 1 run scoreboard players get #price tmp
title @s times 5 40 10
scoreboard players set @s ttlT 55
function rlk:ditem/sell_msg with storage rlk:sell
function rlk:view/ttl_blank
execute unless score #k110 snd matches 1 run function rlk:snd/f117
execute unless score #k111 snd matches 1 run function rlk:snd/f118
execute unless score #k112 snd matches 1 run function rlk:snd/f119
execute unless score #k113 snd matches 1 run function rlk:snd/f120
