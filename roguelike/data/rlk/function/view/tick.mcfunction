execute if score @s rdCam matches 1 run return run function rlk:boss/raiden/camera/hold
# 시점 시스템 매 틱 (@s = 플레이어). player/tick 보다 먼저 실행된다
# 지도 클릭 잠금/길게 누름 판정
execute if score @s vMapH matches 1.. run scoreboard players remove @s vMapH 1
execute if score @s vMapL matches 1.. run scoreboard players remove @s vMapL 1
execute if score @s vMapR matches 1.. run scoreboard players remove @s vMapR 1
# G 메뉴(빠른 동작 대화창)의 버튼
scoreboard players enable @s rlkMenu
execute if score @s rlkMenu matches 1.. run function rlk:view/menu_do
function rlk:view/burst_camera_tick
execute if score @s vMap matches 1 run return run function rlk:view/map_tick
# 실제 적용: 켜져 있고(#on) 개발자 모드가 아닐 때
scoreboard players set #eff view 0
execute if score #on view matches 1 unless score @s devMode matches 1 run scoreboard players set #eff view 1
execute if score #eff view matches 0 run return run function rlk:view/fps_tick
# 죽어 있는 동안 / 아이템 선택 공간에 있는 동안은 쉰다(아바타는 그 자리에 남음)
execute if score @s dead matches 1 run return run function rlk:view/hold
execute if score @s pkMode matches 1.. run return run function rlk:view/hold
execute unless entity @e[tag=rlk_av,limit=1] at @s run function rlk:view/spawn
tag @s remove rlk_body
# 아바타 클릭 실드: 없으면 만들고, 아바타 자리로 옮기고, 이번 틱에도 주인이 있다고 표시(표시가 없으면 combat/mshield_tick 이 지움)
execute unless score #bowChg tmp matches 1 unless entity @e[tag=rlk_avsh,limit=1] at @e[tag=rlk_av,limit=1] run summon minecraft:interaction ~ ~ ~ {Tags:["rlk_view","rlk_mshield","rlk_avsh"],width:1.3f,height:2.2f,response:false}
execute unless score #bowChg tmp matches 1 at @e[tag=rlk_av,limit=1] run tp @e[tag=rlk_avsh,limit=1] ~ ~-0.1 ~
execute unless score #bowChg tmp matches 1 run tag @e[tag=rlk_avsh] add rlk_msync
# 지난 틱에 생긴 몹이 아바타를 노리게
execute as @e[tag=rlk_agq] run function rlk:view/mob_aggro
# 입력 → 아바타 이동 / 아바타가 맞았는지 / 조준점 / 카메라
function rlk:view/move
execute unless score #sprNow view = #spr view run function rlk:view/sprint_fov
execute as @e[tag=rlk_av,limit=1] run function rlk:view/av_tick
function rlk:view/aim
scoreboard players set #ci view 0
execute if score #vmode view matches 2 run function rlk:view/ride_tick
execute unless score #vmode view matches 2 run function rlk:view/rot
# 2초마다: 투명 유지 · 손에 든 무기 맞춤 · 멈춰 선 몹의 어그로 다시 끌기 · 여분 아바타 정리
scoreboard players add #t view 1
execute if score #t view matches 40.. run function rlk:view/slow
