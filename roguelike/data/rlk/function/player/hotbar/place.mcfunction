# 핫바 유지 (@s). 0번 = 기본공격(무기), 1번 = 원소전투 스킬, 2번 = 원소폭발, 3~8번 = 빈칸. 올바른 아이템이 아닐 때만 교체
# 아이템 선택 공간: 핫바를 비운다
execute if score @s pkMode matches 1.. run return run function rlk:player/hotbar/blank
# 돌아옴: 빈 아이템을 모두 치운다(아래에서 원래 핫바를 다시 만든다)
execute if items entity @s container.* *[minecraft:custom_data~{rlk_ui:{role:"blank"}}] run clear @s *[minecraft:custom_data~{rlk_ui:{role:"blank"}}]
execute if items entity @s player.cursor *[minecraft:custom_data~{rlk_ui:{role:"blank"}}] run item replace entity @s player.cursor with air
execute unless items entity @s hotbar.0 *[minecraft:custom_data~{rlk_ui:{role:"attack"}}] run function rlk:player/hotbar/fix_attack
function rlk:char/hotbar

# 예전 판의 채움칸(방벽)이 남아 있으면 지움
execute if items entity @s container.* minecraft:barrier[minecraft:custom_data~{rlk_ui:{}}] run clear @s minecraft:barrier[minecraft:custom_data~{rlk_ui:{}}]