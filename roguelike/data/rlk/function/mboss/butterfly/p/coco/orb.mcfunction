# @s = an orb, at it (module tick). Age mbT: homing 1..39 (9 degrees/t), its pj life ends at 40
# (pj_end keeps it as a still prop), the burst hazard at 40 in its group (quiet), pulses, the burst at 50.
scoreboard players add @s mbT 1
execute if score @s mbT matches 1..39 run function rlk:mboss/pj/steer {max:9}
execute if entity @s[tag=rlk_mb_bf_p14o0] run function rlk:mboss/butterfly/p/coco/follow0
execute if entity @s[tag=rlk_mb_bf_p14o1] run function rlk:mboss/butterfly/p/coco/follow1
scoreboard players operation #bfM mb = @s mbT
scoreboard players operation #bfM mb %= #bfK2 mb
execute if score @s mbT matches ..40 if score #bfM mb matches 0 run particle minecraft:dust{color:[0.898f,0.984f,0.784f],scale:1} ~ ~ ~ 0.4 0.4 0.4 0 3 force @a[tag=player]
execute if score @s mbT matches ..40 if score #bfM mb matches 0 run particle minecraft:end_rod ~ ~ ~ 0.3 0.3 0.3 0.01 1 force @a[tag=player]
scoreboard players operation #bfM mb = @s mbT
scoreboard players operation #bfM mb %= #bfK10 mb
# every 10 t of flight: its hum (no shadow ring on the floor: the telegraph rule)
execute if score @s mbT matches ..39 if score #bfM mb matches 0 run function rlk:mboss/butterfly/fx/snd/orb_fly
execute if score @s mbT matches 40 rotated ~ 0 run function rlk:mboss/butterfly/p/coco/burst_tell
execute if score @s mbT matches 41 run data merge entity @s {start_interpolation:0,interpolation_duration:3,transformation:{scale:[1.95f,1.95f,1.95f]}}
execute if score @s mbT matches 44 run data merge entity @s {start_interpolation:0,interpolation_duration:3,transformation:{scale:[1.7f,1.7f,1.7f]}}
execute if score @s mbT matches 47 run data merge entity @s {start_interpolation:0,interpolation_duration:3,transformation:{scale:[1.95f,1.95f,1.95f]}}
execute if score @s mbT matches 50 run function rlk:mboss/butterfly/p/coco/burst
