# 기본공격으로 처치했을 때 (@s = 플레이어, at @s). #mobKilled = 이번 공격의 처치 수, #killBoss / #killMini = 보스(boss)·미니보스(miniboss) 태그 처치 여부
# 온-킬형 효과는 여기에 추가한다.
function rlk:items/hook/on_kill
# 각인 광전사 6개: 처치하면 잠시 공격 속도 증가
execute if score berserk engN matches 6.. run scoreboard players operation @s berT = #berT tmp
