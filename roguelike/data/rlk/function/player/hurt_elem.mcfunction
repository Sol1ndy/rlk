# 반응 피해(감전·연소 틱 등)를 플레이어가 직접 받음 (@s = 플레이어, 입력: #dmg, #elem). 방어력 미적용
execute if score @s dashInvT matches 1.. run return 0
scoreboard players operation #dmgIn tmp = #dmg tmp
# 각인 수호: 보호막
function rlk:engravings/guard/absorb
function rlk:element/shield_absorb
execute unless score #dmgIn tmp matches 1.. run return 0
scoreboard players operation @s curHealth -= #dmgIn tmp
execute if score @s curHealth matches ..0 run scoreboard players set @s curHealth 0
scoreboard players operation #hurtDmg tmp = #dmgIn tmp
execute at @e[tag=rlk_body,limit=1] anchored eyes run function rlk:player/hurt_do
