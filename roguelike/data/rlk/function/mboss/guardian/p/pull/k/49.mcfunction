# pull tick 49 (@s = body, at the body).
scoreboard players set #hzSfx mb 0
scoreboard players set #hzAct mb 3
scoreboard players set #hzQuiet mb 1
execute positioned ~ 201 ~ rotated as @s rotated ~ 0 run function rlk:mboss/hz/sector {r:68,a:180,tell:15,dmg:120}
playsound minecraft:item.trident.riptide_1 hostile @a[tag=player] ~ ~ ~ 0.4 1.4 0.13
playsound minecraft:entity.player.attack.knockback hostile @a[tag=player] ~ ~ ~ 0.6 0.6 0.2
