# The decor props after a /reload (aux entities are gone): the moon halo and the lotus of the phase (a
# look request then sets them to its look, core/look/go).
kill @e[type=minecraft:item_display,tag=rlk_hr_deco]
execute if score #ph hr matches ..1 run summon minecraft:item_display 889.0 218 -33.0 {Tags:["rlk_room","rlk_mb_aux","rlk_hr_deco","rlk_hr_deco_moon_halo","rlk_hr_dnew"]}
execute if score #ph hr matches ..1 as @e[type=minecraft:item_display,tag=rlk_hr_dnew] at @s run tp @s ~ ~ ~ 12.38 0
execute if score #ph hr matches ..1 as @e[type=minecraft:item_display,tag=rlk_hr_dnew] run function rlk:boss/scarlet/fx/prop/moon_halo {look:"p1"}
execute if score #ph hr matches ..1 run tag @e[type=minecraft:item_display,tag=rlk_hr_dnew] remove rlk_hr_dnew
execute if score #ph hr matches ..1 run summon minecraft:item_display 859.5 200.9 -13.5 {Tags:["rlk_room","rlk_mb_aux","rlk_hr_deco","rlk_hr_deco_lotus","rlk_hr_dnew"]}
execute if score #ph hr matches ..1 as @e[type=minecraft:item_display,tag=rlk_hr_dnew] at @s run tp @s ~ ~ ~ 0 0
execute if score #ph hr matches ..1 as @e[type=minecraft:item_display,tag=rlk_hr_dnew] run function rlk:boss/scarlet/fx/prop/lotus {look:"bud"}
execute if score #ph hr matches ..1 run tag @e[type=minecraft:item_display,tag=rlk_hr_dnew] remove rlk_hr_dnew
execute if score #ph hr matches ..1 run summon minecraft:item_display 864.5 200.9 -19.5 {Tags:["rlk_room","rlk_mb_aux","rlk_hr_deco","rlk_hr_deco_lotus","rlk_hr_dnew"]}
execute if score #ph hr matches ..1 as @e[type=minecraft:item_display,tag=rlk_hr_dnew] at @s run tp @s ~ ~ ~ 47 0
execute if score #ph hr matches ..1 as @e[type=minecraft:item_display,tag=rlk_hr_dnew] run function rlk:boss/scarlet/fx/prop/lotus {look:"bud"}
execute if score #ph hr matches ..1 run tag @e[type=minecraft:item_display,tag=rlk_hr_dnew] remove rlk_hr_dnew
execute if score #ph hr matches ..1 run summon minecraft:item_display 871.5 200.9 -20.5 {Tags:["rlk_room","rlk_mb_aux","rlk_hr_deco","rlk_hr_deco_lotus","rlk_hr_dnew"]}
execute if score #ph hr matches ..1 as @e[type=minecraft:item_display,tag=rlk_hr_dnew] at @s run tp @s ~ ~ ~ 94 0
execute if score #ph hr matches ..1 as @e[type=minecraft:item_display,tag=rlk_hr_dnew] run function rlk:boss/scarlet/fx/prop/lotus {look:"bud"}
execute if score #ph hr matches ..1 run tag @e[type=minecraft:item_display,tag=rlk_hr_dnew] remove rlk_hr_dnew
execute if score #ph hr matches ..1 run summon minecraft:item_display 877.5 200.9 -23.5 {Tags:["rlk_room","rlk_mb_aux","rlk_hr_deco","rlk_hr_deco_lotus","rlk_hr_dnew"]}
execute if score #ph hr matches ..1 as @e[type=minecraft:item_display,tag=rlk_hr_dnew] at @s run tp @s ~ ~ ~ 141 0
execute if score #ph hr matches ..1 as @e[type=minecraft:item_display,tag=rlk_hr_dnew] run function rlk:boss/scarlet/fx/prop/lotus {look:"bud"}
execute if score #ph hr matches ..1 run tag @e[type=minecraft:item_display,tag=rlk_hr_dnew] remove rlk_hr_dnew
execute if score #ph hr matches ..1 run summon minecraft:item_display 884.5 200.9 -21.5 {Tags:["rlk_room","rlk_mb_aux","rlk_hr_deco","rlk_hr_deco_lotus","rlk_hr_dnew"]}
execute if score #ph hr matches ..1 as @e[type=minecraft:item_display,tag=rlk_hr_dnew] at @s run tp @s ~ ~ ~ 188 0
execute if score #ph hr matches ..1 as @e[type=minecraft:item_display,tag=rlk_hr_dnew] run function rlk:boss/scarlet/fx/prop/lotus {look:"bud"}
execute if score #ph hr matches ..1 run tag @e[type=minecraft:item_display,tag=rlk_hr_dnew] remove rlk_hr_dnew
execute if score #ph hr matches ..1 run summon minecraft:item_display 899.5 200.9 -14.5 {Tags:["rlk_room","rlk_mb_aux","rlk_hr_deco","rlk_hr_deco_lotus","rlk_hr_dnew"]}
execute if score #ph hr matches ..1 as @e[type=minecraft:item_display,tag=rlk_hr_dnew] at @s run tp @s ~ ~ ~ 235 0
execute if score #ph hr matches ..1 as @e[type=minecraft:item_display,tag=rlk_hr_dnew] run function rlk:boss/scarlet/fx/prop/lotus {look:"bud"}
execute if score #ph hr matches ..1 run tag @e[type=minecraft:item_display,tag=rlk_hr_dnew] remove rlk_hr_dnew
execute if score #ph hr matches ..1 run summon minecraft:item_display 903.5 200.9 -14.5 {Tags:["rlk_room","rlk_mb_aux","rlk_hr_deco","rlk_hr_deco_lotus","rlk_hr_dnew"]}
execute if score #ph hr matches ..1 as @e[type=minecraft:item_display,tag=rlk_hr_dnew] at @s run tp @s ~ ~ ~ 282 0
execute if score #ph hr matches ..1 as @e[type=minecraft:item_display,tag=rlk_hr_dnew] run function rlk:boss/scarlet/fx/prop/lotus {look:"bud"}
execute if score #ph hr matches ..1 run tag @e[type=minecraft:item_display,tag=rlk_hr_dnew] remove rlk_hr_dnew
execute if score #ph hr matches ..1 run summon minecraft:item_display 890.5 200.9 -19.5 {Tags:["rlk_room","rlk_mb_aux","rlk_hr_deco","rlk_hr_deco_lotus","rlk_hr_dnew"]}
execute if score #ph hr matches ..1 as @e[type=minecraft:item_display,tag=rlk_hr_dnew] at @s run tp @s ~ ~ ~ 329 0
execute if score #ph hr matches ..1 as @e[type=minecraft:item_display,tag=rlk_hr_dnew] run function rlk:boss/scarlet/fx/prop/lotus {look:"bud"}
execute if score #ph hr matches ..1 run tag @e[type=minecraft:item_display,tag=rlk_hr_dnew] remove rlk_hr_dnew
execute if score #ph hr matches 2.. run summon minecraft:item_display 889.0 218 -33.0 {Tags:["rlk_room","rlk_mb_aux","rlk_hr_deco","rlk_hr_deco_moon_halo","rlk_hr_dnew"]}
execute if score #ph hr matches 2.. as @e[type=minecraft:item_display,tag=rlk_hr_dnew] at @s run tp @s ~ ~ ~ 12.38 0
execute if score #ph hr matches 2.. as @e[type=minecraft:item_display,tag=rlk_hr_dnew] run function rlk:boss/scarlet/fx/prop/moon_halo {look:"p2"}
execute if score #ph hr matches 2.. run tag @e[type=minecraft:item_display,tag=rlk_hr_dnew] remove rlk_hr_dnew
execute if score #ph hr matches 2.. run summon minecraft:item_display 859.5 200.9 -13.5 {Tags:["rlk_room","rlk_mb_aux","rlk_hr_deco","rlk_hr_deco_lotus","rlk_hr_dnew"]}
execute if score #ph hr matches 2.. as @e[type=minecraft:item_display,tag=rlk_hr_dnew] at @s run tp @s ~ ~ ~ 0 0
execute if score #ph hr matches 2.. as @e[type=minecraft:item_display,tag=rlk_hr_dnew] run function rlk:boss/scarlet/fx/prop/lotus {look:"bloom"}
execute if score #ph hr matches 2.. run tag @e[type=minecraft:item_display,tag=rlk_hr_dnew] remove rlk_hr_dnew
execute if score #ph hr matches 2.. run summon minecraft:item_display 864.5 200.9 -19.5 {Tags:["rlk_room","rlk_mb_aux","rlk_hr_deco","rlk_hr_deco_lotus","rlk_hr_dnew"]}
execute if score #ph hr matches 2.. as @e[type=minecraft:item_display,tag=rlk_hr_dnew] at @s run tp @s ~ ~ ~ 47 0
execute if score #ph hr matches 2.. as @e[type=minecraft:item_display,tag=rlk_hr_dnew] run function rlk:boss/scarlet/fx/prop/lotus {look:"bloom"}
execute if score #ph hr matches 2.. run tag @e[type=minecraft:item_display,tag=rlk_hr_dnew] remove rlk_hr_dnew
execute if score #ph hr matches 2.. run summon minecraft:item_display 871.5 200.9 -20.5 {Tags:["rlk_room","rlk_mb_aux","rlk_hr_deco","rlk_hr_deco_lotus","rlk_hr_dnew"]}
execute if score #ph hr matches 2.. as @e[type=minecraft:item_display,tag=rlk_hr_dnew] at @s run tp @s ~ ~ ~ 94 0
execute if score #ph hr matches 2.. as @e[type=minecraft:item_display,tag=rlk_hr_dnew] run function rlk:boss/scarlet/fx/prop/lotus {look:"bloom"}
execute if score #ph hr matches 2.. run tag @e[type=minecraft:item_display,tag=rlk_hr_dnew] remove rlk_hr_dnew
execute if score #ph hr matches 2.. run summon minecraft:item_display 877.5 200.9 -23.5 {Tags:["rlk_room","rlk_mb_aux","rlk_hr_deco","rlk_hr_deco_lotus","rlk_hr_dnew"]}
execute if score #ph hr matches 2.. as @e[type=minecraft:item_display,tag=rlk_hr_dnew] at @s run tp @s ~ ~ ~ 141 0
execute if score #ph hr matches 2.. as @e[type=minecraft:item_display,tag=rlk_hr_dnew] run function rlk:boss/scarlet/fx/prop/lotus {look:"bloom"}
execute if score #ph hr matches 2.. run tag @e[type=minecraft:item_display,tag=rlk_hr_dnew] remove rlk_hr_dnew
execute if score #ph hr matches 2.. run summon minecraft:item_display 884.5 200.9 -21.5 {Tags:["rlk_room","rlk_mb_aux","rlk_hr_deco","rlk_hr_deco_lotus","rlk_hr_dnew"]}
execute if score #ph hr matches 2.. as @e[type=minecraft:item_display,tag=rlk_hr_dnew] at @s run tp @s ~ ~ ~ 188 0
execute if score #ph hr matches 2.. as @e[type=minecraft:item_display,tag=rlk_hr_dnew] run function rlk:boss/scarlet/fx/prop/lotus {look:"bloom"}
execute if score #ph hr matches 2.. run tag @e[type=minecraft:item_display,tag=rlk_hr_dnew] remove rlk_hr_dnew
execute if score #ph hr matches 2.. run summon minecraft:item_display 899.5 200.9 -14.5 {Tags:["rlk_room","rlk_mb_aux","rlk_hr_deco","rlk_hr_deco_lotus","rlk_hr_dnew"]}
execute if score #ph hr matches 2.. as @e[type=minecraft:item_display,tag=rlk_hr_dnew] at @s run tp @s ~ ~ ~ 235 0
execute if score #ph hr matches 2.. as @e[type=minecraft:item_display,tag=rlk_hr_dnew] run function rlk:boss/scarlet/fx/prop/lotus {look:"bloom"}
execute if score #ph hr matches 2.. run tag @e[type=minecraft:item_display,tag=rlk_hr_dnew] remove rlk_hr_dnew
execute if score #ph hr matches 2.. run summon minecraft:item_display 903.5 200.9 -14.5 {Tags:["rlk_room","rlk_mb_aux","rlk_hr_deco","rlk_hr_deco_lotus","rlk_hr_dnew"]}
execute if score #ph hr matches 2.. as @e[type=minecraft:item_display,tag=rlk_hr_dnew] at @s run tp @s ~ ~ ~ 282 0
execute if score #ph hr matches 2.. as @e[type=minecraft:item_display,tag=rlk_hr_dnew] run function rlk:boss/scarlet/fx/prop/lotus {look:"bloom"}
execute if score #ph hr matches 2.. run tag @e[type=minecraft:item_display,tag=rlk_hr_dnew] remove rlk_hr_dnew
execute if score #ph hr matches 2.. run summon minecraft:item_display 890.5 200.9 -19.5 {Tags:["rlk_room","rlk_mb_aux","rlk_hr_deco","rlk_hr_deco_lotus","rlk_hr_dnew"]}
execute if score #ph hr matches 2.. as @e[type=minecraft:item_display,tag=rlk_hr_dnew] at @s run tp @s ~ ~ ~ 329 0
execute if score #ph hr matches 2.. as @e[type=minecraft:item_display,tag=rlk_hr_dnew] run function rlk:boss/scarlet/fx/prop/lotus {look:"bloom"}
execute if score #ph hr matches 2.. run tag @e[type=minecraft:item_display,tag=rlk_hr_dnew] remove rlk_hr_dnew
