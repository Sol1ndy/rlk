# {s}: the cut of strike s on the player again (its marker to the player's floor spot, yaw her -> the player; the
# framework's hz/aim recomputes its axis: this tick's hit test uses it). Until the lock (strike - LOCK_LEAD).
$execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ facing entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] feet rotated ~180 0 as @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=$(s)}] run function rlk:mboss/hz/aim
