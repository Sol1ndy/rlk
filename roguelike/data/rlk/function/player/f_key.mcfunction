# F = 패링 (@s = 플레이어, at @s; player/def/input: 무기 · 스킬 · 폭발 아이템이 왼손에 넘어옴, 웅크리지 않음). 아이템 회수는
# player/hotbar/tick 이 한다. 받은 F 는 지금 틱(#now cb)을 parAt 에 찍고, #parGap 틱 동안 다시 받지 않는다. 그동안 또 누르면
# (연타 · 키를 누르고 있어 반복 입력) 받지 않는 시간이 지금 + #parRe 로 늘어난다. 판정은 맞는 순간(player/def/judge)
execute if score @s vMap matches 1 run return 0
execute if score @s pkMode matches 1.. run return 0
execute if score @s dead matches 1 run return 0
execute if score @s buT matches 1.. run return 0
execute if score @s rnDie matches 1.. run return 0
execute if score @s rdCam matches 1 run return 0
execute unless score @s parHit matches -2147483648.. run function rlk:player/def/reset
execute if score #now cb < @s parLk run return run function rlk:player/def/press_re
function rlk:player/def/press
