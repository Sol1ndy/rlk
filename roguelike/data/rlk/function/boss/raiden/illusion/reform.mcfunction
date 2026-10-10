# As the boss at its (new) feet: face the player and play the arrival art. The rig
# stays hidden (rdPat 5) until the art has formed, then finish/stagger shows it.
tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute rotated as @s run tp @s ~ ~ ~ ~ 0
function rlk:boss/raiden/movement/arrive
