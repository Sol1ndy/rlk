# A new brand (5 DoT ticks, the first 20 t later); a Cryo strike starts at 1 stack.
scoreboard players operation @s azBrE = #azBrIn mb
scoreboard players set @s azBrT 5
scoreboard players set @s azBrC 20
scoreboard players set @s azBrS 0
execute if score #azBrIn mb matches 4 run scoreboard players set @s azBrS 1
execute if score #azBrIn mb matches 4 if score #azBrStrike mb matches 1 run scoreboard players set #azBrCs mb 1
scoreboard players set #azBrNew mb 1
scoreboard players set #azHeal mb 0
function rlk:boss/azhdaha/fx/snd/brand_apply
