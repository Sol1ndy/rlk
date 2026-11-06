# @s = travelling hazard at rel rdHSp (its cards' summon): the cards at the front of rel rdHGo, still; vis/travel_go
# gives them their ONE interpolation (to the end state over F - rdHGo ticks) at rel rdHGo, raiden_kit.TRAVEL_GAP
# ticks after this summon, so the client has ticked them before (user 10-22: else it may show the end state).
scoreboard players operation #rdD rd = @s rdHF
scoreboard players operation #rdD rd -= @s rdHGo
execute store result storage rlk:rd v.d int 1 run scoreboard players get #rdD rd
scoreboard players operation #rdR0 rd = @s rdHB
scoreboard players operation #rdR0 rd *= @s rdHGo
scoreboard players operation #rdR0 rd /= #rdK1000 rd
scoreboard players operation #rdR0 rd += @s rdHA
scoreboard players operation #rdR1 rd = @s rdHB
scoreboard players operation #rdR1 rd *= @s rdHF
scoreboard players operation #rdR1 rd /= #rdK1000 rd
scoreboard players operation #rdR1 rd += @s rdHA
execute store result storage rlk:rd v.tz0 float 0.001 run scoreboard players get #rdR0 rd
execute store result storage rlk:rd v.tz1 float 0.001 run scoreboard players get #rdR1 rd
execute if score @s rdHK matches 5 run function rlk:boss/raiden/hazard/vis/travel_sweep
execute if score @s rdHK matches 6 run function rlk:boss/raiden/hazard/vis/travel_slab
execute if score @s rdHK matches 7 run function rlk:boss/raiden/hazard/vis/travel_orb
scoreboard players operation @e[tag=rlk_rd_vown] rdVId = @s rdHId
tag @e[tag=rlk_rd_vown] remove rlk_rd_vown
