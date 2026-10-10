# 원소 소환물 매 틱 (루트 tick 에서 호출)
execute as @e[tag=rlk_core] at @s run function rlk:element/core_tick
execute as @e[tag=rlk_crystal] at @s run function rlk:element/crystal_tick
execute as @e[tag=rlk_lndrift] at @s run function rlk:element/lunar/drift_tick
execute as @e[tag=rlk_dcore] at @s run function rlk:char/nefer/dec_tick
execute as @e[tag=rlk_nfsh_dead] run function rlk:char/nefer/shadow_dead_tick
function rlk:element/core_gc
execute as @e[tag=rlk_core,scores={cF=1..}] run function rlk:element/core_fly
execute as @e[tag=rlk_dcore,scores={cF=1..}] run function rlk:element/core_fly
# 공허 반응: 파편 · 사형 선고 번짐 (캐릭터와 상관없이)
execute as @e[tag=rlk_rnsh] at @s run function rlk:element/void/sh_tick
execute as @e[tag=rlk_rndm] at @s run function rlk:char/ronova/doom_spread
