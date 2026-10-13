# As the boss: the white trail follows HP down only after TRAIL_DELAY ticks without damage.
execute unless score @s buTrail matches 0.. run scoreboard players operation @s buTrail = #buHp bu
execute unless score @s buLast matches 0.. run scoreboard players operation @s buLast = #buHp bu
execute if score #buHp bu < @s buLast run scoreboard players set @s buT 0
scoreboard players add @s buT 1
execute if score @s buTrail < #buHp bu run scoreboard players operation @s buTrail = #buHp bu
execute if score @s buT matches 16.. if score @s buTrail > #buHp bu run function rlk:bossui/trail_step
scoreboard players operation @s buLast = #buHp bu
