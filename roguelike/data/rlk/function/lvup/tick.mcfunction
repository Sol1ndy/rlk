# 레벨 업 아이템 선택 매 틱 (@s = 플레이어)
execute unless score @s pkPending matches 0.. run function rlk:lvup/init
# 웅크림 감지용 통계(sneak_time)는 매 틱 비운다: 1 이상이면 직전 틱에 웅크리고 있었음 (hotbar/tick 이 먼저 읽음)
scoreboard players set @s sneakT 0
# 고를 아이템이 남았다는 안내(화면 아래 subtitle). 다른 제목이 떠 있으면(ttlT) 그쪽이 먼저
scoreboard players reset 아이템선택 stacks
execute if score @s ttlT matches 1.. run scoreboard players remove @s ttlT 1
# F5 위쪽 시점: 웅크리기 키를 누르는 순간 = 아이템 선택 공간 들어가기/돌아오기
scoreboard players set #snk tmp 0
execute if predicate rlk:in_sneak run scoreboard players set #snk tmp 1
# 보스 등장 연출 중(#mbLive 1 · #mbSt 0: 홍련의 등장 건너뛰기 = Shift 길게)에는 누르는 순간을 탭으로 쓰지 않는다(전투 중 거절음 없음).
# 누른 상태(vSnk)는 그대로 기억하므로 연출이 끝날 때까지 누르고 있어도 탭이 되지 않는다. 선택 공간 안에서는 그대로(나가기)
execute if score #snk tmp matches 1 unless score @s vSnk matches 1 if score #mbLive mb matches 1 if score #mbSt mb matches 0 unless score @s pkMode matches 1.. run scoreboard players set @s vSnk 1
# 연출 카메라에 잡혀 있는 동안(mboss/cam/hold, 태그 rlk_mb_camh: 홍련의 컷신, 60 % 컷신 건너뛰기 = Shift 길게)에도 탭으로 쓰지 않는다
execute if score #snk tmp matches 1 unless score @s vSnk matches 1 if entity @s[tag=rlk_mb_camh] unless score @s pkMode matches 1.. run scoreboard players set @s vSnk 1
execute if score #snk tmp matches 1 unless score @s vSnk matches 1 unless score @s dead matches 1 if score @s uiCd matches ..0 run function rlk:lvup/sneak_tap
scoreboard players operation @s vSnk = #snk tmp
function rlk:lvup/pick_sub
execute if score @s pkMode matches 1.. run function rlk:lvup/room_tick
