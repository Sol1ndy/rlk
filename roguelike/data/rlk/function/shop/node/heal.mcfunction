# @s = 플레이어. 회복 구매 (골드는 try_buy 에서 확인함). 체력이 가득하면 사지 않는다
execute if score @s curHealth >= @s maxHealth run return run function rlk:char/deny {t:"체력이 가득 차 있습니다"}
$data modify storage rlk:io hs set from storage rlk:shop heals.$(id)
execute store result score #hp tmp run data get storage rlk:io hs.pct
scoreboard players operation @s gold -= #buyprice tmp
scoreboard players operation #heal tmp = @s maxHealth
scoreboard players operation #heal tmp *= #hp tmp
scoreboard players operation #heal tmp /= #100 tmp
execute if score #heal tmp matches ..0 run scoreboard players set #heal tmp 1
function rlk:player/heal
scoreboard players set #bought tmp 1
execute unless score #k30 snd matches 1 run function rlk:snd/f32
execute unless score #k202 snd matches 1 run function rlk:snd/f221
