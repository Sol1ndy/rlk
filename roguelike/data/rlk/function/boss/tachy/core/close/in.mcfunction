# Back (@s = body): visible, vulnerable, the blink_in clip and burst, facing the player.
tag @s remove rlk_mb_inv
function rlk:boss/tachy/rig/state/normal
function rlk:mboss/mv/face
function rlk:boss/tachy/rig/play/blink_in
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.5 ~ run function rlk:boss/tachy/fx/p/blink_in
function rlk:boss/tachy/fx/snd/blink_in
