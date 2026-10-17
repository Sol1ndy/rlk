# Hit frame: bright outline + fill, sound, module visual event 1.
execute unless entity @s[tag=rlk_mb_hzq] run function rlk:mboss/hz/flash
execute if score @s mbHzS matches 1 run playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.55 1.5 0.3
execute if score @s mbHzS matches 1 run playsound minecraft:block.anvil.land hostile @a[tag=player] ~ ~ ~ 0.3 0.6 0.3
execute if score @s mbHzS matches 2 run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1 0.7 0.3
execute if score @s mbHzS matches 3 run playsound minecraft:item.trident.throw hostile @a[tag=player] ~ ~ ~ 1 0.8 0.3
execute if score @s mbHzS matches 4 run playsound minecraft:entity.iron_golem.attack hostile @a[tag=player] ~ ~ ~ 1 0.6 0.3
execute if score @s mbHzS matches 4 run playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.7 0.8 0.3
execute if score @s mbHzV matches 1.. run scoreboard players set #hzEv mb 1
execute if score @s mbHzV matches 1.. run function rlk:mboss/d/hz_vis
