# Core service 10: the move kind #apMvK (1 crawl 2 walk 3 step 4 turn180).
scoreboard players set #apMvT mb 0
execute if score #apMvK mb matches 1 run function rlk:boss/apep/play/crawl_p1
execute if score #apMvK mb matches 2 run function rlk:boss/apep/play/walk_p1
execute if score #apMvK mb matches 3..4 run function rlk:boss/apep/mv/step
