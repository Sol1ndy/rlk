# Hook spawn (@s = the arena marker at C of hr_field, rotated as it). The body (mboss/body: husk scale 1.35, click
# shield 1.2 x 2.9, miniboss economy, rlk_mb_inv in the intro) sits on her rock 884 201 5
# facing the moon, her back to the player arriving at start (PLAN §3.1). The event scores are cleared (PLAN §7.3.1).
execute positioned 884 201 5 rotated 187.31 0 run function rlk:mboss/body
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:boss/scarlet/core/setup
scoreboard players set #hrEv hr 0
scoreboard players set #hrEvDone hr 0
scoreboard players set #hrEvDrop hr 0
