# Pattern 2 "찌르기" (@s = body, at @s; #prT = 1.. pattern clock).
execute if score #prT mb matches 1 run function rlk:mboss/mv/face
execute if score #prT mb matches 1 run function rlk:mboss/proto/pose/thrust_wind {d:10}
execute if score #prT mb matches 1 run scoreboard players set #hzKB mb 4
execute if score #prT mb matches 1 run scoreboard players set #hzSfx mb 3
execute if score #prT mb matches 1 at @s rotated as @s rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/line {len:120,w:22,tell:18,dmg:120}
execute if score #prT mb matches 16 run function rlk:mboss/proto/pose/thrust {d:3}
execute if score #prT mb matches 16..20 run function rlk:mboss/mv/step {d:0.8}
execute if score #prT mb matches 38 run function rlk:mboss/proto/finish
