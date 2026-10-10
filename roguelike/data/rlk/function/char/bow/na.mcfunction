# 활 기본 공격 (@s = 플레이어, at 몸). 틱당 한 번만
execute store result score #now tmp run time query gametime
execute if score @s swungAt = #now tmp run return 0
scoreboard players operation @s swungAt = #now tmp
# 당기는 중에는 기본 공격을 하지 않는다
execute if score @s bowT matches 1.. run return 0
execute as @e[tag=rlk_av,limit=1] run swing @s mainhand
# 이번 타의 계수(#bCoef) · 화살 수(#bN) · 콤보 길이(#bSteps): 캐릭터가 정한다
scoreboard players operation #step tmp = @s comboStep
scoreboard players set #bCoef tmp 100
scoreboard players set #bN tmp 1
scoreboard players set #bSteps tmp 1
scoreboard players set #bOff tmp 0
scoreboard players set #bOff2 tmp 0
scoreboard players set #bFin tmp 0
execute if score #charN tmp matches 2 run function rlk:char/yoimiya/na_coef
execute if score #charN tmp matches 2 run function rlk:char/yoimiya/na_fx
# 다음 타까지: #bowCdN / 공격 속도
scoreboard players operation #cd tmp = #bowCdN tmp
scoreboard players set #as tmp 100
execute if score @s atkSpeed matches 1.. run scoreboard players operation #as tmp = @s atkSpeed
scoreboard players operation #cd tmp /= #as tmp
execute if score #cd tmp matches ..1 run scoreboard players set #cd tmp 2
scoreboard players operation @s atkCD = #cd tmp
scoreboard players add @s comboStep 1
execute if score @s comboStep >= #bSteps tmp run scoreboard players set @s comboStep 0
scoreboard players set @s cboIdle 0
# 발사 (두 발짜리 타는 두 번째 화살을 #bowQGap 틱 뒤에)
function rlk:char/bow/na_shot
execute if score #bN tmp matches 2.. run scoreboard players operation @s bowQ = #bowQGap tmp
execute if score #bN tmp matches 2.. run scoreboard players operation @s bowQc = #bCoef tmp
execute if score #bN tmp matches 2.. run scoreboard players operation @s bowQo = #bOff2 tmp
# 각인 연격 4개: 2타에 추가 화살 한 발(공격력의 #flurryCoef%)
execute if score #step tmp matches 1 if score flurry engN matches 4.. run scoreboard players set @s bowF 5
execute unless score #k231 snd matches 1 run function rlk:snd/f258
# 기본공격 시 발동(적중 여부 무관)
scoreboard players set #basic itv 1
function rlk:items/hook/on_basic_attack
scoreboard players set #basic itv 0
