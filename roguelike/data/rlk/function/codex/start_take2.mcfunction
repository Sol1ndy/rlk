$execute if data storage rlk:items registry.$(id).char run return 0
$function rlk:items/give {id:"$(id)"}
$title @s actionbar [{text:"시작 아이템: ",color:"gray"},{nbt:"registry.$(id).name",storage:"rlk:items",interpret:true,color:"white"}]
scoreboard players set @s hudHold 30
execute unless score #k70 snd matches 1 run function rlk:snd/f75
scoreboard players remove #stPick room 1
execute if score #stPick room matches ..0 run return run function rlk:lvup/exit
scoreboard players set @s pkRedraw 1
