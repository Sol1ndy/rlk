# 원소전투 스킬을 썼을 때 (@s = 플레이어, 위치·방향 = 몸)
execute if score @s it_raven_feather matches 1.. run function rlk:items/proc/raven_start
execute if score @s it_hot_pot matches 1.. run function rlk:items/proc/pot_place
execute if score @s it_jade_shard matches 1.. run function rlk:items/proc/jade
execute if score @s it_ice_quill matches 1.. run function rlk:items/proc/quill_gain
execute if score @s it_baron_bunny matches 1.. unless score #bunnyCd itv matches 1.. run function rlk:items/proc/bunny_place
execute if score @s it_sun_blossom matches 1.. run function rlk:items/proc/blossom_place
execute if score @s it_jellyfish matches 1.. run function rlk:items/proc/jelly_place
execute if score @s it_general_banner matches 1.. run function rlk:items/proc/gflag_place
execute if score @s it_obsidian_mirror matches 1.. run function rlk:items/proc/mirror
execute if score @s it_ember_oath matches 1.. run function rlk:items/proc/ring_start
execute if score @s it_tailor_doll matches 1.. run function rlk:items/proc/doll_place
execute if score @s it_grass_ring matches 1.. run function rlk:items/proc/gring_start
execute if score @s it_hurricane_core matches 1.. run function rlk:items/proc/vortex_place
execute if score @s it_salon_invite matches 1.. run function rlk:items/proc/salon_start
execute if score @s it_sesshou_sakura matches 1.. run function rlk:items/proc/sakura_place
# 바람 신의 시: 띄워 올리기
execute if score @s it_skyward_verse matches 1.. run function rlk:items/proc/updraft
execute if score @s it_lumidouce_case matches 1.. run function rlk:items/proc/case_place
execute if score @s it_dragon_flame matches 1.. run scoreboard players operation #dragT itv = #dragDur tmp
execute if score @s it_tengu_feather matches 1.. run function rlk:items/proc/tengu_place
execute if score @s it_night_stars matches 1.. run function rlk:items/proc/night_start
# 아이템(4차): 계약의 잉크 · 퇴마의 부적 · 간호사의 주사기 · 수련의 무희
execute if score @s it_contract_ink matches 1.. run function rlk:items/proc/ink
execute if score @s it_exorcist_charm matches 1.. run function rlk:items/proc/exorcist
execute if score @s it_nurse_syringe matches 1.. run function rlk:items/proc/nurse_gain
execute if score @s it_water_lily matches 1.. run scoreboard players operation #lilyT itv = #lilyDur tmp
execute if score @s it_moon_chalice matches 1.. run function rlk:items/proc/cg_rip_start
# 튜토리얼: 스킬(3단계 · 캐릭터 2쪽)
execute if score #tutS lob matches 3 if score @s lobRoom matches 2 run scoreboard players add #tutC lob 1
execute if score #tutS lob matches 22 if score @s lobRoom matches 2 run scoreboard players add #tutC lob 1
