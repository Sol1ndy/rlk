# @s = 소유 플레이어(위치는 참격 지점). 키리온 참격 데미지(공격력의 #kirionCoef%, 강화 단계로 조정) + 플래그 정리
scoreboard players operation #dmg tmp = @s atk
scoreboard players operation #dmg tmp *= #kirionCoef tmp
scoreboard players operation #dmg tmp /= #100 tmp
scoreboard players set #crit tmp 0
scoreboard players set #stunHit tmp 0
function rlk:combat/clear_atkflags
# 불 원소 피해 (부착 쿨 적용: 같은 대상에 2.5초마다 또는 3타마다 한 번 부착)
scoreboard players set #elem tmp 1
scoreboard players set #elU tmp 1000
scoreboard players set #icd tmp 1
