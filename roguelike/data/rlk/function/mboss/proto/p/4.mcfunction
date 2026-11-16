# Pattern 4 "파문" (@s = body, at @s; #prT = 1.. pattern clock).
execute if score #prT mb matches 1 run function rlk:mboss/proto/pose/both_up {d:10}
execute if score #prT mb matches 1 run scoreboard players set #hzSfx mb 4
execute if score #prT mb matches 1 run execute positioned ~ 201 ~ run function rlk:mboss/hz/ring {r0:35,r:95,tell:22,dmg:110}
execute if score #prT mb matches 1 run playsound minecraft:block.respawn_anchor.charge hostile @a[tag=player] ~ ~ ~ 0.7 0.7 0.23
execute if score #prT mb matches 20 run function rlk:mboss/proto/pose/both_down {d:3}
execute if score #prT mb matches 40 run function rlk:mboss/proto/finish
