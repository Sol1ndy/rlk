# STUB (AP-CORE, ap_contract 1.6): the revival stage; AP-REV replaces this file.
# @s = body (bars hook, phase 2): the gold progress bar (#buHp = #apHt / 10 of 1000, colour 10, no
# numbers; cm.md 11); the under-bar = the time to the warning (gold), red after it.
scoreboard players operation #buHp bu = #apHt mb
scoreboard players operation #buHp bu /= #c10 mb
scoreboard players set #buMax bu 1000
scoreboard players set #buHpCol bu 10
scoreboard players set #buNoNum bu 1
scoreboard players set #buSub bu 2000
scoreboard players operation #buSub bu -= #apClk mb
execute if score #buSub bu matches ..-1 run scoreboard players set #buSub bu 0
scoreboard players set #buSubMax bu 2000
scoreboard players set #buSubCol bu 5
execute if score #apTo mb matches 1 run scoreboard players set #buSub bu 2000
execute if score #apTo mb matches 1 run scoreboard players set #buSubCol bu 2
