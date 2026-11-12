# CS0 intro (hr_design §3.1): 20 shots, lines 1-11; seated with the cup and the bottle, the walk, the leap; intro_end: line 11, the draw, the stance.
# The first tick without the lock (the framework releases the player in this tick): the stands, the actor and the
# stage go.
function rlk:mboss/cam/kill
function rlk:char/cine/stop
kill @e[type=minecraft:marker,tag=rlk_hr_stage]
kill @e[type=minecraft:marker,tag=rlk_hr_stage2]
scoreboard players set #sq_h hr 0
