# 레벨 업 아이템 선택 매 틱 (@s = 플레이어)
execute unless score @s pkPending matches 0.. run function rlk:lvup/init
# 웅크림 감지용 통계(sneak_time)는 매 틱 비운다: 1 이상이면 직전 틱에 웅크리고 있었음 (hotbar/tick 이 먼저 읽음)
scoreboard players set @s sneakT 0
# 고를 아이템이 남았다는 안내(화면 아래 subtitle). 다른 제목이 떠 있으면(ttlT) 그쪽이 먼저
scoreboard players reset 아이템선택 stacks
execute if score @s ttlT matches 1.. run scoreboard players remove @s ttlT 1
function rlk:lvup/pick_sub
execute if score @s pkMode matches 1.. run function rlk:lvup/room_tick
