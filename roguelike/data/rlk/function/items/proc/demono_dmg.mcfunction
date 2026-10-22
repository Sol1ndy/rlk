# @s = 플레이어. 데모노미콘 피해 계산(공격력의 #demonoCoef%, 강화 단계로 조정). 원소는 호출한 마법이 정함(불기둥 = 불, 촉수 = 물, 서리 화살 = 얼음)
scoreboard players operation #dmg tmp = @s atk
scoreboard players operation #dmg tmp *= #demonoCoef tmp
scoreboard players operation #dmg tmp /= #100 tmp
scoreboard players set #crit tmp 0
scoreboard players set #stunHit tmp 0
function rlk:combat/clear_atkflags
scoreboard players set #elU tmp 1000
