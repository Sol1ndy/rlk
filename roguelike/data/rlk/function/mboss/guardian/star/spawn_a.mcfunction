# @s = body: star of slot A (her right, the player's left), 4.2 b out. Kind = the recorded element (active) or 5 (inert 타성(금)).
scoreboard players operation #gdSk1 mb = #gdSlotA mb
execute if score #gdSk1 mb matches 0 run scoreboard players set #gdSk1 mb 5
scoreboard players operation #gdSk mb = #gdSk1 mb
scoreboard players set #gdSs mb 1
scoreboard players set #gdSa1 mb 1
execute rotated as @s rotated ~24 0 positioned ^ ^ ^4.2 positioned ~ 201 ~ run function rlk:mboss/guardian/star/make
