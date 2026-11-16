# Hook test {id:N} (as the player, /function rlk:boss/test/pattern {id:N}); the list: test/help.
$scoreboard players set #tst tk $(id)
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:boss/tachy/test/run
