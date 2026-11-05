# A decoration bolt here (@s any; the floor spot 3-6 b from the player): no hit box (PLAN §4.5, questions.md Q-A12).
execute positioned ~ ~ ~ run particle minecraft:dust{color:[1.0,0.88,0.29],scale:1.6} ~ ~ ~ 0.05 1.6 0.05 0 14 force @a[tag=player]
execute positioned ~ ~ ~ run particle minecraft:electric_spark ~ ~ ~ 0.1 1.2 0.1 0.05 6 force @a[tag=player]
execute positioned ~ ~ ~ run playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 0.15 1.9 0
