# Hook spawn (@s = the arena marker at C of hr_field, rotated as it). The body (mboss/body: husk scale 1.0, click
# shield 1.2 x 2.4, miniboss economy, rlk_mb_inv in the intro) sits on her rock 884.0 201 5.0
# facing the moon, her back to the player arriving at start (PLAN §3.1). The event scores are cleared (PLAN §7.3.1).
# F2 round 1 (V2R-02): the boss bars off from her spawn on (fight_vars has just cleared #mbBarOff; with the
# framework's start_go show guarded by it, CS0 never shows a bar; core/intro/begin repeats it, intro/done ends it).
execute positioned 884.0 201 5.0 rotated 187.31 0 run function rlk:mboss/body
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:boss/scarlet/core/setup
function rlk:mboss/bars_off
scoreboard players set #hrEv hr 0
scoreboard players set #hrEvDone hr 0
scoreboard players set #hrEvDrop hr 0
