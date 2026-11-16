# @s = body: star of slot B (her left, the player's right), 4.2 b out. Kind = the recorded element (active) or 6 (inert 타성(청)).
scoreboard players operation #gdSk2 mb = #gdSlotB mb
execute if score #gdSk2 mb matches 0 run scoreboard players set #gdSk2 mb 6
scoreboard players operation #gdSk mb = #gdSk2 mb
scoreboard players set #gdSs mb 2
scoreboard players set #gdSa2 mb 1
execute rotated as @s rotated ~-24 0 positioned ^ ^ ^4.2 positioned ~ 201 ~ run function rlk:mboss/guardian/star/make
