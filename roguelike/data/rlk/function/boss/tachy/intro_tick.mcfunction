# Hook intro_tick (@s = body, #mbT 1..; rlk_mb_inv). The intro sequence (184 t clip, seq/intro or the stand-in)
# on the clock #sq tk; music phase 1 at 176, the push ring (no damage) at 178; the fight at the end.
execute if score #mbT mb matches 1 run function rlk:boss/tachy/core/intro/begin
execute unless score #mbT mb matches 1 run scoreboard players add #sq tk 1
execute unless score #mbT mb matches 1 run function rlk:boss/tachy/seq/intro/tick
execute if score #sq tk matches 176 run function rlk:mboss/music/set {ph:1}
execute if score #sq tk matches 178 at @s run function rlk:mboss/push/ring {r:40,to:45,kb:4}
execute if score #sqdone tk matches 1 run function rlk:boss/tachy/core/intro/done
execute if score #sq tk matches 186.. run function rlk:boss/tachy/core/intro/done
function rlk:boss/tachy/rig/tick
