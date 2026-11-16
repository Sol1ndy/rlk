scoreboard players add #apMvT mb 1
function rlk:boss/apep/p/move/fx
execute if score #apMvK mb matches 1 run return run function rlk:boss/apep/mv/crawl
execute if score #apMvK mb matches 2 run return run function rlk:boss/apep/mv/walk
execute if score #apMvK mb matches 3 if score #apMvT mb matches 10.. run return run function rlk:boss/apep/p/end
execute if score #apMvK mb matches 4 if score #apMvT mb matches 10 run function rlk:boss/apep/mv/step
execute if score #apMvK mb matches 4 if score #apMvT mb matches 20.. run return run function rlk:boss/apep/p/end
