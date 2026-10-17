# #auxHp mb = body max HP x #auxHpPct / 100 (1..100 %, overflow-safe; no body = #auxHp unchanged).
execute unless entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run return 0
execute if score #auxHpPct mb matches 101.. run scoreboard players set #auxHpPct mb 100
scoreboard players operation #t mb = @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] mhpM
execute if score #t mb matches 10000000.. run return run function rlk:mboss/aux/pool_big
scoreboard players operation #t mb *= #auxHpPct mb
scoreboard players operation #t mb /= #c100 mb
scoreboard players operation #auxHp mb = #t mb
