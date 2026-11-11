# 3단계(퍼펙트) 패링 효과 (@s = 플레이어; 태그 rlk_hc_atk = 공격한 적이 있으면 그쪽으로): 접점(아바타 가슴에서 적 쪽 0.55칸)에
# 금백색 별빛(g/star) · 섬광 · 불꽃, 화면을 가로지르는 금주황 줄(g/title streak, 6틱), 발밑에 기어가는 노란 번개(fx/t_arc 10틱),
# 화면이 짧게 튐(시점 1.5도, 다음 틱에 되돌림 fx/t_jolt; 서버 전체를 멈추거나 느리게 하지 않음). 소리: 모루 · 삼지창 · 자수정 울림.
# 표식의 cb 는 한 틱 더한 값(fx/tick 이 만든 틱에도 한 번 줄임): 번개 11 = 10틱, 화면 튐 3 = 다음 틱에 되돌림
execute if entity @e[tag=rlk_hc_atk,limit=1] at @e[tag=rlk_body,limit=1] positioned ~ ~1.25 ~ facing entity @e[tag=rlk_hc_atk,limit=1] eyes positioned ^ ^ ^0.55 run function rlk:player/def/fx/p3_at
execute unless entity @e[tag=rlk_hc_atk,limit=1] at @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_body,limit=1] rotated ~ 0 positioned ~ ~1.25 ~ positioned ^ ^ ^0.55 run function rlk:player/def/fx/p3_at
function rlk:player/def/fx/ovl {g:"streak",in:0,hold:3,out:3,t:6}
execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_cb_fx","rlk_cb_arc","rlk_cb_new"]}
execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_cb_fx","rlk_cb_jolt","rlk_cb_new"]}
scoreboard players set @e[type=minecraft:marker,tag=rlk_cb_arc,tag=rlk_cb_new] cb 11
scoreboard players set @e[type=minecraft:marker,tag=rlk_cb_jolt,tag=rlk_cb_new] cb 3
# 위아래(pitch)는 끝(±90도)에서 잘리므로 거의 똑바로 올려다볼 때는 좌우(yaw)만 튄다(되돌릴 때 1도 어긋나지 않게; 표식 rlk_cb_jp = 위아래도 튐)
execute store success score #t cb if entity @a[tag=player,limit=1,x_rotation=-88..90]
execute if score #t cb matches 1 run tag @e[type=minecraft:marker,tag=rlk_cb_jolt,tag=rlk_cb_new] add rlk_cb_jp
tag @e[tag=rlk_cb_new] remove rlk_cb_new
execute if score #t cb matches 1 as @a[tag=player,limit=1] at @s run rotate @s ~1.5 ~-1
execute unless score #t cb matches 1 as @a[tag=player,limit=1] at @s run rotate @s ~1.5 ~
