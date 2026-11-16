# 박자를 비운다(load: /reload 뒤 아무것도 멈춘 채 남지 않게; 시험). 멈춘 틱 수 #btLag 는 전투 시계의 일부라 지우지 않는다
function rlk:player/def/beat/end
# 접속한 플레이어가 없을 때 남은 대역 리그(마네킹 캐릭터의 박자 동작)도 치운다
execute unless entity @a[tag=player,scores={plActive=1},limit=1] run kill @e[tag=rlk_pl]
execute unless entity @a[tag=player,scores={plActive=1},limit=1] run kill @e[tag=rlk_pl_basis]
execute unless score #btLag cb matches -2147483648.. run scoreboard players set #btLag cb 0
scoreboard players operation #btAdj cb = #btLag cb
