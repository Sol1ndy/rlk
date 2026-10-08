# @s = 판매 버튼, at @s
scoreboard players operation #dg tmp = @s dgid
execute store result storage rlk:dtmp key int 1 run scoreboard players get #dg tmp
execute store result storage rlk:dtmp dg int 1 run scoreboard players get #dg tmp
execute at @s as @a[tag=player,limit=1] run function rlk:ditem/sell_p
