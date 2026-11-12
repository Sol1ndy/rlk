# Pattern 3 "휘두르기" (@s = body, at @s; #prT = 1.. pattern clock).
execute if score #prT mb matches 1 run function rlk:mboss/mv/face
execute if score #prT mb matches 1 run function rlk:mboss/proto/pose/sweep_wind {d:10}
execute if score #prT mb matches 1 run scoreboard players set #hzSfx mb 2
execute if score #prT mb matches 1 at @s rotated as @s rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/sector {r:55,a:75,tell:16,dmg:130}
execute if score #prT mb matches 15 run function rlk:mboss/proto/pose/sweep {d:3}
execute if score #prT mb matches 34 run function rlk:mboss/proto/finish
