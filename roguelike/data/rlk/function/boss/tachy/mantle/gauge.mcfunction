# The mantle gauge changed (@s = body): the cocoon card of its quarter (the gauge is the boss-bar under-bar).
scoreboard players operation #hud_g tk = #sh tk
execute if score #sh tk matches 76..1000 unless score #hud_c tk matches 100 at @s rotated as @s rotated ~ 0 positioned ~ ~1.5 ~ run function rlk:boss/tachy/fx/p/cocoon {pct:100}
execute if score #sh tk matches 76..1000 run scoreboard players set #hud_c tk 100
execute if score #sh tk matches 51..75 unless score #hud_c tk matches 75 at @s rotated as @s rotated ~ 0 positioned ~ ~1.5 ~ run function rlk:boss/tachy/fx/p/cocoon {pct:75}
execute if score #sh tk matches 51..75 run scoreboard players set #hud_c tk 75
execute if score #sh tk matches 26..50 unless score #hud_c tk matches 50 at @s rotated as @s rotated ~ 0 positioned ~ ~1.5 ~ run function rlk:boss/tachy/fx/p/cocoon {pct:50}
execute if score #sh tk matches 26..50 run scoreboard players set #hud_c tk 50
execute if score #sh tk matches -1000..25 unless score #hud_c tk matches 25 at @s rotated as @s rotated ~ 0 positioned ~ ~1.5 ~ run function rlk:boss/tachy/fx/p/cocoon {pct:25}
execute if score #sh tk matches -1000..25 run scoreboard players set #hud_c tk 25
