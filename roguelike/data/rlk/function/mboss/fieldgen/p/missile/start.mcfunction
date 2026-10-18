# C4 바위 폭탄 (clip missiles; @s = body): launches [21, 22, 24, 25, 27, 28, 30, 31, 33, 34], lock +14 (tell 14), impact +28 = 49..62; 2 volley groups.
scoreboard players set #fq4Pz mb 0
function rlk:mboss/fieldgen/rig_stub/face/track
execute at @s rotated as @s rotated ~ 0 positioned ^5.33 ^4.55 ^0 run function rlk:mboss/fieldgen/fx/p/tip_flare
execute at @s rotated as @s rotated ~ 0 positioned ^-5.33 ^4.55 ^0 run function rlk:mboss/fieldgen/fx/p/tip_flare
execute at @s rotated as @s rotated ~ 0 positioned ^5.33 ^4.55 ^0 run function rlk:mboss/fieldgen/fx/snd/tip_flare
