# Pattern 5 "투창" (@s = body, at @s; #prT = 1.. pattern clock).
execute if score #prT mb matches 1 run function rlk:mboss/mv/face
execute if score #prT mb matches 1 run function rlk:mboss/proto/pose/raise {d:10}
execute if score #prT mb matches 1 run scoreboard players set #hzSfx mb 3
execute if score #prT mb matches 1 run scoreboard players set #hzY1 mb 22
execute if score #prT mb matches 1 at @s rotated as @s rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/line {len:300,w:14,tell:18,dmg:130}
execute if score #prT mb matches 17 run function rlk:mboss/proto/pose/strike {d:3}
execute if score #prT mb matches 17 run function rlk:mboss/proto/javelin
execute if score #prT mb matches 42 run function rlk:mboss/proto/finish
