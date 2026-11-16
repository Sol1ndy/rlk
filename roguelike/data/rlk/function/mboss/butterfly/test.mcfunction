# Hook test {id:N} (as the player, /function rlk:mboss/test/pattern {id:N}). See test/help.
$scoreboard players set #bfTst mb $(id)
execute if score #mbSt mb matches 0 run function rlk:mboss/intro_end
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/butterfly/test/run
