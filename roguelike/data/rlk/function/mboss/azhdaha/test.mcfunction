# Hook test {id:N} (as the player, /function rlk:mboss/test/pattern {id:N}). See test/help.
$scoreboard players set #azTst mb $(id)
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/azhdaha/test/run
