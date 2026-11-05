# R2 pattern tick 28.
execute if score #r2_two hr matches 1 run function rlk:mboss/mv/face
execute if score #r2_two hr matches 1 run function rlk:boss/scarlet/g/disc/throw {kb:0}
execute if score #r2_two hr matches 1 at @s run playsound minecraft:item.trident.riptide_2 hostile @a[tag=player] ~ ~ ~ 0.6 1.7 0.2
execute if score #r2_two hr matches 1 at @s run playsound minecraft:entity.breeze.shoot hostile @a[tag=player] ~ ~ ~ 0.5 1 0.17
execute if score #r2_two hr matches 1 at @s run playsound minecraft:item.trident.throw hostile @a[tag=player] ~ ~ ~ 0.3 1 0.1
execute unless score #r2_two hr matches 1 run function rlk:mboss/mv/face
execute unless score #r2_two hr matches 1 run function rlk:boss/scarlet/g/disc/throw {kb:2}
execute unless score #r2_two hr matches 1 at @s run playsound minecraft:item.trident.riptide_2 hostile @a[tag=player] ~ ~ ~ 0.6 1.7 0.2
execute unless score #r2_two hr matches 1 at @s run playsound minecraft:entity.breeze.shoot hostile @a[tag=player] ~ ~ ~ 0.5 1 0.17
execute unless score #r2_two hr matches 1 at @s run playsound minecraft:item.trident.throw hostile @a[tag=player] ~ ~ ~ 0.3 1 0.1
