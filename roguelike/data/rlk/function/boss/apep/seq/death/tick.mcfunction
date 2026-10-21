# AP-P1 (plan 8.4 D, 7.9): @s = body, #apPT = 0..: droop 30 (+ the face fades), the topple lands 82 (splash), wither
# 85, sink 100-118 (white leaflets every 6 t), gone 118: the golden seed at the death spot, its chime
# at 120. No creature vocals.
execute if score #apPT mb matches 30 run execute at @s run function rlk:boss/apep/fx/snd/d_droop
execute if score #apPT mb matches 30 run execute at @s run function rlk:boss/apep/fx/snd/d_face_fade
execute if score #apPT mb matches 82 run execute at @s positioned ~ 201 ~ run function rlk:boss/apep/fx/p/water_splash
execute if score #apPT mb matches 82 run execute at @s run function rlk:boss/apep/fx/snd/d_splash
execute if score #apPT mb matches 85 run execute at @s run function rlk:boss/apep/fx/snd/d_leaves
execute if score #apPT mb matches 100 run execute at @s run function rlk:boss/apep/fx/snd/d_leaves
execute if score #apPT mb matches 110 run execute at @s run function rlk:boss/apep/fx/snd/d_leaves
execute if score #apPT mb matches 100 run execute at @s rotated as @s rotated ~ 0 run function rlk:boss/apep/fx/p/leaf_dissolve
execute if score #apPT mb matches 106 run execute at @s rotated as @s rotated ~ 0 run function rlk:boss/apep/fx/p/leaf_dissolve
execute if score #apPT mb matches 112 run execute at @s rotated as @s rotated ~ 0 run function rlk:boss/apep/fx/p/leaf_dissolve
execute if score #apPT mb matches 118 run execute at @s rotated as @s rotated ~ 0 run function rlk:boss/apep/fx/p/leaf_dissolve
execute if score #apPT mb matches 100 run execute at @s run function rlk:boss/apep/fx/snd/d_sink
execute if score #apPT mb matches 118 run execute at @s positioned ~ 201 ~ rotated as @s rotated ~ 0 run function rlk:boss/apep/om/seed/spawn
execute if score #apPT mb matches 120 run execute at @s positioned ~ 201 ~ run function rlk:boss/apep/fx/snd/d_seed
