# @s = body (module tick, phase 1): every 10 t a sample and the BACK dwell ring (3 samples; the rule needs >= 2).
scoreboard players operation #apM mb = #apFc mb
scoreboard players operation #apM mb %= #apK10 mb
execute unless score #apM mb matches 0 run return 0
function rlk:boss/apep/ai/sample
scoreboard players add #apBkI mb 1
execute if score #apBkI mb matches 3.. run scoreboard players set #apBkI mb 0
execute if score #apBkI mb matches 0 run scoreboard players set #apBk0 mb 0
execute if score #apBkI mb matches 0 if score #apZone mb matches 4 run scoreboard players set #apBk0 mb 1
execute if score #apBkI mb matches 1 run scoreboard players set #apBk1 mb 0
execute if score #apBkI mb matches 1 if score #apZone mb matches 4 run scoreboard players set #apBk1 mb 1
execute if score #apBkI mb matches 2 run scoreboard players set #apBk2 mb 0
execute if score #apBkI mb matches 2 if score #apZone mb matches 4 run scoreboard players set #apBk2 mb 1
scoreboard players set #apBackT mb 0
scoreboard players operation #apBackT mb += #apBk0 mb
scoreboard players operation #apBackT mb += #apBk1 mb
scoreboard players operation #apBackT mb += #apBk2 mb
