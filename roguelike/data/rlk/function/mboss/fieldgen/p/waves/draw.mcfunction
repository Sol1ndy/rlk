# @s = a live front, at it: its current rim as dust points (the framework circle primitive of radius k / 2).
scoreboard players operation #fq21K mb = @s mbHzR
scoreboard players add #fq21K mb 250
scoreboard players operation #fq21K mb /= #c500 mb
execute if score #fq21K mb matches ..0 run scoreboard players set #fq21K mb 1
execute if score #fq21K mb matches 61.. run scoreboard players set #fq21K mb 60
execute store result storage rlk:mboss fg.wv.k int 1 run scoreboard players get #fq21K mb
scoreboard players set #hzAng mb 180
function rlk:mboss/fieldgen/p/waves/draw_m with storage rlk:mboss fg.wv
