# 포자 주머니 (실행 위치 = 버섯이 죽은 바닥). 맞힐 수 있는 물체: 투명 NoAI 허스크(rlk_mob 을 미리 달아 체력바 · 방 몹 아님, rlk_zmob 없음) + 모습 2부품
summon minecraft:husk ~ ~ ~ {Tags:["rlk_room","rlk_mob","rlk_cmlink","rlk_c3pod","rlk_c3pnew"],NoAI:1b,Silent:1b,PersistenceRequired:1b,DeathLootTable:"minecraft:empty",IsBaby:0b,CanPickUpLoot:0b,active_effects:[{id:"minecraft:invisibility",duration:-1,amplifier:0,show_particles:0b,ambient:1b}],attributes:[{id:"minecraft:scale",base:0.55d},{id:"minecraft:max_health",base:1024d},{id:"minecraft:knockback_resistance",base:1d}],Health:1024f}
scoreboard players operation @e[tag=rlk_c3pnew,type=minecraft:husk] c3L = #c3PodL tmp
scoreboard players set @e[tag=rlk_c3pnew,type=minecraft:husk] mlv 1
scoreboard players set @e[tag=rlk_c3pnew,type=minecraft:husk] mhp0 1
scoreboard players set @e[tag=rlk_c3pnew,type=minecraft:husk] mhpM 1
scoreboard players set @e[tag=rlk_c3pnew,type=minecraft:husk] mhpC 1
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_pet","rlk_cmlink","rlk_fp_pt","rlk_fp_pod","rlk_c3pnew"],NoGravity:1b,Invulnerable:1b,billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:1,view_range:1.5f,width:1.6f,height:1.6f,shadow_radius:0f,brightness:{sky:15,block:15},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:cm/c3/fp/pod","minecraft:custom_model_data":{colors:[16777215]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_pet","rlk_cmlink","rlk_fp_pt","rlk_fp_glow","rlk_c3pnew"],NoGravity:1b,Invulnerable:1b,billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:1,view_range:1.5f,width:1.6f,height:1.6f,shadow_radius:0f,brightness:{sky:15,block:15},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:cm/c3/fp/glow","minecraft:custom_model_data":{colors:[16777215]}}}}
# 주머니와 부품은 cmId 로 묶임. 주머니도 rlk_cmlink(매 틱 cm/c3/clean 에서 rlk_cmsync) → 모습이 없어져도 cm/clean 이 돌아 제때 사라짐
scoreboard players add #cmIdC tmp 1
scoreboard players operation @e[tag=rlk_c3pnew] cmId = #cmIdC tmp
tag @e[tag=rlk_c3pnew] add rlk_cmsync
execute as @e[tag=rlk_c3pnew,tag=rlk_fp_pt] run function rlk:cm/fp/pose/0
tag @e[tag=rlk_c3pnew] remove rlk_c3pnew
execute unless score #c3fpgrow snd matches 1 run function rlk:cm/c3/snd/fpgrow
