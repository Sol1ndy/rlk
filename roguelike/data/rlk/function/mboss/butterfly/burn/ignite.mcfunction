execute as @a[tag=player,limit=1] run function rlk:element/src_player
function rlk:element/calc {m:50}
scoreboard players operation @s burnDmg = #rdmg tmp
scoreboard players set @s burnI 0
scoreboard players set @s burnOn 1
scoreboard players set #rx tmp 10
scoreboard players set #lunRx tmp 0
function rlk:element/rx_text
