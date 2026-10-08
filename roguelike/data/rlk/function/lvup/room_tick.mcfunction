# 선택 공간 안 (@s = 플레이어, 매 틱)
# 왼손의 지도는 치워 둔다
execute if items entity @s weapon.offhand minecraft:filled_map[minecraft:custom_data~{rlk_map:1b}] run item replace entity @s weapon.offhand with air
# 자리를 벗어났으면(사망·강제 이동 등) 정리만 하고 끝
execute in minecraft:overworld positioned 104.5 195 4.5 unless entity @s[distance=..2.5] run return run function rlk:lvup/cleanup
execute if score @s pkCd matches 1.. run scoreboard players remove @s pkCd 1
execute if score @s pkRedraw matches 1.. run function rlk:lvup/redraw_wait
# 조준: 눈에서 시선 방향으로 레이 → 가장 먼저 닿는 UI 요소
scoreboard players set #pkK tmp 0
scoreboard players set #pkI tmp 0
scoreboard players set #pkRay tmp 0
execute at @s anchored eyes positioned ^ ^ ^0.01 anchored feet run function rlk:lvup/ray
# 지금 모드에서 누를 수 없는 요소는 무시
function rlk:lvup/hover_filter
execute unless score #pkK tmp = @s pkHK run function rlk:lvup/hover_change
execute if score #pkK tmp = @s pkHK unless score #pkI tmp = @s pkHI run function rlk:lvup/hover_change
# 설명 창은 조준점 옆을 따라다님 (인벤 아이템을 볼 때는 왼쪽, 그 밖에는 오른쪽: 각인 창을 가리지 않게)
execute unless score @s pkHK matches 2 at @s anchored eyes positioned ^-1.6 ^ ^3 run tp @e[tag=rlk_pk_tip] ~ ~ ~
execute if score @s pkHK matches 2 at @s anchored eyes positioned ^1.6 ^ ^3 run tp @e[tag=rlk_pk_tip] ~ ~ ~
# 인벤토리 상세: 한 줄의 왼쪽 절반을 볼 때는 설명 창을 오른쪽에
execute if score @s pkMode matches 4 if score @s pkHK matches 2 if score @s pkHI matches ..4 at @s anchored eyes positioned ^-1.6 ^ ^3 run tp @e[tag=rlk_pk_tip] ~ ~ ~
# 인벤토리 상세: 각인 설명 창은 아이템 설명 창의 반대쪽
execute if score @s pkMode matches 4 if score @s pkHI matches ..4 at @s anchored eyes positioned ^1.6 ^ ^3 run tp @e[tag=rlk_pk_tip2] ~ ~ ~
execute if score @s pkMode matches 4 if score @s pkHI matches 5.. at @s anchored eyes positioned ^-1.6 ^ ^3 run tp @e[tag=rlk_pk_tip2] ~ ~ ~
# 아이템 도감: 설명 창은 조준한 칸의 반대쪽, 각인 설명 창은 같은 쪽 아래
execute if score @s pkMode matches 6 run function rlk:codex/tip_pos
