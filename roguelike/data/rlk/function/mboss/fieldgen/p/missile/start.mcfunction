# C4 바위 폭탄 (clip missiles; @s = body): launches [23, 25, 26, 28, 29, 31, 32, 34, 35, 37], lock +14 (tell 14), impact +28 = 51..65; 2 volley groups.
function rlk:mboss/fieldgen/rig/face/track
execute at @s rotated as @s rotated ~ 0 positioned ^5.332 ^4.55 ^0 run function rlk:mboss/fieldgen/fx/p/tip_flare
execute at @s rotated as @s rotated ~ 0 positioned ^-5.332 ^4.55 ^0 run function rlk:mboss/fieldgen/fx/p/tip_flare
execute at @s rotated as @s rotated ~ 0 positioned ^5.332 ^4.55 ^0 run function rlk:mboss/fieldgen/fx/snd/tip_flare
