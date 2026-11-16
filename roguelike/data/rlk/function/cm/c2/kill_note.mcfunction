# 2챕터 몹 처치 기록 (@s = 죽는 두뇌, combat/apply 에서). 10틱 안에 3마리 → 다중 처치 신호. 큰 슬라임은 분열할 레벨을 리그에 남김
execute store result score #c2Now tmp run time query gametime
execute if entity @s[tag=rlk_cm_sl] run function rlk:cm/sl/keep_lv
scoreboard players operation #c2Dt tmp = #c2Now tmp
scoreboard players operation #c2Dt tmp -= #c2K2 tmp
scoreboard players operation #c2K2 tmp = #c2K1 tmp
scoreboard players operation #c2K1 tmp = #c2Now tmp
execute if score #c2Dt tmp matches ..10 run function rlk:cm/c2/multi
