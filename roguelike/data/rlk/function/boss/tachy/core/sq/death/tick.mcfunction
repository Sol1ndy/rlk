# Stand-in death tick (#sq tk 1..130).
execute if score #sq tk matches 20 at @s run playsound minecraft:entity.iron_golem.damage hostile @a[tag=player] ~ ~ ~ 0.6 0.6 0.2
execute if score #sq tk matches 20 at @s run playsound minecraft:item.armor.equip_netherite hostile @a[tag=player] ~ ~ ~ 0.5 0.7 0.17
execute if score #sq tk matches 116 at @s run playsound minecraft:block.sand.break hostile @a[tag=player] ~ ~ ~ 0.7 0.7 0.23
execute if score #sq tk matches 116 at @s run playsound minecraft:entity.blaze.death hostile @a[tag=player] ~ ~ ~ 0.4 0.6 0.13
execute if score #sq tk matches 130.. run scoreboard players set #sqdone tk 1
