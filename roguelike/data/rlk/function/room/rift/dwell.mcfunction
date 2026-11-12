# @s = an open anchor, at it: the player body within 1.0 b horizontal and |dy| < 1.5 b for 10 consecutive ticks while
# no combat, alive, outside the selection space and the map screen -> room/rift/enter.
execute unless score #combat room matches 0 run return run scoreboard players set @s riftDw 0
execute if score @s riftCd matches 1.. run return run scoreboard players set @s riftDw 0
execute unless entity @e[tag=rlk_body,distance=..1.81,limit=1] run return run scoreboard players set @s riftDw 0
execute if entity @a[tag=player,scores={dead=1}] run return run scoreboard players set @s riftDw 0
execute if entity @a[tag=player,scores={pkMode=1..}] run return run scoreboard players set @s riftDw 0
execute if entity @a[tag=player,scores={vMap=1}] run return run scoreboard players set @s riftDw 0
execute unless function rlk:room/rift/near run return run scoreboard players set @s riftDw 0
scoreboard players add @s riftDw 1
execute at @e[tag=rlk_body,limit=1] run particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.5 0.3 0.4 4
execute if score @s riftDw matches 1 run playsound minecraft:block.portal.ambient block @a[tag=player] ~ ~ ~ 0.3 1.8 0.1
execute if score @s riftDw matches 10.. run function rlk:room/rift/enter
