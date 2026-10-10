# As boss, at its position before any relocation this tick. Parts wait under the floor
# with teleport_duration 0, so the reappearance frame snaps instead of sliding up/across.
execute unless score @s rdHidden matches 1 as @e[tag=rlk_raiden_part] run data merge entity @s {teleport_duration:0}
scoreboard players set @s rdHidden 1
tp @e[tag=rlk_raiden_part] ~ ~-60 ~
