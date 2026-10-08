execute if score #pcN tmp matches ..0 run return 0
execute store result storage rlk:chars p.y float 1 run random value -179..180
execute store result storage rlk:chars p.x float 1 run random value -70..10
data modify storage rlk:chars p.color set from storage rlk:hud encol
function rlk:char/particle_spawn with storage rlk:chars p
scoreboard players remove #pcN tmp 1
function rlk:char/particle_loop
