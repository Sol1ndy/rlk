# macro: id. 캐릭터 아이템이면 그 캐릭터로 교체, 아니면 보유 칸(9칸)에 자리가 있을 때 지급(같은 아이템을 여러 개 넣을 수 있다)
$execute if data storage rlk:items registry.$(id).char run return run function rlk:codex/give_char with storage rlk:items registry.$(id)
execute store result score #ol tmp run data get storage rlk:pinv order
execute if score #ol tmp matches 9.. run return run function rlk:char/deny {t:"보유 칸이 가득 찼습니다 (9칸)"}
$function rlk:items/give {id:"$(id)"}
$title @s actionbar [{text:"인벤토리에 추가: ",color:"gray"},{nbt:"registry.$(id).name",storage:"rlk:items",interpret:true,color:"white"}]
scoreboard players set @s hudHold 20
execute unless score #k69 snd matches 1 run function rlk:snd/f74
