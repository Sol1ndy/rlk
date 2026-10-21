# @s = body: per-element RES (plan 4.2): the registry res (0 / 5 / *) + the rolled pair 30 (cm.md 8).
scoreboard players set @s mbRes1 10
scoreboard players set @s mbRes2 10
scoreboard players set @s mbRes3 10
scoreboard players set @s mbRes4 10
execute if score #azLeg mb matches 1 run scoreboard players set @s mbRes1 30
execute if score #azLeg mb matches 2 run scoreboard players set @s mbRes2 30
execute if score #azTail mb matches 3 run scoreboard players set @s mbRes3 30
execute if score #azTail mb matches 4 run scoreboard players set @s mbRes4 30
