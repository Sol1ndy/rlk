# Pattern 1 "강타" (@s = body, at @s; #prT = 1.. pattern clock).
execute if score #prT mb matches 1 run function rlk:mboss/mv/face
execute if score #prT mb matches 1 run function rlk:mboss/proto/pose/raise {d:8}
execute if score #prT mb matches 1 run scoreboard players set #hzSfx mb 1
execute if score #prT mb matches 1 run execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:35,tell:24,dmg:150}
execute if score #prT mb matches 1 run playsound minecraft:entity.ravager.roar hostile @a[tag=player] ~ ~ ~ 0.5 1.4 0.17
execute if score #prT mb matches 20 run function rlk:mboss/proto/pose/strike {d:4}
execute if score #prT mb matches 25 run particle minecraft:explosion ~ ~1 ~ 0.4 0.2 0.4 0 2 force @a[tag=player]
execute if score #prT mb matches 44 run function rlk:mboss/proto/finish
