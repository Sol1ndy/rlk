# W1 stage bl tick 24
function rlk:boss/tachy/p/w1/far
tag @s remove rlk_mb_inv
function rlk:boss/tachy/rig/state/normal
function rlk:boss/tachy/rig/play/blink_in
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.5 ~ run function rlk:boss/tachy/fx/p/blink_in
execute at @s run function rlk:boss/tachy/fx/snd/blink_in
