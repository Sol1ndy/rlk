scoreboard players set @s pmAtkPending 0
execute unless score @s pmAtkKind = #charN tmp run return 0
execute if score #charN tmp matches 3 run function rlk:char/skirk/na_extra
execute if score #charN tmp matches 5 run function rlk:char/melee/extra
scoreboard players set @s skQ 0
scoreboard players set @s naQ 0
