# A pending look request (#hrLook = api.LOOK_ID; @s any): the arena's look job now (no job is running), unless the
# arena already stands in that look (its stamp; a job drops the stamp when it starts, so a cut one runs again).
scoreboard players operation #lk hr = #hrLook hr
execute if score #hrLook hr matches 1 unless data storage rlk:mboss {built_hr_field:"hr_field@1:moon"} in minecraft:overworld run function rlk:mboss/arena/hr_field/look/moon
execute if score #hrLook hr matches 2 unless data storage rlk:mboss {built_hr_field:"hr_field@1:crimson"} in minecraft:overworld run function rlk:mboss/arena/hr_field/look/crimson
execute if score #hrLook hr matches 3 unless data storage rlk:mboss {built_hr_field:"hr_field@1:dark"} in minecraft:overworld run function rlk:mboss/arena/hr_field/look/dark
execute if score #hrLook hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_deco_moon_halo] run function rlk:boss/scarlet/fx/prop/moon_halo {look:"p1"}
execute if score #hrLook hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_deco_lotus] run function rlk:boss/scarlet/fx/prop/lotus {look:"bud"}
execute if score #hrLook hr matches 2 as @e[type=minecraft:item_display,tag=rlk_hr_deco_moon_halo] run function rlk:boss/scarlet/fx/prop/moon_halo {look:"p2"}
execute if score #hrLook hr matches 2 as @e[type=minecraft:item_display,tag=rlk_hr_deco_lotus] run function rlk:boss/scarlet/fx/prop/lotus {look:"bloom"}
execute if score #hrLook hr matches 3 as @e[type=minecraft:item_display,tag=rlk_hr_deco_moon_halo] run function rlk:boss/scarlet/fx/prop/moon_halo {look:"off"}
execute if score #hrLook hr matches 3 as @e[type=minecraft:item_display,tag=rlk_hr_deco_lotus] run function rlk:boss/scarlet/fx/prop/lotus {look:"bloom"}
scoreboard players set #hrLook hr 0
