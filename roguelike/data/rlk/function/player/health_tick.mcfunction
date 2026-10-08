# 체력 처리 (@s = 플레이어, 매 틱). 실제 체력은 curHealth / maxHealth 스코어이고 액션바에 표시한다
# 바닐라 체력은 1024(상한)으로 고정해 두고 "맞았는지 감지"하는 데만 쓴다: 깎인 양(하트 반 칸 = 1) × #mobDmgMul = 받은 원피해
# → 한 방에 바닐라 피해 1024 이상이 아니면 바닐라에서 즉사하지 않음
# 이전 버전(바닐라 체력 20)에서 넘어온 플레이어: 늘리고 채운 뒤 이번 틱은 감지 생략
execute unless score @s vhp matches 1024 run return run function rlk:player/vhp_fix
execute store result score #h100 tmp run data get entity @s Health 100
# 죽어 있는 동안은 아무것도 하지 않음. 부활하면 체력을 채움(이번 틱은 감지 생략)
execute if score #h100 tmp matches ..0 run return run scoreboard players set @s dead 1
execute if score @s dead matches 1 run return run function rlk:player/on_respawn
execute if score #h100 tmp < #vhp100 tmp run function rlk:player/vanilla_hit
execute if score @s curHealth > @s maxHealth run scoreboard players operation @s curHealth = @s maxHealth
execute if score @s curHealth matches ..0 run function rlk:player/die
