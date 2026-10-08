# 일반 공격 붉은 시선 (@s = 플레이어, at 몸): 붉은 눈 구체 4타(72% / 66% / 90% / 120%, 가까운 적을 쫓아감). 공허 원소, 4타는 부착 쿨 없이 공허를 묻힌다
execute store result score #now tmp run time query gametime
execute if score @s swungAt = #now tmp run return 0
scoreboard players operation @s swungAt = #now tmp
execute as @e[tag=rlk_av,limit=1] run swing @s mainhand
scoreboard players operation #step tmp = @s comboStep
scoreboard players set #coef tmp 72
execute if score #step tmp matches 1 run scoreboard players set #coef tmp 66
execute if score #step tmp matches 2 run scoreboard players set #coef tmp 90
execute if score #step tmp matches 3.. run scoreboard players set #coef tmp 120
function rlk:char/bow/calc
scoreboard players set #pKind tmp 7
scoreboard players set #pEl tmp 8
scoreboard players set #pIcd tmp 1
scoreboard players set #pBig tmp 0
execute if score #step tmp matches 3.. run scoreboard players set #pIcd tmp 0
execute if score #step tmp matches 3.. run scoreboard players set #pBig tmp 1
scoreboard players set #pSub tmp 3
scoreboard players set #pLife tmp 14
# 숄더뷰: 떠 있는 법구에서(보는 방향으로) / 1인칭: 눈앞에서
scoreboard players set #catOn tmp 0
execute unless entity @s[tag=rlk_body] if entity @e[tag=rlk_rncat_c,limit=1] run scoreboard players set #catOn tmp 1
execute if score #catOn tmp matches 1 positioned as @e[tag=rlk_rncat_c,limit=1] rotated as @s run function rlk:char/ronova/proj_spawn
execute if score #catOn tmp matches 1 run function rlk:char/ronova/cat_flash
execute if score #catOn tmp matches 0 if score #step tmp matches 0 anchored eyes positioned ^0.55 ^-0.1 ^0.3 run function rlk:char/ronova/proj_spawn
execute if score #catOn tmp matches 0 if score #step tmp matches 1 anchored eyes positioned ^-0.55 ^-0.1 ^0.3 run function rlk:char/ronova/proj_spawn
execute if score #catOn tmp matches 0 if score #step tmp matches 2 anchored eyes positioned ^ ^0.45 ^0.3 run function rlk:char/ronova/proj_spawn
execute if score #catOn tmp matches 0 if score #step tmp matches 3.. anchored eyes positioned ^ ^-0.15 ^0.5 run function rlk:char/ronova/proj_spawn
execute if score #catOn tmp matches 0 anchored eyes run particle minecraft:dust{color:[0.88,0.12,0.22],scale:0.9} ^ ^-0.15 ^0.6 0.12 0.12 0.12 0 6
# 다음 타까지: #rnNaCd 틱(4타 뒤 #rnNaCd4) / 공격 속도
scoreboard players operation #cd tmp = #rnNaCd tmp
execute if score #step tmp matches 3.. run scoreboard players operation #cd tmp = #rnNaCd4 tmp
scoreboard players operation #cd tmp *= #100 tmp
scoreboard players set #as tmp 100
execute if score @s atkSpeed matches 1.. run scoreboard players operation #as tmp = @s atkSpeed
scoreboard players operation #cd tmp /= #as tmp
execute if score #cd tmp matches ..1 run scoreboard players set #cd tmp 2
scoreboard players operation @s atkCD = #cd tmp
scoreboard players add @s comboStep 1
execute if score @s comboStep matches 4.. run scoreboard players set @s comboStep 0
scoreboard players set @s cboIdle 0
# 소리: 맑은 공명 + 바람 가르는 소리(타마다 음 높이를 조금씩), 4타는 주문 소리 + 반짝임
execute if score #step tmp matches 0 run playsound minecraft:block.amethyst_block.resonate master @a ~ ~ ~ 0.35 1.6
execute if score #step tmp matches 1 run playsound minecraft:block.amethyst_block.resonate master @a ~ ~ ~ 0.35 1.75
execute if score #step tmp matches 2 run playsound minecraft:block.amethyst_block.resonate master @a ~ ~ ~ 0.35 1.9
execute if score #step tmp matches ..2 run playsound minecraft:entity.breeze.shoot master @a ~ ~ ~ 0.25 1.6
execute if score #step tmp matches 3.. run playsound minecraft:entity.evoker.cast_spell master @a ~ ~ ~ 0.4 1.3
execute if score #step tmp matches 3.. run playsound minecraft:block.beacon.power_select master @a ~ ~ ~ 0.3 1.8
execute if score #step tmp matches 3.. run playsound minecraft:entity.breeze.shoot master @a ~ ~ ~ 0.35 1.2
scoreboard players set #basic itv 1
function rlk:items/hook/on_basic_attack
scoreboard players set #basic itv 0
