# Back at the centre on the floor facing south (the CS white-out), the rig unparked; proxies inv (the revival
# clip hides the body until its burst; its px sets make it targetable).
scoreboard players set #apPark mb 0
scoreboard players set #mbNoLeash mb 0
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run tp @s 440 201 8 0 0
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:boss/apep/rig/unpark
function rlk:boss/apep/px/inv
