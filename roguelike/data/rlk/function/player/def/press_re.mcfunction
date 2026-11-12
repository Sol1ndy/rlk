# @s = 플레이어. 받지 않은 F(받지 않는 시간 안의 연타 · 반복 입력): 지금부터 #parRe 틱 동안은 어떤 F 도 받지 않는다(#parMl cb).
# parLk 는 건드리지 않는다: 패링이 되어도(player/def/par_use 가 parLk 를 당겨도) 이 시간은 남으므로 #parRe 틱보다 빠른 연타는 연속
# 공격 속에서도 처음 한 번만 받고, #parRe 틱 이상의 박자로 누르는 F 는 한 번 무시된 뒤 바로 다시 받는다(연속 공격의 나머지를 잃지 않음)
scoreboard players operation #parMl cb = #now cb
scoreboard players operation #parMl cb += #parRe tmp
