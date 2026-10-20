# @s = body: the run ends (disc gone, skid, charge_stop); the pattern ends 21 t later
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p9run] at @s rotated as @s run function rlk:mboss/hz/expire
scoreboard players set #aq9R mb -1
scoreboard players operation #aq9X mb = #azPT mb
scoreboard players add #aq9X mb 21
scoreboard players operation #azPLen mb = #aq9X mb
function rlk:mboss/azhdaha/rig/play/charge_stop
function rlk:mboss/azhdaha/fx/snd/charge_skid
function rlk:mboss/azhdaha/fx/p/skid
function rlk:mboss/azhdaha/p/release
