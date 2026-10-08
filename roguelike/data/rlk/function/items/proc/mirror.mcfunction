# @s = 플레이어, 위치 = 몸. 보호막(최대 체력의 #mirShield%) + 주변 6칸 적에게 '받는 피해 증가' 표시
scoreboard players operation #amt tmp = @s maxHealth
scoreboard players operation #amt tmp *= #mirShield tmp
scoreboard players operation #amt tmp /= #100 tmp
execute if score #amt tmp matches ..0 run scoreboard players set #amt tmp 1
function rlk:element/shield_gain
execute store result score #t1 itv run time query gametime
scoreboard players operation #t1 itv += #mirDur tmp
scoreboard players operation @e[tag=rlk_mob,distance=..6] mirEnd = #t1 itv
execute at @e[tag=rlk_mob,distance=..6] run particle minecraft:dust{color:[0.25f,0.2f,0.35f],scale:1.2f} ~ ~2.1 ~ 0.2 0.1 0.2 0 8
particle minecraft:dust{color:[0.25f,0.2f,0.35f],scale:1.0f} ~6.00 ~0.2 ~0.00 0 0 0 0 1
particle minecraft:dust{color:[0.25f,0.2f,0.35f],scale:1.0f} ~5.80 ~0.2 ~1.55 0 0 0 0 1
particle minecraft:dust{color:[0.25f,0.2f,0.35f],scale:1.0f} ~5.20 ~0.2 ~3.00 0 0 0 0 1
particle minecraft:dust{color:[0.25f,0.2f,0.35f],scale:1.0f} ~4.24 ~0.2 ~4.24 0 0 0 0 1
particle minecraft:dust{color:[0.25f,0.2f,0.35f],scale:1.0f} ~3.00 ~0.2 ~5.20 0 0 0 0 1
particle minecraft:dust{color:[0.25f,0.2f,0.35f],scale:1.0f} ~1.55 ~0.2 ~5.80 0 0 0 0 1
particle minecraft:dust{color:[0.25f,0.2f,0.35f],scale:1.0f} ~0.00 ~0.2 ~6.00 0 0 0 0 1
particle minecraft:dust{color:[0.25f,0.2f,0.35f],scale:1.0f} ~-1.55 ~0.2 ~5.80 0 0 0 0 1
particle minecraft:dust{color:[0.25f,0.2f,0.35f],scale:1.0f} ~-3.00 ~0.2 ~5.20 0 0 0 0 1
particle minecraft:dust{color:[0.25f,0.2f,0.35f],scale:1.0f} ~-4.24 ~0.2 ~4.24 0 0 0 0 1
particle minecraft:dust{color:[0.25f,0.2f,0.35f],scale:1.0f} ~-5.20 ~0.2 ~3.00 0 0 0 0 1
particle minecraft:dust{color:[0.25f,0.2f,0.35f],scale:1.0f} ~-5.80 ~0.2 ~1.55 0 0 0 0 1
particle minecraft:dust{color:[0.25f,0.2f,0.35f],scale:1.0f} ~-6.00 ~0.2 ~0.00 0 0 0 0 1
particle minecraft:dust{color:[0.25f,0.2f,0.35f],scale:1.0f} ~-5.80 ~0.2 ~-1.55 0 0 0 0 1
particle minecraft:dust{color:[0.25f,0.2f,0.35f],scale:1.0f} ~-5.20 ~0.2 ~-3.00 0 0 0 0 1
particle minecraft:dust{color:[0.25f,0.2f,0.35f],scale:1.0f} ~-4.24 ~0.2 ~-4.24 0 0 0 0 1
particle minecraft:dust{color:[0.25f,0.2f,0.35f],scale:1.0f} ~-3.00 ~0.2 ~-5.20 0 0 0 0 1
particle minecraft:dust{color:[0.25f,0.2f,0.35f],scale:1.0f} ~-1.55 ~0.2 ~-5.80 0 0 0 0 1
particle minecraft:dust{color:[0.25f,0.2f,0.35f],scale:1.0f} ~-0.00 ~0.2 ~-6.00 0 0 0 0 1
particle minecraft:dust{color:[0.25f,0.2f,0.35f],scale:1.0f} ~1.55 ~0.2 ~-5.80 0 0 0 0 1
particle minecraft:dust{color:[0.25f,0.2f,0.35f],scale:1.0f} ~3.00 ~0.2 ~-5.20 0 0 0 0 1
particle minecraft:dust{color:[0.25f,0.2f,0.35f],scale:1.0f} ~4.24 ~0.2 ~-4.24 0 0 0 0 1
particle minecraft:dust{color:[0.25f,0.2f,0.35f],scale:1.0f} ~5.20 ~0.2 ~-3.00 0 0 0 0 1
particle minecraft:dust{color:[0.25f,0.2f,0.35f],scale:1.0f} ~5.80 ~0.2 ~-1.55 0 0 0 0 1
