# 2: a ring 2.5 .. 5 b around the body (tell 28 t).
execute if score #spT mb matches 1 at @s positioned ~ 201 ~ run function rlk:mboss/hz/ring {r0:25,r:50,tell:28,dmg:110}
execute if score #spT mb matches 1 at @s run playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 0.4 1.6 0.13
execute if score #spT mb matches 44.. run scoreboard players set #spPat mb 0
