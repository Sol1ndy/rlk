# The lanes again after a pause (@s = body): tell = the ticks left to the fire (1 while firing), hold to the off.
execute if score #fgPT mb matches 155.. run return 0
scoreboard players set #fgX mb 22
scoreboard players operation #fgX mb -= #fgPT mb
execute if score #fgX mb matches ..0 run scoreboard players set #fgX mb 1
execute store result storage rlk:mboss fg.ln.tell int 1 run scoreboard players get #fgX mb
scoreboard players set #fgM mb 155
scoreboard players operation #fgM mb -= #fgPT mb
scoreboard players operation #fgM mb -= #fgX mb
execute store result storage rlk:mboss fg.ln.hold int 1 run scoreboard players get #fgM mb
data modify storage rlk:mboss fg.ln merge value {len:58,w:6,back:-30,el:5}
data modify storage rlk:mboss fg.ln.id set value 0
function rlk:mboss/fieldgen/fx/tele/mline_end {id:0}
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p3e,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @s rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/fieldgen/fx/tele/mline with storage rlk:mboss fg.ln
data modify storage rlk:mboss fg.ln.id set value 1
function rlk:mboss/fieldgen/fx/tele/mline_end {id:1}
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p3g,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @s rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/fieldgen/fx/tele/mline with storage rlk:mboss fg.ln
