# Spawn failed (no registry entry, no body after the spawn hook): retry twice, then cancel without reward.
function rlk:mboss/cleanup_aux
scoreboard players add #mbFail mb 1
execute if score #mbFail mb matches ..2 run return run scoreboard players set #spawnT room 10
function rlk:mboss/start_cancel
