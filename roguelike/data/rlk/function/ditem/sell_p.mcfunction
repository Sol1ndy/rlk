# @s = 판매하는 플레이어
scoreboard players set #retok tmp 1
function rlk:ditem/sell_price with storage rlk:dtmp
scoreboard players operation @s gold += #price tmp
function rlk:ditem/kill_group with storage rlk:dtmp
execute store result storage rlk:sell amt int 1 run scoreboard players get #price tmp
title @s times 5 40 10
scoreboard players set @s ttlT 55
function rlk:ditem/sell_msg with storage rlk:sell
title @s title {"text":""}
playsound minecraft:block.chain.place master @s ~ ~ ~ 1.0 1.7
playsound minecraft:block.chain.break master @s ~ ~ ~ 0.8 2.0
playsound minecraft:block.chain.hit master @s ~ ~ ~ 0.8 1.4
playsound minecraft:block.amethyst_block.chime master @s ~ ~ ~ 0.7 1.5
