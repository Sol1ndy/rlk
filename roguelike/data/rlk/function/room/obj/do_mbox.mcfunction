# 중간보스 아이템 상자(oact 15, @s = 상자 오브젝트, at @s): 상자 하나 = 챕터 등급 아이템 선택 1번.
# pkMb +1 이라 이 묶음에는 캐릭터 카드가 나오지 않는다(lvup/roll).
# 닫힌 상자를 처음 누르면: 선택 1번을 받고 상자가 "열림"이 된 뒤(mboss/box/open: 태그 rlk_mb_boxopen, 금빛 윤곽, 글자 "(열림)") 선택 화면으로.
# 상자는 그 자리에 남는다: 선택을 실제로 쓸 때(고르거나 건너뛸 때 lvup/act/resolve → mboss/box/spend) 열린 상자 하나가 사라진다.
# 그래서 Shift 로 돌아와도 상자가 있고, 열린 상자를 다시 누르면 선택 화면만 다시 연다. 기회는 늘지 않고 선택지도 그대로
# (lvup/toggle 은 rlk:lvpick choices 가 비었을 때만 굴리고, 돌아가기(lvup/exit)는 choices 를 지우지 않음 = 공짜 리롤 없음).
# 열린 상자인데 중간보스 선택(pkMb)이 남아 있지 않으면(정상으로는 생기지 않는 상태) 기회 없이 상자만 치운다
execute if entity @s[tag=rlk_mb_boxopen] unless entity @a[tag=player,scores={pkMb=1..}] run return run function rlk:mboss/box/gone
execute if entity @s[tag=rlk_mb_boxopen] run return run execute as @a[tag=player,limit=1] at @s unless score @s pkMode matches 1.. run function rlk:lvup/toggle
execute as @a[tag=player,limit=1] run scoreboard players add @s pkMb 1
execute as @a[tag=player,limit=1] run function rlk:lvup/add {n:1}
function rlk:mboss/box/open
execute as @a[tag=player,limit=1] at @s unless score @s pkMode matches 1.. run function rlk:lvup/toggle
