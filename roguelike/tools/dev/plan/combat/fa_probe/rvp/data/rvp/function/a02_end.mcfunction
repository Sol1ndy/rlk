data modify storage rvp:log a02 set value {}
execute store result storage rvp:log a02.rcT_max int 1 run scoreboard players get #H_rcTmax rvp
execute store result storage rvp:log a02.fail_sound_ticks int 1 run scoreboard players get #H_fail rvp
execute store result storage rvp:log a02.dodges int 1 run scoreboard players get #H_dg rvp
scoreboard players set #mode rvp 0
kill @s
