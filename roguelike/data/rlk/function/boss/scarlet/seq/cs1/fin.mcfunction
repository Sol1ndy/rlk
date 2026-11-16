# CS1 (hr_design §3.2): the clash, pushed apart, the hat and the bottle, the petal, 홍련일섬, the crimson field; locked 0-720, skippable 40-560 -> 566.
# The first tick without the lock (the framework releases the player in this tick): the stands, the actor and the
# stage go.
function rlk:mboss/cam/kill
function rlk:char/cine/stop
kill @e[type=minecraft:marker,tag=rlk_hr_stage]
kill @e[type=minecraft:marker,tag=rlk_hr_stage2]
scoreboard players set #sq_h hr 0
scoreboard players set #mbNoLeash mb 0
