# 2챕터 두뇌 준비 (@s = 새 두뇌, at @s; cm/init 끝에서, #cid = cmId)
scoreboard players set @s c2Age 0
scoreboard players set @s c2H 0
scoreboard players set @s cmAH 0
scoreboard players set @s cmAR 0
scoreboard players set @s cmAP -1
execute store result score @s cmAF run random value 0..47
execute if entity @s[tag=rlk_cm_ns] run return run function rlk:cm/ns/init
execute if entity @s[tag=rlk_cm_sl] run return run function rlk:cm/sl/init
execute if entity @s[tag=rlk_cm_ss] run return run function rlk:cm/ss/init
execute if entity @s[tag=rlk_cm_sp] run return run function rlk:cm/sp/init
execute if entity @s[tag=rlk_cm_dr] run return run function rlk:cm/dr/init
