# t189: every dome pops (the models' pop clip, the rims end, the pop sound); the safe markers go. The kit's
# flash + shards per dome at t189 / 190 / 191 (one dome a tick: the per-tick command budget).
function rlk:boss/apep/om/dome/play {i:0,clip:"dome_pop"}
function rlk:boss/apep/om/dome/play {i:1,clip:"dome_pop"}
function rlk:boss/apep/om/dome/play {i:2,clip:"dome_pop"}
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_dome,limit=1] at @s run function rlk:boss/apep/fx/snd/q2_pop
function rlk:boss/apep/fx/tele/safe_end {id:0}
function rlk:boss/apep/fx/tele/safe_end {id:1}
function rlk:boss/apep/fx/tele/safe_end {id:2}
kill @e[type=minecraft:marker,tag=rlk_mb_ap_dome]
