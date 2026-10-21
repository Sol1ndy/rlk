# Hook test {id:N} (as the player, /function rlk:mboss/test/pattern {id:N}; ap_contract 0.8). See test/help.
$scoreboard players set #apTst mb $(id)
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/apep/test/run
