# Hook on_hit (@s = body inside combat/apply): a short flash.
execute unless score #spFlash mb matches 1.. run function rlk:mboss/spproto/rig/glow
scoreboard players set #spFlash mb 3
