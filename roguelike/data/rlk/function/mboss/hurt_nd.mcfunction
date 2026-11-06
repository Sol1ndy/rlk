# @s = player: one hit that dash i-frames cannot dodge (dashInvT is 0 during the call, then restored).
execute store result score #mbDI mb run scoreboard players get @s dashInvT
scoreboard players set @s dashInvT 0
function rlk:cm/hit_pl2
scoreboard players operation @s dashInvT = #mbDI mb
