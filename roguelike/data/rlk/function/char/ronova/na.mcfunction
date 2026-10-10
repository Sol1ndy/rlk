# 일반 공격 붉은 시선 (@s = 플레이어, at 몸): 붉은 눈 구체 4타(72% / 66% / 90% / 120%, 조준한 적만 추적). 공허 원소, 4타는 부착 쿨 없이 공허를 묻힌다
execute store result score #now tmp run time query gametime
execute if score @s swungAt = #now tmp run return 0
scoreboard players operation @s swungAt = #now tmp
# 클릭 순간 실제 카메라의 눈·시선으로 목표를 갱신한다(지난 틱의 아바타 회전을 쓰지 않음).
function rlk:char/ronova/na_aim
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
# 숄더뷰: 법구에서 / 1인칭: 눈앞에서. 각 발사점에서 동일한 조준 지점을 바라본다.
scoreboard players set #catOn tmp 0
execute unless entity @s[tag=rlk_body] if entity @e[tag=rlk_rncat_c,limit=1] run scoreboard players set #catOn tmp 1
execute if score #catOn tmp matches 1 positioned as @e[tag=rlk_rncat_c,limit=1] rotated as @s run function rlk:char/ronova/proj_spawn
execute if score #catOn tmp matches 1 run function rlk:char/ronova/cat_flash
execute if score #catOn tmp matches 0 if score #step tmp matches 0 at @e[tag=rlk_body,limit=1] anchored eyes positioned ^ ^ ^ anchored feet positioned ^0.55 ^-0.1 ^0.3 run function rlk:char/ronova/proj_spawn
execute if score #catOn tmp matches 0 if score #step tmp matches 1 at @e[tag=rlk_body,limit=1] anchored eyes positioned ^ ^ ^ anchored feet positioned ^-0.55 ^-0.1 ^0.3 run function rlk:char/ronova/proj_spawn
execute if score #catOn tmp matches 0 if score #step tmp matches 2 at @e[tag=rlk_body,limit=1] anchored eyes positioned ^ ^ ^ anchored feet positioned ^ ^0.45 ^0.3 run function rlk:char/ronova/proj_spawn
execute if score #catOn tmp matches 0 if score #step tmp matches 3.. at @e[tag=rlk_body,limit=1] anchored eyes positioned ^ ^ ^ anchored feet positioned ^ ^-0.15 ^0.5 run function rlk:char/ronova/proj_spawn
kill @e[tag=rlk_rn_aim]
execute if score #catOn tmp matches 0 positioned ~ ~1.62 ~ run particle minecraft:dust{color:[0.88,0.12,0.22],scale:0.9} ^ ^-0.15 ^0.6 0.12 0.12 0.12 0 6
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
execute if score #step tmp matches 0 unless score #k42 snd matches 1 run function rlk:snd/f298
execute if score #step tmp matches 1 unless score #k266 snd matches 1 run function rlk:snd/f299
execute if score #step tmp matches 2 unless score #k267 snd matches 1 run function rlk:snd/f300
execute if score #step tmp matches ..2 unless score #k268 snd matches 1 run function rlk:snd/f301
execute if score #step tmp matches 3.. unless score #k269 snd matches 1 run function rlk:snd/f302
execute if score #step tmp matches 3.. unless score #k270 snd matches 1 run function rlk:snd/f303
execute if score #step tmp matches 3.. unless score #k271 snd matches 1 run function rlk:snd/f304
scoreboard players set #basic itv 1
function rlk:items/hook/on_basic_attack
scoreboard players set #basic itv 0
