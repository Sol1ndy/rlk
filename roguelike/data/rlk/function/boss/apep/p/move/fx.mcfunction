# Service 10 (core) step sounds (plan 8.1 M; @s = body, #apMvT = 1.. the move clock, #apMvK 1 crawl 2 walk 3-4
# crab-turn steps): crawl_p1 steps every 8 t to t40, the plant of crawl_stop_p1 at t49; walk_p1 steps every
# 9 t; turn_p1_step steps every 5 t.
scoreboard players operation #apM mb = #apMvT mb
scoreboard players operation #apM mb %= #apK8 mb
execute if score #apM mb matches 0 run execute if score #apMvK mb matches 1 if score #apMvT mb matches ..40 run function rlk:boss/apep/fx/snd/m_crawl
execute if score #apMvK mb matches 1 if score #apMvT mb matches 49 run function rlk:boss/apep/fx/snd/p1_land
execute if score #apMvK mb matches 2 if score #apMvT mb matches 9 run function rlk:boss/apep/fx/snd/m_walk
execute if score #apMvK mb matches 2 if score #apMvT mb matches 18 run function rlk:boss/apep/fx/snd/m_walk
execute if score #apMvK mb matches 2 if score #apMvT mb matches 27 run function rlk:boss/apep/fx/snd/m_walk
execute if score #apMvK mb matches 2 if score #apMvT mb matches 36 run function rlk:boss/apep/fx/snd/m_walk
scoreboard players operation #apM mb = #apMvT mb
scoreboard players operation #apM mb %= #apK5 mb
execute if score #apM mb matches 0 run execute if score #apMvK mb matches 3.. run function rlk:boss/apep/fx/snd/m_walk
