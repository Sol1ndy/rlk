# 아바타·카메라 받침·조준점 만들기 (@s = 플레이어, at @s = 아바타가 설 자리)
kill @e[tag=rlk_view]
scoreboard players add #avId view 1
# 캐릭터 정보에 model 이 없으면 wide(기본)
execute if data storage rlk:chars cur.info unless data storage rlk:chars cur.info.model run data modify storage rlk:chars cur.info.model set value "wide"
function rlk:view/spawn2 with storage rlk:chars cur.info
# 캐릭터 정보(스킨)가 없으면 기본 모습으로
execute unless entity @e[tag=rlk_avnew,limit=1] run summon minecraft:mannequin ~ ~ ~ {Tags:["rlk_view","rlk_av","rlk_body","rlk_pet","rlk_avnew"],hide_description:1b}
execute rotated as @s as @e[tag=rlk_avnew] run rotate @s ~ 0
scoreboard players operation @e[tag=rlk_avnew] avId = #avId view
# 바닐라 체력 1024 고정(맞았는지 감지만 함. 실제 체력은 플레이어의 curHealth) / 낙하 피해 없음
attribute @e[tag=rlk_avnew,limit=1] minecraft:max_health base set 1024
attribute @e[tag=rlk_avnew,limit=1] minecraft:fall_damage_multiplier base set 0
attribute @e[tag=rlk_avnew,limit=1] minecraft:step_height base set 0.6
data modify entity @e[tag=rlk_avnew,limit=1] Health set value 1024f
item replace entity @e[tag=rlk_avnew,limit=1] weapon.mainhand from entity @s hotbar.0
function rlk:view/av_unwrap
execute if score #charN tmp matches 7..8 run item replace entity @e[tag=rlk_avnew,limit=1] weapon.mainhand with minecraft:air
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_view","rlk_camv"],teleport_duration:1}
scoreboard players set #durNow view -1
execute positioned ~ ~1.62 ~ positioned ^ ^ ^6 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_view","rlk_aim"]}
summon minecraft:marker ~ ~ ~ {Tags:["rlk_view","rlk_vmk"]}
# 진짜 플레이어: 투명 · 중력 없음 · 몹과 같은 팀(몹이 진짜 플레이어를 노리지 않게)
effect give @s minecraft:invisibility infinite 0 true
attribute @s minecraft:gravity base set 0
# 바닐라 3인칭(F5)을 눌러도 카메라가 물러나지 않게
attribute @s minecraft:camera_distance base set 0
team join rlk_cam @s
team join rlk_stun @e[tag=rlk_av]
team join rlk_cam @e[tag=rlk_mob]
# 이미 나와 있는 몹의 어그로를 아바타로
execute as @e[tag=rlk_mob,tag=!rlk_cmb] run damage @s 0 minecraft:generic by @e[tag=rlk_avnew,limit=1]
tag @e[tag=rlk_avnew] remove rlk_avnew
