# A9 dash (@s = the body, tick 26): through the locked spot to 3 b beyond it, at most 12 b, probed
# in 0.5 b steps (mv/ok; p/a9/pstep); the start marker and the probed length feed the dash line at tick 27.
kill @e[type=minecraft:marker,tag=rlk_hr_a9s]
execute at @s positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a9","rlk_hr_a9s"]}
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] feet run tp @e[type=minecraft:marker,tag=rlk_hr_a9s,limit=1] ~ ~ ~ ~ 0
scoreboard players set #t hr 24
scoreboard players set #t2 hr 0
kill @e[type=minecraft:marker,tag=rlk_hr_dp]
execute at @s positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_dp"]}
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] feet as @e[type=minecraft:marker,tag=rlk_hr_dp,limit=1] run tp @s ~ ~ ~ ~ 0
execute as @e[type=minecraft:marker,tag=rlk_hr_dp,limit=1] at @s run function rlk:boss/scarlet/p/a9/pstep
scoreboard players operation #a9_n hr = #t2 hr
kill @e[type=minecraft:marker,tag=rlk_hr_dp]
data modify storage rlk:hr core.dash set value {len:0,w:24,tell:1,dmg:54}
execute store result storage rlk:hr core.dash.len int 5 run scoreboard players get #a9_n hr
execute at @s positioned ~ 201 ~ unless entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1,distance=..2.3] at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] facing entity @s feet rotated ~ 0 positioned ^ ^ ^2 if function rlk:mboss/mv/ok if function rlk:boss/scarlet/core/cam_ok run return run function rlk:boss/scarlet/p/a9/go {t:2}
execute at @s positioned ~ 201 ~ unless entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1,distance=..3.8] at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] facing entity @s feet rotated ~ 0 positioned ^ ^ ^3.5 if function rlk:mboss/mv/ok if function rlk:boss/scarlet/core/cam_ok run function rlk:boss/scarlet/p/a9/go {t:2}
