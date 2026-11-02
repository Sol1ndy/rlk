# The dialog line of F1 (@s = body): one of api.LINE_OF (random), #lines = when.
scoreboard players operation #lines kn = #clk kn
execute store result score #t kn run random value 0..2
execute if score #t kn matches 0 run function rlk:mboss/line/say {t:"어둠이 내려앉는 순간 멸망이 도래한다.",c:"#FF9AA8",gap:2,hold:50,snd:1}
execute if score #t kn matches 1 run function rlk:mboss/line/say {t:"카운트 다운이 시작됐군.",c:"#FF9AA8",gap:2,hold:50,snd:1}
execute if score #t kn matches 2 run function rlk:mboss/line/say {t:"네가 몸을 기댈 거미줄이 있을까.",c:"#FF9AA8",gap:2,hold:50,snd:1}
