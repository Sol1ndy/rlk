# 6b blade eye (A-11, polearm after-effect): an eye sigil 1.5 b beside the player, glint 8, burst 12 (disk r 2).
scoreboard players set @s rdSgFxT 0
kill @e[tag=rlk_rd_sgfx]
execute store result score #rdSgSide rd run random value 0..1
execute if score #rdSgSide rd matches 0 at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~ 0 positioned ^1.5 ^ ^0 positioned ~ 201 ~ run function rlk:boss/raiden/sg/fx6b_at
execute if score #rdSgSide rd matches 1 at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~ 0 positioned ^-1.5 ^ ^0 positioned ~ 201 ~ run function rlk:boss/raiden/sg/fx6b_at
