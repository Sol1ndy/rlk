# Third timeline hit of one clip (pmThird = hit_ticks[2]); same extra-strike path as combat/second.
scoreboard players set @s pmAtkPending 0
execute unless score @s pmAtkKind = #charN tmp run return 0
execute if score #charN tmp matches 6 run function rlk:char/melee/extra
scoreboard players set @s skQ 0
scoreboard players set @s naQ 0
scoreboard players set @s naQn 0
