# The HP run of bossui/draw in the #buHpCol colour (1..9 = SUB_COLORS, 10 = gold); #len bu = the HP fill.
execute if score #buHpCol bu matches 1 run return run function rlk:bossui/run_hp {col:"#C58BFF"}
execute if score #buHpCol bu matches 2 run return run function rlk:bossui/run_hp {col:"#FF8A3D"}
execute if score #buHpCol bu matches 3 run return run function rlk:bossui/run_hp {col:"#4FB8FF"}
execute if score #buHpCol bu matches 4 run return run function rlk:bossui/run_hp {col:"#9FE8F5"}
execute if score #buHpCol bu matches 5 run return run function rlk:bossui/run_hp {col:"#F2C14E"}
execute if score #buHpCol bu matches 6 run return run function rlk:bossui/run_hp {col:"#6FE3C1"}
execute if score #buHpCol bu matches 7 run return run function rlk:bossui/run_hp {col:"#A5D94A"}
execute if score #buHpCol bu matches 8 run return run function rlk:bossui/run_hp {col:"#E8C35A"}
execute if score #buHpCol bu matches 9 run return run function rlk:bossui/run_hp {col:"#7BD88F"}
execute if score #buHpCol bu matches 10 run return run function rlk:bossui/run_hp {col:"#EDCF63"}
