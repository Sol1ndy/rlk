# Hook test {id:N} (as the player, from /function rlk:mboss/test/pattern): 1..7 = run that pattern next
# (the running one is cut), 90 = spawn a breakable star.
$scoreboard players set #prReq mb $(id)
execute if score #prReq mb matches 90 as @e[tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/proto/star
execute if score #prReq mb matches 90 run return run scoreboard players set #prReq mb 0
execute unless score #prReq mb matches 1..7 run return run scoreboard players set #prReq mb 0
execute if score #mbSt mb matches 0 run function rlk:mboss/intro_end
execute if score #prPat mb matches 1.. run function rlk:mboss/lib_clear
execute if score #prPat mb matches 1.. as @e[tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/proto/finish
scoreboard players set #prCool mb 1
