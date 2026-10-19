execute if score #mbPause mb matches 0 as @e[tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/d/pause
# chapter mode (AZ-CM): the pause edge halts the music (resume restarts the phase track) and drops proxy clicks
execute if score #mbPause mb matches 0 if score #mbMusPh mb matches 1.. run function rlk:mboss/music/halt
execute if score #mbPx mb matches 1 run function rlk:mboss/px/clear_input
scoreboard players set #mbPause mb 1
# No boss bars on the death screen (the run, or the test, is lost).
execute if entity @a[tag=player,scores={dead=1}] run function rlk:mboss/bars_hide
