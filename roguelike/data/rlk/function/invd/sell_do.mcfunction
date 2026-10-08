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
title @s title {"text":""}
playsound minecraft:block.chain.place master @s ~ ~ ~ 1.0 1.7
playsound minecraft:block.chain.break master @s ~ ~ ~ 0.8 2.0
playsound minecraft:block.chain.hit master @s ~ ~ ~ 0.8 1.4
playsound minecraft:block.amethyst_block.chime master @s ~ ~ ~ 0.7 1.5
