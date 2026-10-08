# 원소 입자 생성 (위치 = 실행 위치, macro: n = 개수, el = 원소 번호(0 = 무속성)). 흩어졌다가 플레이어에게 빨려 들어가 원소 에너지가 된다
# 입자 하나의 기본 에너지: 캐릭터와 같은 원소 #enSame / 무속성 #enNeutral / 다른 원소 #enOther (원신: 3 / 2 / 1) — load 의 조절 지점
$scoreboard players set #pcN tmp $(n)
$scoreboard players set #pcEl tmp $(el)
scoreboard players operation #pcVal tmp = #enOther tmp
execute if score #pcEl tmp matches 0 run scoreboard players operation #pcVal tmp = #enNeutral tmp
execute if score #pcEl tmp = #charElem tmp run scoreboard players operation #pcVal tmp = #enSame tmp
function rlk:char/particle_loop
