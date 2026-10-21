# @s = body (bars hook, every tick): the under-bar. Phase 1: HP down to the floor (the P1 pool, Dendro colour);
# T1 / CS: the sequence progress (gold); phase 2: the Heart bar (rev/bars: #buHp = #apHt / 10, #buMax 1000,
# #buHpCol 10 gold, #buNoNum 1; cm.md 11); phase 3: HP.
execute if score #mbSt mb matches 0 run return 0
execute if score #apPh mb matches 2 run return run function rlk:boss/apep/rev/bars
execute if score #apPh mb matches 15 run return run function rlk:boss/apep/hud/bar_seq
execute if score #apPh mb matches 25 run return run function rlk:boss/apep/hud/bar_seq
scoreboard players operation #buSub bu = @s mhpC
scoreboard players operation #buSub bu -= #mbFloor mb
scoreboard players operation #buSubMax bu = @s mhpM
scoreboard players operation #buSubMax bu -= #mbFloor mb
execute if score #buSubMax bu matches ..0 run scoreboard players set #buSubMax bu 1
execute if score #buSub bu matches ..-1 run scoreboard players set #buSub bu 0
scoreboard players set #buSubCol bu 7
