# /function rlk:boss/raiden/test/armored: fresh test fight, transformed straight away.
function rlk:boss/raiden/test/start
execute unless score #rdTest rd matches 1 run return 0
execute as @e[tag=rlk_raiden,limit=1] at @s run function rlk:boss/raiden/transform_start
tellraw @s [{text:"[보스 테스트] ",color:"light_purple",bold:true},{text:"바로 악요의 요구우 텐마(갑주 단계)로 변신합니다.",color:"white",bold:false}]
