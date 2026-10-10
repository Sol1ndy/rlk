# @s = 판매하는 플레이어
scoreboard players set #retok tmp 1
function rlk:ditem/sell_price with storage rlk:dtmp
scoreboard players operation @s gold += #price tmp
function rlk:ditem/kill_group with storage rlk:dtmp
execute store result storage rlk:sell amt int 1 run scoreboard players get #price tmp
title @s times 5 40 10
scoreboard players set @s ttlT 55
function rlk:ditem/sell_msg with storage rlk:sell
function rlk:view/ttl_blank
execute unless score #k110 snd matches 1 run function rlk:snd/f117
execute unless score #k111 snd matches 1 run function rlk:snd/f118
execute unless score #k112 snd matches 1 run function rlk:snd/f119
execute unless score #k113 snd matches 1 run function rlk:snd/f120
