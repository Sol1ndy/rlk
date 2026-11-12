# Crab crawl toward the player at 0.25 b/t (inside the glide disc) until the near band or 40 t, then
# crawl_stop_p1 (32 t).
execute if score #apMvT mb matches ..40 run function rlk:mboss/mv/turn {max:4}
execute if score #apMvT mb matches ..40 run execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.25 run function rlk:boss/apep/u/step_here
execute if score #apMvT mb matches ..39 if entity @e[tag=rlk_body,distance=..7.5,limit=1] run scoreboard players set #apMvT mb 41
execute if score #apMvT mb matches 41 run function rlk:boss/apep/play/crawl_stop_p1
execute if score #apMvT mb matches 73.. run function rlk:boss/apep/p/end
