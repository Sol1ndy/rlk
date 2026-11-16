# 보유 아이템 pkHI 를 한 단계 강화 (@s = 플레이어). 이미 ★★★ 이면 거절
execute if score #enchN room matches ..0 run return run function rlk:lvup/exit
execute store result storage rlk:lvpick a.h int 1 run scoreboard players get @s pkHI
data remove storage rlk:lvpick b.id
function rlk:ench/pick2 with storage rlk:lvpick a
execute unless data storage rlk:lvpick b.id run return 0
scoreboard players set #enh tmp 0
function rlk:items/enh_get with storage rlk:lvpick b
execute if score #enh tmp matches 3.. run return run function rlk:char/deny {t:"이미 최대로 강화되었습니다 (★★★)"}
function rlk:items/enh_add with storage rlk:lvpick b
# 남은 횟수 -1 (인챈트대의 oarg 도 같이)
scoreboard players remove #enchN room 1
execute as @e[tag=rlk_obj,scores={oact=5}] if score @s ogid = #enchG room run scoreboard players operation @s oarg = #enchN room
execute store result storage rlk:room a.n int 1 run scoreboard players get #enchN room
execute as @e[tag=rlk_olbl] if score @s ogid = #enchG room run function rlk:ench/label with storage rlk:room a
scoreboard players set @s invDirty 2
execute unless score #k350 snd matches 1 run function rlk:snd/f417
execute unless score #k2 snd matches 1 run function rlk:snd/f415
function rlk:ench/msg with storage rlk:lvpick b
# 다 썼으면 인챈트대를 없애고 나간다
execute if score #enchN room matches ..0 as @e[tag=rlk_obj,scores={oact=5}] if score @s ogid = #enchG room run function rlk:room/obj/kill_group
execute if score #enchN room matches ..0 run return run function rlk:lvup/exit
scoreboard players set @s pkRedraw 1
