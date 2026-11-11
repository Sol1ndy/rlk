# F = 패링 (@s = 플레이어, at @s; player/def/input: 무기 · 스킬 · 폭발 아이템이 왼손에 넘어옴, 웅크리지 않음). 아이템 회수는
# player/hotbar/tick 이 한다. 받은 F 는 지금 틱(#now cb)을 parAt 에 찍고, parLk 까지 다시 받지 않는다(player/def/press: #parGap;
# 막으면 #parChain). 받지 않은 F(연타 · 키를 누르고 있어 생기는 반복 입력)는 그 뒤 #parRe 틱 동안 어떤 F 도 받지 않게 한다
# (#parMl cb, player/def/press_re). 판정은 맞는 순간(player/def/judge)
execute if score @s vMap matches 1 run return 0
execute if score @s pkMode matches 1.. run return 0
execute if score @s dead matches 1 run return 0
execute if score @s buT matches 1.. run return 0
execute if score @s rnDie matches 1.. run return 0
execute if score @s rdCam matches 1 run return 0
# 움직임이 잠긴 동작(스킬 시전 등, pmMoveLock) 중에는 받지 않는다(닷지와 같음: 그 동작을 끊지 않게)
execute if score @s pmMoveLock matches 1 run return 0
execute unless score @s parHit matches -2147483648.. run function rlk:player/def/reset
execute if score #now cb < @s parLk run return run function rlk:player/def/press_re
execute if score #now cb < #parMl cb run return run function rlk:player/def/press_re
function rlk:player/def/press
