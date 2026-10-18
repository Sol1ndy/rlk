# @s = an orb, at it: homing for 40 t (9 deg/t), then it slows over the burst decal locked under it.
scoreboard players add @s mbT 1
execute if score @s mbT matches 1..40 run function rlk:mboss/pj/steer {max:9}
execute if score @s mbT matches 40 run function rlk:mboss/butterfly/p/coco/burst_tell
scoreboard players operation #bfM mb = @s mbT
scoreboard players operation #bfM mb %= #bfK3 mb
execute if score #bfM mb matches 0 run particle minecraft:dust{color:[0.898f,0.984f,0.784f],scale:1} ~ ~ ~ 0.4 0.4 0.4 0 3 force @a[tag=player]
