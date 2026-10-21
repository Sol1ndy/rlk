# Undodgeable (돌진, 수천수만의 염원, guard recovery): dash i-frames are 0 for this one hit, then restored.
execute as @a[tag=player,limit=1] store result score #rdDI rd run scoreboard players get @s dashInvT
scoreboard players set @a[tag=player,limit=1] dashInvT 0
scoreboard players set #rdNoDodge rd 1
function rlk:boss/raiden/hurt
scoreboard players set #rdNoDodge rd 0
scoreboard players operation @a[tag=player,limit=1] dashInvT = #rdDI rd
