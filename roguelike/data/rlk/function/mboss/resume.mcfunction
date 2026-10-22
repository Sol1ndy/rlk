scoreboard players set #mbPause mb 0
execute if score #mbMusPh mb matches 1.. store result storage rlk:mboss a.ph int 1 run scoreboard players get #mbMusPh mb
execute if score #mbMusPh mb matches 1.. run function rlk:mboss/music/set with storage rlk:mboss a
execute as @e[tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/d/resume
