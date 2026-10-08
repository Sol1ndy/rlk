# 원소 반응이 일어남 (@s = 맞은 몹 또는 풀 씨앗, #rx = 반응 번호)
# 단풍잎 한 장: 확산(8) → 확산된 원소(몹의 rxEl)로 주는 피해 증가
execute if score #rx tmp matches 8 if score @a[tag=player,limit=1] it_maple_leaf matches 1.. unless score #mapleCd itv matches 1.. run function rlk:items/proc/maple
# 별빛 바람뭉치: 얼음을 확산(8)
execute if score #rx tmp matches 8 if score @s rxEl matches 4 if score @a[tag=player,limit=1] it_star_wisp matches 1.. unless score #wispCd itv matches 1.. run function rlk:items/proc/wisp_spawn
# 특순대 휘장: 과부하(3)
execute if score #rx tmp matches 3 if score @a[tag=player,limit=1] it_musketeer_badge matches 1.. run scoreboard players operation #muskT itv = #muskDur tmp
# 스칸다의 씨앗: 씨앗이 붙은 적에게 반응
execute if entity @s[tag=rlk_mob] if score @a[tag=player,limit=1] it_skandha_seed matches 1.. unless score #skCd itv matches 1.. run function rlk:items/proc/skandha_rx
# 용의 불씨: 증발(1)·융해(2) 피해 증가
execute if score #dragT itv matches 1.. if score #rx tmp matches 1..2 unless score #tfm tmp matches 1 run function rlk:items/proc/drag_rx
# 밤혼의 구슬: 과부하(3)·초전도(4)·감전(5)
execute if score #rx tmp matches 3..5 if entity @s[tag=rlk_mob] if score @a[tag=player,limit=1] it_nightsoul_orb matches 1.. unless score #orbCd itv matches 1.. run function rlk:items/proc/orb_queue
# 바람 슬라임 인형: 확산(8)
execute if score #rx tmp matches 8 if score @a[tag=player,limit=1] it_wind_slime matches 1.. run scoreboard players operation #slimeT itv = #slimeDur tmp
# 꿈결 베개: 확산(8) / 달빛 베틀: 모든 반응
execute if score #rx tmp matches 8 if score @a[tag=player,limit=1] it_dream_pillow matches 1.. run scoreboard players operation #pillowT itv = #pillowDur tmp
execute if score @a[tag=player,limit=1] it_moonlit_loom matches 1.. run scoreboard players operation #loomT itv = #loomDur tmp
