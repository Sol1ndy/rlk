# 소멸 (@s = 몹, at @s): 표시 · 효과 + 로노바의 고유 특성 「삼킨 이름」: 잔향 1칸(몹에 붙어 있던 원소, 없으면 무작위) · 원소 에너지 2pt
function rlk:element/rx_text3 {name:"소멸",col:"#E0365F"}
particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.6 0.3 0.6 60
particle minecraft:dust{color:[0.88,0.12,0.22],scale:2.0} ~ ~1 ~ 0.3 0.6 0.3 0 30
particle minecraft:dust{color:[0.08,0.02,0.05],scale:1.6} ~ ~1 ~ 0.2 0.5 0.2 0 20
particle minecraft:squid_ink ~ ~1 ~ 0.2 0.4 0.2 0.05 10
playsound minecraft:block.respawn_anchor.deplete master @a ~ ~ ~ 0.9 0.7
playsound minecraft:entity.vex.death master @a ~ ~ ~ 0.6 0.5
execute unless score #charN tmp matches 7 run return 0
execute store result score #rvE tmp run random value 1..7
execute if score @s aGrass matches 1.. run scoreboard players set #rvE tmp 7
execute if score @s aIce matches 1.. run scoreboard players set #rvE tmp 4
execute if score @s frzT matches 1.. run scoreboard players set #rvE tmp 4
execute if score @s aThunder matches 1.. run scoreboard players set #rvE tmp 3
execute if score @s aWater matches 1.. run scoreboard players set #rvE tmp 2
execute if score @s aFire matches 1.. run scoreboard players set #rvE tmp 1
execute if score #rvE tmp matches 7 run scoreboard players set #rvE tmp 9
execute as @a[tag=player,limit=1] run function rlk:char/ronova/echo_add
scoreboard players add @a[tag=player,limit=1] energy 200
