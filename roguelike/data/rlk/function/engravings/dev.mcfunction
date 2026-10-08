# 시험용: 각인 개수를 아이템 없이 더한다. 사용: /function rlk:engravings/dev {id:"guard",n:4}   (id = 각인 id — engravings/register 참고, n:0 이면 해제)
$scoreboard players set $(id) engDev $(n)
scoreboard players set @a[tag=player] invDirty 2
$tellraw @s [{"text":"[각인] ","color":"gold","bold":true},{"text":"시험용 개수: $(id) +$(n)","color":"gray","bold":false}]
