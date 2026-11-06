# 1: a 3 b electro disc at the player (tell 24 t).
execute if score #spT mb matches 1 run scoreboard players set #hzEl mb 3
execute if score #spT mb matches 1 at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:30,tell:24,dmg:100}
execute if score #spT mb matches 1 at @s run playsound minecraft:block.respawn_anchor.charge hostile @a[tag=player] ~ ~ ~ 0.6 1.4 0.2
execute if score #spT mb matches 40.. run scoreboard players set #spPat mb 0
