# {pct} (as anything; 1..100): the body's pool = #mbTot x pct / 100 (overflow-safe), full; the HP bar refills over 30 t
# (#mbRamp, mboss/bars). #mbPoolPct remembers the split (test/level re-applies it).
$scoreboard players set #mbPoolPct mb $(pct)
execute if score #mbPoolPct mb matches ..0 run scoreboard players set #mbPoolPct mb 1
execute if score #mbPoolPct mb matches 101.. run scoreboard players set #mbPoolPct mb 100
scoreboard players operation #t mb = #mbTot mb
execute if score #t mb matches 10000000.. run scoreboard players operation #t mb /= #c100 mb
scoreboard players operation #t mb *= #mbPoolPct mb
execute if score #mbTot mb matches ..9999999 run scoreboard players operation #t mb /= #c100 mb
execute if score #t mb matches ..0 run scoreboard players set #t mb 1
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run scoreboard players operation @s mhpM = #t mb
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run scoreboard players operation @s mhpC = #t mb
scoreboard players set #mbRamp mb 30
