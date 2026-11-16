# 잔상 (round V: 흰 테두리 — 붉은 꽃밭에서도 보이게; 위치 · 방향 = 닷지를 시작한 자리, 아바타가 보던 쪽): 지금 캐릭터 모습의 마네킹(투명 + 빛남 = 테두리만, 팀 rlk_cbred 의 색), 8틱 보임
# (cb 9: 만든 틱 + 8틱째에 fx/ghost_out 이 치움). 앞선 잔상이 남아 있으면 먼저 치운다(kill 은 사망 동작을 보여 주므로 fx/ghost_out)
execute as @e[tag=rlk_cb_ghost] run function rlk:player/def/fx/ghost_out
execute if data storage rlk:chars cur.info.prof run function rlk:player/def/fx/pd_ghost_m with storage rlk:chars cur.info
execute unless data storage rlk:chars cur.info.prof run summon minecraft:mannequin ~ ~ ~ {Tags:["rlk_cb_fx","rlk_cb_ghost","rlk_pet","rlk_cb_new"],hide_description:1b,immovable:1b,NoGravity:1b,Invulnerable:1b,Silent:1b,Glowing:1b,active_effects:[{id:"minecraft:invisibility",duration:-1,amplifier:0,show_particles:0b,ambient:1b}]}
team join rlk_cbred @e[tag=rlk_cb_ghost,tag=rlk_cb_new]
execute as @e[tag=rlk_cb_ghost,tag=rlk_cb_new] run rotate @s ~ 0
scoreboard players set @e[tag=rlk_cb_ghost,tag=rlk_cb_new] cb 9
tag @e[tag=rlk_cb_new] remove rlk_cb_new
