# 기본공격 범위 루프용: 대상마다 데미지를 기본값으로 복원 후 apply (@s = 몹)
scoreboard players operation #dmg tmp = #dmgBase tmp
function rlk:combat/apply
