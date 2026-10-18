# burst clock 3
scoreboard players set #hzKB mb 4
scoreboard players set #hzSfx mb 0
scoreboard players set #hzVis mb 51
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzY1 mb 5
execute at @s positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:120,tell:45,dmg:220}
execute at @s positioned ~ 201 ~ rotated ~ 0 run function rlk:mboss/fieldgen/fx/tele/disc {r:120,tell:45,el:5,hold:3}
execute at @s positioned ~ 201 ~ rotated ~ 0 run playsound minecraft:block.trial_spawner.about_to_spawn_item hostile @a[tag=player] ~ ~ ~ 0.6 0.7 0.2
