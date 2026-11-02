# The dialog line of Q5B (@s = body): one of api.LINE_OF (random), #lines = when.
scoreboard players operation #lines kn = #clk kn
execute store result score #t kn run random value 0..2
execute if score #t kn matches 0 run function rlk:mboss/line/say {t:"이제 네 본심을 볼 수 있겠군.",c:"#FF9AA8",gap:2,hold:50,snd:1}
execute if score #t kn matches 1 run function rlk:mboss/line/say {t:"형벌을 시작하지.",c:"#FF9AA8",gap:2,hold:50,snd:1}
execute if score #t kn matches 2 run function rlk:mboss/line/say {t:"일몰은 그저, 모든 것의 시작일 뿐.",c:"#FF9AA8",gap:2,hold:50,snd:1}
