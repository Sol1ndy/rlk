# Next pattern: fixed rotation 1..7, overridden by the test lock (#mbLock) or a test request (#prReq).
scoreboard players add #prNext mb 1
execute if score #prNext mb matches 8.. run scoreboard players set #prNext mb 1
scoreboard players operation #prPat mb = #prNext mb
execute if score #mbLock mb matches 1..7 run scoreboard players operation #prPat mb = #mbLock mb
execute if score #prReq mb matches 1..7 run scoreboard players operation #prPat mb = #prReq mb
scoreboard players set #prReq mb 0
scoreboard players set #prT mb 0
scoreboard players set #prGoT mb 0
scoreboard players set #prGo mb 0
# Melee patterns close in first (sweep).
execute if score #prPat mb matches 3 unless entity @e[tag=rlk_body,distance=..3.6,limit=1] run scoreboard players set #prGo mb 1
execute if score #prPat mb matches 1 run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"강타",color:"#FFD86B"}]
execute if score #prPat mb matches 2 run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"찌르기",color:"#FFD86B"}]
execute if score #prPat mb matches 3 run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"휘두르기",color:"#FFD86B"}]
execute if score #prPat mb matches 4 run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"파문",color:"#FFD86B"}]
execute if score #prPat mb matches 5 run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"투창",color:"#FFD86B"}]
execute if score #prPat mb matches 6 run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"끌어당겨 회전베기",color:"#FFD86B"}]
execute if score #prPat mb matches 7 run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"전역 강타",color:"#FFD86B"}]
execute if score #prPat mb matches 1 run scoreboard players set #prLen mb 44
execute if score #prPat mb matches 2 run scoreboard players set #prLen mb 38
execute if score #prPat mb matches 3 run scoreboard players set #prLen mb 34
execute if score #prPat mb matches 4 run scoreboard players set #prLen mb 40
execute if score #prPat mb matches 5 run scoreboard players set #prLen mb 42
execute if score #prPat mb matches 6 run scoreboard players set #prLen mb 66
execute if score #prPat mb matches 7 run scoreboard players set #prLen mb 60
