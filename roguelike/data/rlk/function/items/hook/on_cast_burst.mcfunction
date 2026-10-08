# 원소폭발을 썼을 때 (@s = 플레이어, 위치·방향 = 몸)
execute if score @s it_rain_sheath matches 1.. run scoreboard players operation #rainT itv = #rainDur tmp
execute if score @s it_banner matches 1.. run function rlk:items/proc/flag_place
# 각인 전의 4개: 원소폭발을 쓴 뒤 공격력 증가
execute if score spirit engN matches 4.. run scoreboard players operation #spiritT eng = #spiritDur tmp
execute if score @s it_hound_whistle matches 1.. run function rlk:items/proc/hound_start
execute if score @s it_ember_oath matches 1.. run function rlk:items/proc/oath_use
# 바람 신의 시: 폭풍의 눈
execute if score @s it_skyward_verse matches 1.. run function rlk:items/proc/storm_place
# 옥장 방패: 운석
execute if score @s it_jade_shard matches 1.. run function rlk:items/proc/meteor_place
# 스칸다의 씨앗: 원소 마스터리 증가
execute if score @s it_skandha_seed matches 1.. run scoreboard players operation #mayaT itv = #mayaDur tmp
# 살롱의 초대장: 열기
execute if score @s it_salon_invite matches 1.. run function rlk:items/proc/fan_start
execute if score @s it_seamless_shield matches 1.. run scoreboard players operation #seamT itv = #seamDur tmp
execute if score @s it_opera_flag matches 1.. run scoreboard players operation #operaT itv = #operaDur tmp
execute if score @s it_opera_flag matches 1.. run scoreboard players operation #operaN itv = #operaMax tmp
execute if score @s it_genie_lamp matches 1.. run scoreboard players operation #genieT itv = #genieDur tmp
# 아이템(4차): 죄인의 창끝 · 서약의 단검 · 성스러운 방패 · 민들레 씨앗 · 붉은 달의 서약
execute if score @s it_sinner_spear matches 1.. run scoreboard players operation #sinT itv = #sinDur tmp
execute if score @s it_pact_dagger matches 1.. run function rlk:items/proc/dagger_bol
execute if score @s it_holy_shield matches 1.. run scoreboard players operation #candT itv = #candDur tmp
execute if score @s it_dandelion_seed matches 1.. run function rlk:items/proc/dandelion
execute if score @s it_crimson_moon matches 1.. run function rlk:items/proc/cmoon_bol
execute if score @s it_moon_chalice matches 1.. run function rlk:items/proc/cg_moon
