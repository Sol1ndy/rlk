# 떠오르는 재액의 달 (@s = 플레이어, at 몸): 모든 핏값을 회수 → 보는 방향 앞쪽(4칸 앞을 중심으로 반경 5칸 + 발동 자리 반경 2.5칸)에 공격력의 370% 불 원소 피해 → 생명의 계약을 해소하고 회복 → 스킬 재사용 대기 초기화
execute store result score #ynow tmp run time query gametime
execute as @e[tag=rlk_mob] if score @s arDir > #ynow tmp run function rlk:char/arlecchino/dir_take
function rlk:char/dmg_calc {coef:370}
function rlk:items/hook/burst_dmg
scoreboard players set #elem tmp 1
scoreboard players set #elU tmp 1000
tag @e[tag=rlk_mob,distance=..2.5] add rlk_hit
execute rotated ~ 0 positioned ^ ^ ^4 run tag @e[tag=rlk_mob,distance=..5] add rlk_hit
scoreboard players operation #dmgBase tmp = #dmg tmp
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
tag @e[tag=rlk_hit] remove rlk_hit
function rlk:char/after_hit
# 해소 + 회복: 해소한 생명의 계약의 #arHealBol% + 공격력의 #arHealAtk%
function rlk:player/bol/clear
scoreboard players operation #heal tmp = #bolWas tmp
scoreboard players operation #heal tmp *= #arHealBol tmp
scoreboard players operation #heal tmp /= #100 tmp
scoreboard players operation #t1 tmp = @s atk
scoreboard players operation #t1 tmp *= #arHealAtk tmp
scoreboard players operation #t1 tmp /= #100 tmp
scoreboard players operation #heal tmp += #t1 tmp
function rlk:player/heal
scoreboard players set @s skillCd 0
