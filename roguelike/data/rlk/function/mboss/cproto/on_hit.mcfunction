# Hook on_hit (@s = body inside combat/apply; #mbPart = the proxy that was hit, 0 = the body directly): a short flash.
execute unless score #cpFlash mb matches 1.. run function rlk:mboss/cproto/rig/glow
scoreboard players set #cpFlash mb 3
scoreboard players operation #cpLastPart mb = #mbPart mb
