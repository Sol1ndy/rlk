# 원소 소환물 매 틱 (루트 tick 에서 호출)
execute as @e[tag=rlk_core] at @s run function rlk:element/core_tick
execute as @e[tag=rlk_crystal] at @s run function rlk:element/crystal_tick
execute as @e[tag=rlk_lndrift] at @s run function rlk:element/lunar/drift_tick
execute as @e[tag=rlk_dcore] at @s run function rlk:char/nefer/dec_tick
execute as @e[tag=rlk_nfsh_dead] run function rlk:char/nefer/shadow_dead_tick
function rlk:element/core_gc
