# repel {at:60|5} (hr_design §3.4): the deflect, the blade lock, the grab, the hilt on her hat, two cuts, back to back, the throw, the kick; HP steps at 49 / 101 / 129; locked 0-140, the bars on.
# The lock of this tick (@s = the body; #sq 0..139 while #sq_cx is not 1): the request the framework holds the
# player on (#mbCam mb 1, cleared by mboss/main every tick), the actor on the sequence clock, the camera lines.
# #sq_h = this run has seen the player held. Released after that (a pause, /reload, a relog, a killed stand), or
# never held by tick 3 (the framework holds in the tick of the first request made inside mboss/main, one tick
# later for a start outside it: a kill by a hit) -> no lock for the rest of the run (unlock). Never in the developer
# mode: its player is the body and is never held.
execute if entity @a[tag=player,tag=rlk_mb_camh] run scoreboard players set #sq_h hr 1
execute if score #sq_h hr matches 1 unless entity @a[tag=player,tag=rlk_mb_camh] unless entity @a[tag=player,tag=rlk_body] run return run function rlk:boss/scarlet/seq/repel/unlock
execute if score #sq hr matches 3.. unless score #sq_h hr matches 1 unless entity @a[tag=player,tag=rlk_body] run return run function rlk:boss/scarlet/seq/repel/unlock
scoreboard players set #mbCam mb 1
scoreboard players operation #cavT cine = #sq hr
execute as @a[tag=player,limit=1] run function rlk:char/cine/tick
function rlk:boss/scarlet/seq/repel/cam
