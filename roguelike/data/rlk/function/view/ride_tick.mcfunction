# F5 위쪽 시점 (@s = 플레이어)
# 받침: 아바타 머리 위에 탄 작은 투명 갑옷 거치대. 카메라 거리 속성은 받침의 것이 쓰인다(탈것 기준)
execute unless entity @e[tag=rlk_vseat,limit=1] at @e[tag=rlk_av,limit=1] run function rlk:view/seat_new
scoreboard players set #sr view 0
execute as @e[tag=rlk_vseat,limit=1] on vehicle if entity @s[tag=rlk_av] run scoreboard players set #sr view 1
execute if score #sr view matches 0 run ride @e[tag=rlk_vseat,limit=1] mount @e[tag=rlk_av,limit=1]
# 플레이어는 받침에. 웅크리면 바닐라가 내려 버리므로, 웅크린 동안은 받침 자리로 직접 옮긴다
scoreboard players set #pr view 0
execute on vehicle if entity @s[tag=rlk_vseat] run scoreboard players set #pr view 1
execute if score #pr view matches 0 if predicate rlk:in_sneak at @e[tag=rlk_vseat,limit=1] run tp @s ~ ~0.99 ~
execute if score #pr view matches 0 unless predicate rlk:in_sneak run function rlk:view/ride_mount
# 조준점 표시(화면 가운데). 큰 제목(vBig)이 떠 있는 동안은 쉰다
execute if score @s vBig matches 1.. run scoreboard players remove @s vBig 1
# 아랫줄 안내(ttlT)가 끝나는 순간 남은 글을 지움(조준점을 다시 보낼 때 예전 안내가 따라 나오지 않게)
execute if score @s vTtp matches 1.. unless score @s ttlT matches 1.. run title @s subtitle ""
scoreboard players operation @s vTtp = @s ttlT
scoreboard players add #xh view 1
execute if score #xh view matches 10.. run scoreboard players set #xh view 0
execute if score #xh view matches 0 unless score @s vBig matches 1.. run function rlk:view/xhair
# 손에 든 무기·지도는 3인칭에서 안 보이는 모델로
function rlk:view/hand_wrap

# 우클릭(아이템 사용 중) 감지: 핫바 0~2번(무기·스킬·폭발)을 '쓸 수 있는' 아이템으로 만들어 둠
execute if items entity @s hotbar.0 *[minecraft:custom_data~{rlk_ui:{}}] unless items entity @s hotbar.0 *[minecraft:consumable] run item modify entity @s hotbar.0 {type:"minecraft:set_components",components:{"minecraft:consumable":{consume_seconds:1000000f,animation:"none",sound:"minecraft:intentionally_empty",has_consume_particles:false}}}
execute if items entity @s hotbar.1 *[minecraft:custom_data~{rlk_ui:{}}] unless items entity @s hotbar.1 *[minecraft:consumable] run item modify entity @s hotbar.1 {type:"minecraft:set_components",components:{"minecraft:consumable":{consume_seconds:1000000f,animation:"none",sound:"minecraft:intentionally_empty",has_consume_particles:false}}}
execute if items entity @s hotbar.2 *[minecraft:custom_data~{rlk_ui:{}}] unless items entity @s hotbar.2 *[minecraft:consumable] run item modify entity @s hotbar.2 {type:"minecraft:set_components",components:{"minecraft:consumable":{consume_seconds:1000000f,animation:"none",sound:"minecraft:intentionally_empty",has_consume_particles:false}}}
execute if score @s rcU matches 1 run function rlk:combat/rc_hold
execute unless score @s rcU matches 1 run scoreboard players set @s rcT 0
scoreboard players set @s rcU 0
# 지도는 슬롯 선택으로 열리지 않고 combat/on_attack·rclick_do의 클릭으로 연다.
