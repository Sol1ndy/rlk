# The floor popup "흡수 중 (raw)" (the unclamped value in grey), at most once per 10 t, above the head.
scoreboard players operation #azX mb = #azClk mb
scoreboard players operation #azX mb -= #azPopC mb
execute if score #azX mb matches ..9 run return 0
scoreboard players operation #azPopC mb = #azClk mb
execute store result storage rlk:mboss az.pop.raw int 1 run scoreboard players get #mbFloorRaw mb
execute at @s rotated as @s positioned ^ ^4.2 ^4.3 run function rlk:mboss/azhdaha/ev/pop_m with storage rlk:mboss az.pop
