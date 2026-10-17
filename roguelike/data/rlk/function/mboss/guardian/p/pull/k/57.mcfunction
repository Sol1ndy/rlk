# pull tick 57 (@s = body, at the body).
scoreboard players set #hzSfx mb 0
scoreboard players set #hzAct mb 3
scoreboard players set #hzVis mb 42
execute positioned ~ 201 ~ rotated as @s rotated ~ 0 run function rlk:mboss/hz/sector {r:55,a:180,tell:20,dmg:120}
