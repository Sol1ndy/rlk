# Hook on_hit (@s = body inside combat/apply; #elem #elU #rx #tfm #dmg known). Flags only: start a short flash.
execute unless score #prFlash mb matches 1.. run function rlk:mboss/proto/rig/glow
scoreboard players set #prFlash mb 3
