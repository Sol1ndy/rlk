# @s = a new to_wall hazard: length from the origin along its yaw to the arena wall circle (r 24), at most 47.
scoreboard players set @s rdHA 47000
execute unless entity @e[tag=rlk_raiden_arena,limit=1] run return 0
execute store result score #rdPX rd run data get entity @s Pos[0] 1000
execute store result score #rdPZ rd run data get entity @s Pos[2] 1000
execute store result score #rdCX rd run data get entity @e[tag=rlk_raiden_arena,limit=1] Pos[0] 1000
execute store result score #rdCZ rd run data get entity @e[tag=rlk_raiden_arena,limit=1] Pos[2] 1000
scoreboard players operation #rdPX rd -= #rdCX rd
scoreboard players operation #rdPZ rd -= #rdCZ rd
scoreboard players operation #rdB rd = #rdPX rd
scoreboard players operation #rdB rd *= @s rdFX
scoreboard players operation #rdT rd = #rdPZ rd
scoreboard players operation #rdT rd *= @s rdFZ
scoreboard players operation #rdB rd += #rdT rd
scoreboard players operation #rdB rd /= #rdK1000 rd
scoreboard players operation #rdC rd = #rdPX rd
scoreboard players operation #rdC rd *= #rdPX rd
scoreboard players operation #rdT rd = #rdPZ rd
scoreboard players operation #rdT rd *= #rdPZ rd
scoreboard players operation #rdC rd += #rdT rd
scoreboard players set #rdT rd 576000000
scoreboard players operation #rdC rd -= #rdT rd
scoreboard players operation #rdDisc rd = #rdB rd
scoreboard players operation #rdDisc rd *= #rdB rd
scoreboard players operation #rdDisc rd -= #rdC rd
execute unless score #rdDisc rd matches 1.. run return 0
scoreboard players set #rdX rd 34000
scoreboard players set #rdTwo rd 2
scoreboard players operation #rdT rd = #rdDisc rd
scoreboard players operation #rdT rd /= #rdX rd
scoreboard players operation #rdX rd += #rdT rd
scoreboard players operation #rdX rd /= #rdTwo rd
scoreboard players operation #rdT rd = #rdDisc rd
scoreboard players operation #rdT rd /= #rdX rd
scoreboard players operation #rdX rd += #rdT rd
scoreboard players operation #rdX rd /= #rdTwo rd
scoreboard players operation #rdT rd = #rdDisc rd
scoreboard players operation #rdT rd /= #rdX rd
scoreboard players operation #rdX rd += #rdT rd
scoreboard players operation #rdX rd /= #rdTwo rd
scoreboard players operation #rdT rd = #rdDisc rd
scoreboard players operation #rdT rd /= #rdX rd
scoreboard players operation #rdX rd += #rdT rd
scoreboard players operation #rdX rd /= #rdTwo rd
scoreboard players operation #rdT rd = #rdDisc rd
scoreboard players operation #rdT rd /= #rdX rd
scoreboard players operation #rdX rd += #rdT rd
scoreboard players operation #rdX rd /= #rdTwo rd
scoreboard players operation #rdT rd = #rdDisc rd
scoreboard players operation #rdT rd /= #rdX rd
scoreboard players operation #rdX rd += #rdT rd
scoreboard players operation #rdX rd /= #rdTwo rd
scoreboard players operation #rdT rd = #rdDisc rd
scoreboard players operation #rdT rd /= #rdX rd
scoreboard players operation #rdX rd += #rdT rd
scoreboard players operation #rdX rd /= #rdTwo rd
scoreboard players operation #rdT rd = #rdDisc rd
scoreboard players operation #rdT rd /= #rdX rd
scoreboard players operation #rdX rd += #rdT rd
scoreboard players operation #rdX rd /= #rdTwo rd
scoreboard players operation #rdT rd = #rdDisc rd
scoreboard players operation #rdT rd /= #rdX rd
scoreboard players operation #rdX rd += #rdT rd
scoreboard players operation #rdX rd /= #rdTwo rd
scoreboard players operation #rdX rd -= #rdB rd
execute if score #rdX rd matches 0..47000 run scoreboard players operation @s rdHA = #rdX rd
execute if score #rdX rd matches ..-1 run scoreboard players set @s rdHA 0
