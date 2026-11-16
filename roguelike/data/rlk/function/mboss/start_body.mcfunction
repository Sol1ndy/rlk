# @s = the new body, at @s (start_go, right after the spawn hook): #mbTot = its full max HP; chapter bosses: the first
# pool split (cur.phases[0] < 100) and the hit proxies (state inv until the module's intro ends).
scoreboard players operation #mbTot mb = @s mhpM
scoreboard players set #mbPoolPct mb 100
execute unless score #mbMode mb matches 1 run return 0
execute store result score #t mb run data get storage rlk:mboss cur.phases[0]
execute if score #t mb matches 1..99 store result storage rlk:mboss a.pct int 1 run scoreboard players get #t mb
execute if score #t mb matches 1..99 run function rlk:mboss/repool with storage rlk:mboss a
execute if score #mbPx mb matches 1 run function rlk:mboss/px/spawn
