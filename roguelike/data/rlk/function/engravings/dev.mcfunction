# 시험용: 각인 개수를 아이템 없이 더한다. 사용: /function rlk:engravings/dev {id:"guard",n:4}   (id = 각인 id — engravings/register 참고, n:0 이면 해제)  ({id:"help",n:0}: 각인 id 목록)
$data modify storage rlk:tmp hq set value "$(id)"
execute if data storage rlk:tmp {hq:"help"} run return run function rlk:engravings/dev_help
$scoreboard players set $(id) engDev $(n)
scoreboard players set @a[tag=player] invDirty 2
$tellraw @s [{"text":"[각인] ","color":"gold","bold":true},{"text":"시험용 개수: $(id) +$(n)","color":"gray","bold":false}]
