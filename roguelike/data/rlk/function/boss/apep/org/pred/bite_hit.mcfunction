# A bite: the 1.5 b lunge along the locked aim, the white-yellow bite flash, the bite sound.
execute rotated as @s rotated ~ 0 run function rlk:mboss/mv/step_flat {spd:1.5}
function rlk:boss/apep/org/basic/push_in
execute at @s rotated as @s rotated ~ 0 positioned ^ ^1.0 ^1.2 run function rlk:boss/apep/fx/p/bite_flash
execute at @s run function rlk:boss/apep/fx/snd/o6_bite
