# 월광 (@s = 플레이어): #cgMoonDur 동안 달 반응 피해 +#cgMoon%
scoreboard players operation #cgMoonT itv = #cgMoonDur tmp
execute at @e[tag=rlk_body,limit=1] run particle minecraft:end_rod ~ ~2 ~ 1 1 1 0.05 30
playsound minecraft:block.beacon.activate master @a ~ ~ ~ 0.6 1.6
