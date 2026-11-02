# D2 (@s = body, 12 t before the follow-up): it runs if the dash landed or the player is within 5 b;
# otherwise the cast ends here (the recovery follows).
execute if score #d2_l kn matches 1 run return 0
execute at @s if entity @e[tag=rlk_body,limit=1,distance=..5] run return 0
scoreboard players set #done kn 1
