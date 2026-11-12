# 3챕터 두뇌 준비 (@s = 새 두뇌, at @s; cm/init 끝에서, #cid = cmId)
scoreboard players set @s c2Age 0
execute unless entity @s[tag=rlk_c3a] run return 0
scoreboard players set @s cmAH 0
scoreboard players set @s cmAR 0
scoreboard players set @s cmAP -1
execute store result score @s cmAF run random value 0..47
execute if entity @s[tag=rlk_cm_fu] run return run function rlk:cm/fu/init
execute if entity @s[tag=rlk_cm_em] run return run function rlk:cm/em/init
execute if entity @s[tag=rlk_cm_sb] run return run function rlk:cm/sb/init
execute if entity @s[tag=rlk_cm_cw] run return run function rlk:cm/cw/init
