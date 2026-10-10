execute if score @s pmMoveLock matches 1 run return 0
# 원소전투 스킬 발동 (@s = 플레이어, at @s)
# 스커크는 스킬·폭발의 조건과 재사용 대기가 따로 돈다
execute if score #charN tmp matches 3 run return run function rlk:char/skirk/cast_skill
execute if score #charN tmp matches 4 run return run function rlk:char/clorinde/cast_skill
execute if score #charN tmp matches 6 run return run function rlk:char/navia/cast_skill
execute if score #charN tmp matches 7 run return run function rlk:char/ronova/cast_skill
execute if score #charN tmp matches 8 run return run function rlk:char/nefer/cast_skill
execute if score @s skillCd matches 1.. run return run function rlk:char/deny {t:"원소전투 스킬 재사용 대기 중"}
scoreboard players operation @s skillCd = #skillCdT tmp
# 모래시계 조각: 재사용 대기 감소(개수만큼)
execute if score @s it_hourglass_shard matches 1.. run function rlk:items/proc/hourglass
# 각인 순환 2개: 재사용 대기 감소
execute if score cycle engN matches 2.. run function rlk:engravings/cycle/cd
execute as @e[tag=rlk_av,limit=1] run swing @s mainhand
execute if score #charN tmp matches 1 run function rlk:char/lumine/skill
execute if score #charN tmp matches 2 run function rlk:char/yoimiya/skill
execute if score #charN tmp matches 5 run function rlk:char/arlecchino/skill
# 아이템: 원소전투 스킬을 썼을 때
function rlk:items/hook/on_cast_skill
function rlk:combat/on_skill
