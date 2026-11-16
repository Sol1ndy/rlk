# @s = a dormant anchor, at it: grow (20 t), burst, sounds.
scoreboard players set @s riftS 5
scoreboard players set @s riftT 0
function rlk:room/rift/look/grow
particle minecraft:electric_spark ~ ~1.45 ~ 0.6 0.9 0.6 0.4 40
particle minecraft:end_rod ~ ~1.45 ~ 0.3 0.6 0.3 0.12 16
particle minecraft:flash{color:[0.875f,0.965f,1f,1f]} ~ ~1.45 ~ 0 0 0 0 1
playsound minecraft:entity.lightning_bolt.thunder block @a[tag=player] ~ ~ ~ 0.4 1.6 0.13
playsound minecraft:block.end_portal.spawn block @a[tag=player] ~ ~ ~ 0.5 1.3 0.17
