# Pull tell (27 ticks): a red cage around the player, every 3rd tick.
scoreboard players operation #t mb = #prT mb
scoreboard players operation #t mb %= #c3 mb
execute if score #t mb matches 0 at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.9f,0.1f,0.15f],scale:1.4f} ~ ~1 ~ 0.7 0.9 0.7 0 14 force @a[tag=player]
