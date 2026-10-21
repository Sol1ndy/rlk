# AP-P1 (plan 8.1 E): @s = body, #apPT = 0..109 (entrance_p1). The pool and the rise 0-31, the touch 47, the
# bulb flash 60, the embers 63-80, the Heart drawn up 70, the roar 100;
# the title at t30.
execute if score #apPT mb matches 0 run execute at @s positioned ~ 201 ~ run function rlk:boss/apep/fx/p/burrow_pool {r:35}
execute if score #apPT mb matches 0 run execute at @s positioned ~ 201 ~ run function rlk:boss/apep/fx/p/leaf_flakes
execute if score #apPT mb matches 0 run execute at @s positioned ~ 201 ~ run function rlk:boss/apep/fx/snd/e_emerge
execute if score #apPT mb matches 16 run execute at @s positioned ~ 201 ~ run function rlk:boss/apep/fx/p/leaf_flakes
execute if score #apPT mb matches 30 run function rlk:boss/apep/svc/title_p1
execute if score #apPT mb matches 60 run execute at @s rotated as @s rotated ~ 0 positioned ^-0.21 ^9.46 ^1.55 run function rlk:boss/apep/fx/p/bulb_flash
execute if score #apPT mb matches 60 run execute at @s rotated as @s rotated ~ 0 positioned ^-0.21 ^9.46 ^1.55 run function rlk:boss/apep/fx/snd/e_flash
execute if score #apPT mb matches 63 run execute at @s rotated as @s rotated ~ 0 positioned ^-0.21 ^9.46 ^1.55 run function rlk:boss/apep/fx/p/gold_embers
execute if score #apPT mb matches 67 run execute at @s rotated as @s rotated ~ 0 positioned ^-0.21 ^9.46 ^1.55 run function rlk:boss/apep/fx/p/gold_embers
execute if score #apPT mb matches 71 run execute at @s rotated as @s rotated ~ 0 positioned ^-0.21 ^9.46 ^1.55 run function rlk:boss/apep/fx/p/gold_embers
execute if score #apPT mb matches 75 run execute at @s rotated as @s rotated ~ 0 positioned ^-0.21 ^9.46 ^1.55 run function rlk:boss/apep/fx/p/gold_embers
execute if score #apPT mb matches 79 run execute at @s rotated as @s rotated ~ 0 positioned ^-0.21 ^9.46 ^1.55 run function rlk:boss/apep/fx/p/gold_embers
execute if score #apPT mb matches 70 run function rlk:boss/apep/heart/p1_up
execute if score #apPT mb matches 70 run execute at @s rotated as @s rotated ~ 0 positioned ^-0.21 ^9.46 ^1.55 run function rlk:boss/apep/fx/snd/e_heart_up
execute if score #apPT mb matches 100 run execute at @s run function rlk:boss/apep/fx/snd/e_roar
