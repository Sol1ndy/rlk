# 원소폭발 피해 보정 지점 (@s = 플레이어). 원소폭발의 피해(#dmg)를 계산한 직후에 호출할 것 — 새 캐릭터의 원소폭발도 반드시 이 함수를 부른다
# 초월 · 악요개안: 원소 에너지 1pt당 원소폭발 피해 +0.3% (보유 개수만큼)
execute if score @s it_stormy_eye matches 1.. run function rlk:items/proc/eye_burst
# 불씨의 맹약: 전의 1당 원소폭발 피해 증가
execute if score @s it_ember_oath matches 1.. run function rlk:items/proc/oath_burst
# 각인 절연 4개: 원소폭발 피해 +(원소 충전 효율 × #emblemPct%)%, 최대 #emblemMax%
execute if score emblem engN matches 4.. run function rlk:engravings/emblem/burst
# 각인 전의 2개: 원소폭발 피해 증가
execute if score spirit engN matches 2.. run function rlk:engravings/spirit/burst
