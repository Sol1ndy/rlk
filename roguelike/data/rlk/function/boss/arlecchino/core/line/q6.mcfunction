# The dialog line of Q6 (@s = body): one of api.LINE_OF (random), #lines = when.
scoreboard players operation #lines kn = #clk kn
execute store result score #t kn run random value 0..2
execute if score #t kn matches 0 run function rlk:mboss/line/say {t:"해와 달은 결국 지고 파멸은 계속해서 찾아오지!",c:"#FF9AA8",gap:2,hold:50,snd:1}
execute if score #t kn matches 1 run function rlk:mboss/line/say {t:"부질없는 저항이군!",c:"#FF9AA8",gap:2,hold:50,snd:1}
execute if score #t kn matches 2 run function rlk:mboss/line/say {t:"희망은 사라진지 오래다!",c:"#FF9AA8",gap:2,hold:50,snd:1}
