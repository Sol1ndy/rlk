# @s = 플레이어. 이번 닷지의 첫 퍼펙트 닷지: 원소 에너지 +#dgEn(고정량; 스커크는 일곱빛 섬광 밖에서 뱀의 계략으로), 효과, 아이템 신호
scoreboard players operation @s dgRw = @s dgAt
execute unless score #skMode tmp matches 1 run scoreboard players operation @s energy += #dgEn tmp
execute if score @s energy > #burstCost100 tmp run scoreboard players operation @s energy = #burstCost100 tmp
function rlk:player/def/fx/pd
function rlk:items/hook/on_pdodge
