# 원소폭발 버튼 (@s = 플레이어, at 몸): 쓸 수 있는지 확인 → 시전 동작(멈춤·무적·화면 확대) → 끝나면 char/burst_go 가 실제로 발동
execute if score @s buT matches 1.. run return 0
execute if score @s dead matches 1 run return 0
# 스커크: 일곱빛 섬광 중의 극악기·진은 바로 발동(짧은 강화 시간을 깎지 않게)
execute if score #charN tmp matches 3 if score @s skBurst matches 1.. run return 0
execute if score @s burstCd matches 1.. run return run function rlk:char/deny {t:"원소폭발 재사용 대기 중"}
execute if score #charN tmp matches 3 if score @s skM matches 1.. run return run function rlk:char/burst_go
execute if score #charN tmp matches 3 if score @s energy < #skBurstMin tmp run return run function rlk:char/deny {t:"뱀의 계략 부족 (50pt 필요)"}
execute unless score #charN tmp matches 3 if score @s energy < #burstCost100 tmp run return run function rlk:char/deny {t:"원소 에너지 부족"}
function rlk:char/burst_wind
