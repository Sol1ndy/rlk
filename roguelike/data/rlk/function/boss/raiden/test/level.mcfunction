# /function rlk:boss/raiden/test/level {lv:N}: set the boss level and refill its scaled HP.
$scoreboard players set #rdReq rd $(lv)
execute unless score #rdReq rd matches 1..999 run return run tellraw @s [{text:"[보스 테스트] ",color:"light_purple",bold:true},{text:"레벨은 1 이상이어야 합니다.",color:"red",bold:false}]
execute unless entity @e[tag=rlk_raiden,scores={rdDeath=0},limit=1] run function rlk:boss/raiden/test/start
execute unless entity @e[tag=rlk_raiden,scores={rdDeath=0},limit=1] run return 0
execute as @e[tag=rlk_raiden,limit=1] run scoreboard players operation @s mlv = #rdReq rd
execute as @e[tag=rlk_raiden,limit=1] run function rlk:mob/level_apply
tellraw @s [{text:"[보스 테스트] ",color:"light_purple",bold:true},{text:"보스 레벨 ",color:"gray",bold:false},{score:{name:"#rdReq",objective:"rd"},color:"yellow",bold:false},{text:" · 체력을 다시 채웠습니다.",color:"gray",bold:false}]
