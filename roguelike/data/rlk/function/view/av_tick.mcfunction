# 아바타가 맞았는지 (@s = 아바타, 매 틱). 깎인 바닐라 체력 × #mobDmgMul = 원피해 → 플레이어의 피격 처리로 넘기고 체력은 다시 채움
execute store result score #ah view run data get entity @s Health 100
execute if score #ah view >= #vhp100 tmp run return 0
data modify entity @s Health set value 1024f
# 때린 것이 진짜 플레이어(카메라가 벽에 밀려 아바타에 바짝 붙었을 때 좌클릭이 아바타에 닿음)면 없던 일로: 피해 없음, 넉백 취소
scoreboard players set #pa view 0
execute on attacker if entity @s[type=minecraft:player] run scoreboard players set #pa view 1
execute if score #pa view matches 1 run data modify entity @s Motion[0] set value 0.0d
execute if score #pa view matches 1 run data modify entity @s Motion[2] set value 0.0d
execute if score #pa view matches 1 run return 0
scoreboard players operation #dmgIn tmp = #vhp100 tmp
scoreboard players operation #dmgIn tmp -= #ah view
scoreboard players operation #dmgIn tmp *= #mobDmgMul tmp
scoreboard players operation #dmgIn tmp /= #100 tmp
execute if score #dmgIn tmp matches ..0 run scoreboard players set #dmgIn tmp 1
# 때린 몹의 원소·레벨
scoreboard players set #e tmp 0
scoreboard players set #alv tmp 0
execute on attacker run function rlk:element/read_tag
execute on attacker run scoreboard players operation #alv tmp = @s mlv
execute as @a[tag=player,limit=1] run function rlk:view/av_hurt
