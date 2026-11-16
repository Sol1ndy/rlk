# Open (every 40 t): the hum, and half the time a crackle.
playsound minecraft:block.respawn_anchor.ambient block @a[tag=player] ~ ~ ~ 0.6 1 0.2
execute store result score #riftR room run random value 0..1
execute if score #riftR room matches 1 run playsound minecraft:entity.lightning_bolt.impact block @a[tag=player] ~ ~ ~ 0.15 1.9 0
