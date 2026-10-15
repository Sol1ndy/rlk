# 각인 카드를 고름 (@s = 플레이어): 기적(rlk:pinv mir = 각인 id, 개수 +1) + 그 각인이 달린 아이템 하나 + 나무뿌리 제거 + 나가기
execute if score #mirUsed room matches 1.. run return run function rlk:lvup/exit
execute store result storage rlk:lvpick a.h int 1 run scoreboard players get @s pkHI
function rlk:root/take2 with storage rlk:lvpick a
execute unless data storage rlk:pinv mir run return 0
scoreboard players set #mirUsed room 1
function rlk:root/give with storage rlk:pinv
scoreboard players set @s invDirty 2
execute as @e[tag=rlk_obj,scores={oact=6}] if score @s ogid = #rootG room run function rlk:room/obj/kill_group
function rlk:root/msg with storage rlk:pinv
execute unless score #k73 snd matches 1 run function rlk:snd/f78
function rlk:lvup/exit
