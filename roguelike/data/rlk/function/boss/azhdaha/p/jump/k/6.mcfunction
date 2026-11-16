# jump #azPT 6
function rlk:boss/azhdaha/fx/snd/jump_takeoff
function rlk:boss/azhdaha/px/jump
scoreboard players set #azLeap mb 1
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p2l,limit=1] run function rlk:mboss/mv/leap {t:15,h:30}
scoreboard players set #azNoPush mb 1
