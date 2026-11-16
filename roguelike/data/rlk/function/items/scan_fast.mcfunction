# (@s = 플레이어, items/equip_scan 에서; 바로 앞에서 player/inv/manage 가 돈 경우만) 빠른 스캔 조건 → #scF 1
#  ① 지난 스캔(rlk:scan held)이 이 플레이어의 것  ② order 길이 ≤ invCap  ③ 몸에 있는 모든 rlk 아이템 수(clear … 0 = items/scan_count 와
#  같은 범위: 인벤 · 핫바 · 왼손 · 갑옷 · 커서 · 조합칸) = order 길이. manage 의 place_items 가 order[k] 를 inventory.(9+k) 에 놓았으므로
#  ②③ 이면 그 밖의 rlk 아이템이 없다 → 가진 id = order 의 id, 나머지 id 의 개수는 0
execute unless score @s eqEp = #scEp eqEp run return 0
execute store result score #scO tmp run data get storage rlk:pinv order
execute if score #scO tmp > @s invCap run return 0
execute store result score #scT tmp run clear @s *[minecraft:custom_data~{rlk:{}}] 0
execute unless score #scT tmp = #scO tmp run return 0
scoreboard players set #scF tmp 1
