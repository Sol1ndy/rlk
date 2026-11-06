# From rlk:load (after mboss/init): the rift objectives, the run defaults, #riftOn re-derived from the world
# (/reload keeps every rift entity); a rift caught collapsing finishes now (its boxes fall), one caught
# growing is open, a queued show stays queued.
scoreboard objectives add riftS dummy
scoreboard objectives add riftT dummy
scoreboard objectives add riftCd dummy
scoreboard objectives add riftDw dummy
scoreboard objectives add riftPk dummy
scoreboard objectives add riftA dummy
scoreboard objectives add riftX dummy
scoreboard objectives add riftY dummy
scoreboard objectives add riftZ dummy
execute unless score #riftUsed room matches 0.. run scoreboard players set #riftUsed room 0
execute unless score #riftForce room matches 0.. run scoreboard players set #riftForce room 0
scoreboard players set #riftC2 room 2
scoreboard players set #riftC4 room 4
scoreboard players set #riftC8 room 8
scoreboard players set #riftC40 room 40
scoreboard players set #riftC10 room 10
execute as @e[type=minecraft:marker,tag=rlk_rift,scores={riftS=4}] at @s run function rlk:room/rift/close_end
execute as @e[type=minecraft:marker,tag=rlk_rift,scores={riftS=5}] at @s run function rlk:room/rift/open_now
scoreboard players set #riftOn room 0
execute if entity @e[type=minecraft:marker,tag=rlk_rift,limit=1] run scoreboard players set #riftOn room 1
execute if entity @e[type=minecraft:marker,tag=rlk_riftq,limit=1] run scoreboard players set #riftOn room 1
