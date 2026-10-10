# 커스텀 몹 두뇌 (@s, at @s)
scoreboard players operation #cid tmp = @s cmId
scoreboard players operation #clv tmp = @s mlv
# 쿨타임은 경직 중에도 흐른다
execute if score @s cmCd matches 1.. run scoreboard players remove @s cmCd 1
execute if score @s cmCd2 matches 1.. run scoreboard players remove @s cmCd2 1
scoreboard players set #free tmp 1
execute if score @s stunT matches 1.. run scoreboard players set #free tmp 0
execute if score @s frzT matches 1.. run scoreboard players set #free tmp 0
scoreboard players set #hold tmp 0
# 빙결: 차지·선딜·조준 모두 초기화(모은 화염구 · 궤적 선 · 숨긴 포탄과 떨어질 자리 표시도 지움)
execute if score @s frzT matches 1.. if score @s cmS matches 1.. run function rlk:cm/cancel
execute if score #cmDown tmp matches 1 run function rlk:cm/down
execute if score #cmDown tmp matches 0 run function rlk:cm/aggro
execute if score #cmDown tmp matches 0 if entity @s[tag=rlk_cm_sw] run function rlk:cm/sw/tick
execute if score #cmDown tmp matches 0 if entity @s[tag=rlk_cm_ar] run function rlk:cm/ar/tick
execute if score #cmDown tmp matches 0 if entity @s[tag=rlk_cm_fm] run function rlk:cm/fm/tick
execute if score #cmDown tmp matches 0 if entity @s[tag=rlk_cm_im] run function rlk:cm/im/tick
execute if score #cmDown tmp matches 0 if entity @s[tag=rlk_cm_sh] run function rlk:cm/sh/tick
execute if score #cmDown tmp matches 0 if entity @s[tag=rlk_cm_cn] run function rlk:cm/cn/tick
# 이동 멈춤(사거리 안 · 차지 중): 넉백은 그대로 받는다
execute if entity @s[tag=rlk_cmch] run scoreboard players set #hold tmp 1
execute if score #hold tmp matches 1 unless entity @s[tag=rlk_cmhold] run function rlk:cm/hold_on
execute if score #hold tmp matches 0 if entity @s[tag=rlk_cmhold] run function rlk:cm/hold_off
function rlk:cm/vis
