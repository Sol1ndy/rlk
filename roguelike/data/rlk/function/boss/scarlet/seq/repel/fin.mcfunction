# repel {at:60|5} (hr_design §3.4): the deflect, the blade lock, the grab, the hilt on her hat, two cuts, back to back, the throw, the kick; HP steps at 49 / 101 / 129; locked 0-140, the bars on.
# The first tick without the lock (the framework releases the player in this tick): the stands, the actor and the
# stage go.
function rlk:mboss/cam/kill
kill @e[type=minecraft:marker,tag=rlk_hr_stage]
kill @e[type=minecraft:marker,tag=rlk_hr_stage2]
scoreboard players set #mbNoLeash mb 0
