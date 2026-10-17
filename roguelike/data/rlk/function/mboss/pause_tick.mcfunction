execute if score #mbPause mb matches 0 as @e[tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/d/pause
scoreboard players set #mbPause mb 1
# No boss bars on the death screen (the run, or the test, is lost).
execute if entity @a[tag=player,scores={dead=1}] run function rlk:mboss/bars_hide
