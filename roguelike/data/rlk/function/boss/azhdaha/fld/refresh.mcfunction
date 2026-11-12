# Macro {n} (@s = a field hazard marker, azF = its slot): extend by n, at most 2x its base life; the kit redraws it.
$scoreboard players set #azX mb $(n)
scoreboard players operation #azNfI mb = @s azF
execute if score #azNfI mb matches 0 run return run function rlk:boss/azhdaha/fld/ext_0
execute if score #azNfI mb matches 1 run return run function rlk:boss/azhdaha/fld/ext_1
execute if score #azNfI mb matches 2 run return run function rlk:boss/azhdaha/fld/ext_2
execute if score #azNfI mb matches 3 run return run function rlk:boss/azhdaha/fld/ext_3
execute if score #azNfI mb matches 4 run return run function rlk:boss/azhdaha/fld/ext_4
execute if score #azNfI mb matches 5 run return run function rlk:boss/azhdaha/fld/ext_5
execute if score #azNfI mb matches 6 run return run function rlk:boss/azhdaha/fld/ext_6
execute if score #azNfI mb matches 7 run return run function rlk:boss/azhdaha/fld/ext_7
