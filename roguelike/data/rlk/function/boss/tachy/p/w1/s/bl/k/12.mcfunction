# W1 stage bl tick 12
function rlk:boss/tachy/rig/play/blink_out
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.5 ~ run function rlk:boss/tachy/fx/p/blink_out
execute at @s run function rlk:boss/tachy/fx/snd/blink_out
