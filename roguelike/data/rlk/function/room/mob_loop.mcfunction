execute if score #mobN tmp matches ..0 run return 0
scoreboard players set #try tmp 0
function rlk:room/mob_try
scoreboard players remove #mobN tmp 1
function rlk:room/mob_loop
