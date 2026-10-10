# 원소폭발의 실제 발동 (@s = 플레이어, at 몸): 시전 동작(char/cast_burst → char/burst_wind)이 끝난 뒤 불린다
# 스커크는 스킬·폭발의 조건과 재사용 대기가 따로 돈다
execute if score #charN tmp matches 3 run return run function rlk:char/skirk/cast_burst
execute if score @s burstCd matches 1.. run return run function rlk:char/deny {t:"원소폭발 재사용 대기 중"}
execute if score @s energy < #burstCost100 tmp run return run function rlk:char/deny {t:"원소 에너지 부족"}
scoreboard players set @s energy 0
# 숄더뷰: 발동 뒤에도 잠시 조준선을 본다(한 번에 끝나는 폭발도 바로 몸을 돌리지 않게)
scoreboard players operation @s vAimT = #viewAimHold tmp
scoreboard players operation @s burstCd = #burstCdT tmp
execute as @e[tag=rlk_av,limit=1] run swing @s mainhand
execute if score #charN tmp matches 1 run function rlk:char/lumine/burst
execute if score #charN tmp matches 2 run function rlk:char/yoimiya/burst
execute if score #charN tmp matches 4 run function rlk:char/clorinde/burst
execute if score #charN tmp matches 5 if entity @e[tag=rlk_pm_basis,limit=1] rotated as @e[tag=rlk_pm_basis,limit=1] run function rlk:char/arlecchino/burst
execute if score #charN tmp matches 5 unless entity @e[tag=rlk_pm_basis,limit=1] run function rlk:char/arlecchino/burst
execute if score #charN tmp matches 6 run function rlk:char/navia/burst
execute if score #charN tmp matches 7 run function rlk:char/ronova/burst
execute if score #charN tmp matches 8 run function rlk:char/nefer/burst
# 아이템: 원소폭발을 썼을 때
function rlk:items/hook/on_cast_burst
function rlk:combat/on_skill
