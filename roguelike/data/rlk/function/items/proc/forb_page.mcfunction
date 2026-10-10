# @s = 스킬 데미지를 받은 몹, at @s. 근처 플레이어가 금단의 도서 보유 시 마도서 페이지 오브 드롭(대상별 최대 3)
execute unless entity @a[tag=player,scores={it_forbidden_book=1..},limit=1] run return 0
scoreboard players add @s fbMark 1
execute store result storage rlk:fp mx double 0.01 run random value -18..18
execute store result storage rlk:fp mz double 0.01 run random value -18..18
function rlk:items/proc/forb_page_spawn with storage rlk:fp
execute unless score #k193 snd matches 1 run function rlk:snd/f208
