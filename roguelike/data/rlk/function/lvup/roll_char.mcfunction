execute store result score #rng tmp run random value 1..100
execute if score #rng tmp > #pkCharPct tmp run return 0
# 후보 = pool 에서 지금 캐릭터를 뺀 것
data modify storage rlk:pick cc set from storage rlk:chars pool
function rlk:lvup/roll_char_ex with storage rlk:chars cur
execute store result score #ccN tmp run data get storage rlk:pick cc
execute if score #ccN tmp matches ..0 run return 0
execute store result score #cck tmp run random value 0..9999
scoreboard players operation #cck tmp %= #ccN tmp
execute store result storage rlk:pick ck int 1 run scoreboard players get #cck tmp
function rlk:lvup/roll_char_get with storage rlk:pick
scoreboard players set #pkChar tmp 1
