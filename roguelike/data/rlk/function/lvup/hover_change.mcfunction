# 조준 대상이 바뀜 (@s = 플레이어): 강조 표시 · 설명 창 · 각인 창 갱신
scoreboard players operation @s pkHK = #pkK tmp
scoreboard players operation @s pkHI = #pkI tmp
execute as @e[tag=rlk_pk_hl] run function rlk:lvup/ui/hl_off
execute if score @s pkHK matches 1.. as @e[tag=rlk_pk_d] if score @s pkKind = #pkK tmp if score @s pkIdx = #pkI tmp run function rlk:lvup/ui/hl_on
execute if score @s pkHK matches 1.. run playsound minecraft:block.note_block.hat master @s ~ ~ ~ 0.5 1.9
function rlk:lvup/tip/update
function rlk:lvup/eng/refresh
