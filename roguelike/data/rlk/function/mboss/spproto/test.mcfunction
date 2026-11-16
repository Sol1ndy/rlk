# Hook test {id:N} (as the player, from /function rlk:mboss/test/pattern).
$scoreboard players set #spReq mb $(id)
execute if score #spReq mb matches 1 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run scoreboard players set #spPat mb 1
execute if score #spReq mb matches 1 run scoreboard players set #spT mb 0
execute if score #spReq mb matches 2 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run scoreboard players set #spPat mb 2
execute if score #spReq mb matches 2 run scoreboard players set #spT mb 0
execute if score #spReq mb matches 3 run function rlk:mboss/music/set {ph:0}
execute if score #spReq mb matches 4 run function rlk:mboss/music/set {ph:1}
scoreboard players set #spReq mb 0
