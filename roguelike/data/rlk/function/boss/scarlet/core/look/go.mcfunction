# A pending look request (#hrLook = api.LOOK_ID; @s any): the arena's look job now (no job is running).
scoreboard players operation #lk hr = #hrLook hr
execute if score #hrLook hr matches 1 in minecraft:overworld run function rlk:mboss/arena/hr_field/look/moon
execute if score #hrLook hr matches 2 in minecraft:overworld run function rlk:mboss/arena/hr_field/look/crimson
execute if score #hrLook hr matches 3 in minecraft:overworld run function rlk:mboss/arena/hr_field/look/dark
scoreboard players set #hrLook hr 0
