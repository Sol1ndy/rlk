# @s = body: timer, haze, cube streams (ambient, no damage, K11).
scoreboard players remove #gdTim mb 1
scoreboard players operation #gdTimS mb = #gdTim mb
scoreboard players add #gdTimS mb 19
scoreboard players operation #gdTimS mb /= #gdK20 mb
execute if score #gdHaze mb matches 1 run function rlk:mboss/guardian/chaos/haze
scoreboard players remove #gdCsT mb 1
execute if score #gdCsT mb matches ..0 run function rlk:mboss/guardian/chaos/cs_spawn
function rlk:mboss/guardian/chaos/cs_all
scoreboard players operation #gdM mb = #gdT mb
scoreboard players operation #gdM mb %= #gdK8 mb
execute if score #gdM mb matches 0 run particle minecraft:dust{color:[0.75f,0.1f,0.18f],scale:1.2} ~ ~6.7 ~ 0.4 0.3 0.4 0 3 force @a[tag=player]
execute if score #gdTim mb matches ..0 run function rlk:mboss/guardian/chaos/fail_start
