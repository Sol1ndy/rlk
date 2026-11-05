# A pending look request (#hrLook = api.LOOK_ID; @s any): the arena's look job now (no job is running).
scoreboard players operation #lk hr = #hrLook hr
execute if score #hrLook hr matches 1 in minecraft:overworld run function rlk:mboss/arena/hr_field/look/moon
execute if score #hrLook hr matches 2 in minecraft:overworld run function rlk:mboss/arena/hr_field/look/crimson
execute if score #hrLook hr matches 3 in minecraft:overworld run function rlk:mboss/arena/hr_field/look/dark
execute if score #hrLook hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_deco_moon_halo] run function rlk:boss/scarlet/fx/prop/moon_halo {look:"p1"}
execute if score #hrLook hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_deco_lotus] run function rlk:boss/scarlet/fx/prop/lotus {look:"bud"}
execute if score #hrLook hr matches 2 as @e[type=minecraft:item_display,tag=rlk_hr_deco_moon_halo] run function rlk:boss/scarlet/fx/prop/moon_halo {look:"p2"}
execute if score #hrLook hr matches 2 as @e[type=minecraft:item_display,tag=rlk_hr_deco_lotus] run function rlk:boss/scarlet/fx/prop/lotus {look:"bloom"}
execute if score #hrLook hr matches 3 as @e[type=minecraft:item_display,tag=rlk_hr_deco_moon_halo] run function rlk:boss/scarlet/fx/prop/moon_halo {look:"off"}
execute if score #hrLook hr matches 3 as @e[type=minecraft:item_display,tag=rlk_hr_deco_lotus] run function rlk:boss/scarlet/fx/prop/lotus {look:"bloom"}
scoreboard players set #hrLook hr 0
