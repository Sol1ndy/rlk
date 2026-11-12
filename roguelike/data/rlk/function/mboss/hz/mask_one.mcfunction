# @s = a safe marker of the group: horizontal distance squared to the body (overflow-safe inside 32 b) <= (R0 + 0.3)^2.
execute if score #hzSafe mb matches 1 run return 0
execute store result score #dx mb run data get entity @s Pos[0] 1000
scoreboard players operation #dx mb -= #bx mb
execute store result score #dz mb run data get entity @s Pos[2] 1000
scoreboard players operation #dz mb -= #bz mb
execute unless score #dx mb matches -32000..32000 run return 0
execute unless score #dz mb matches -32000..32000 run return 0
scoreboard players operation #r2 mb = #dx mb
scoreboard players operation #r2 mb *= #dx mb
scoreboard players operation #t mb = #dz mb
scoreboard players operation #t mb *= #dz mb
scoreboard players operation #r2 mb += #t mb
execute if score #r2 mb <= #hzRI2 mb run scoreboard players set #hzSafe mb 1
