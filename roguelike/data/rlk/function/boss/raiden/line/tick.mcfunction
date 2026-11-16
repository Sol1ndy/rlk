# Advances the boss line in progress (#rdLine id, #rdLineT age, #rdLineN next step); called from tick.
execute unless score #rdLine rd matches 1.. run return 0
scoreboard players add #rdLineT rd 1
execute unless score #rdLineT rd = #rdLineN rd run return 0
execute if score #rdLine rd matches 1 if score #rdLineT rd matches 0 run function rlk:boss/raiden/line/show {t:"그",c:"#d7b4ff",s:11,f:0,n:11,e:0,g:5}
execute if score #rdLine rd matches 1 if score #rdLineT rd matches 5 run function rlk:boss/raiden/line/show {t:"그 끝은",c:"#d7b4ff",s:11,f:0,n:11,e:0,g:5}
execute if score #rdLine rd matches 1 if score #rdLineT rd matches 10 run function rlk:boss/raiden/line/show {t:"그 끝은 만겁",c:"#d7b4ff",s:11,f:0,n:11,e:0,g:5}
execute if score #rdLine rd matches 1 if score #rdLineT rd matches 15 run function rlk:boss/raiden/line/show {t:"그 끝은 만겁일지니",c:"#d7b4ff",s:11,f:0,n:11,e:0,g:5}
execute if score #rdLine rd matches 1 if score #rdLineT rd matches 20 run function rlk:boss/raiden/line/show {t:"그 끝은 만겁일지니...",c:"#d7b4ff",s:24,f:12,n:36,e:1,g:5}
execute if score #rdLine rd matches 2 if score #rdLineT rd matches 0 run function rlk:boss/raiden/line/show {t:"이",c:"#d7b4ff",s:9,f:0,n:9,e:0,g:3}
execute if score #rdLine rd matches 2 if score #rdLineT rd matches 3 run function rlk:boss/raiden/line/show {t:"이 몸이",c:"#d7b4ff",s:9,f:0,n:9,e:0,g:3}
execute if score #rdLine rd matches 2 if score #rdLineT rd matches 6 run function rlk:boss/raiden/line/show {t:"이 몸이 곧",c:"#d7b4ff",s:9,f:0,n:9,e:0,g:3}
execute if score #rdLine rd matches 2 if score #rdLineT rd matches 9 run function rlk:boss/raiden/line/show {t:"이 몸이 곧 영원",c:"#d7b4ff",s:9,f:0,n:9,e:0,g:3}
execute if score #rdLine rd matches 2 if score #rdLineT rd matches 12 run function rlk:boss/raiden/line/show {t:"이 몸이 곧 영원이다",c:"#d7b4ff",s:26,f:12,n:38,e:1,g:3}
execute if score #rdLine rd matches 3 if score #rdLineT rd matches 0 run function rlk:boss/raiden/line/show {t:"그",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 3 if score #rdLineT rd matches 2 run function rlk:boss/raiden/line/show {t:"그 무엇",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 3 if score #rdLineT rd matches 4 run function rlk:boss/raiden/line/show {t:"그 무엇도",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 3 if score #rdLineT rd matches 6 run function rlk:boss/raiden/line/show {t:"그 무엇도 영원",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 3 if score #rdLineT rd matches 8 run function rlk:boss/raiden/line/show {t:"그 무엇도 영원한",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 3 if score #rdLineT rd matches 10 run function rlk:boss/raiden/line/show {t:"그 무엇도 영원한 것은",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 3 if score #rdLineT rd matches 12 run function rlk:boss/raiden/line/show {t:"그 무엇도 영원한 것은 없다",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 3 if score #rdLineT rd matches 14 run function rlk:boss/raiden/line/show {t:"그 무엇도 영원한 것은 없다.",c:"#d7b4ff",s:40,f:12,n:52,e:1,g:2}
execute if score #rdLine rd matches 4 if score #rdLineT rd matches 0 run function rlk:boss/raiden/line/show {t:"뇌광",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 4 if score #rdLineT rd matches 2 run function rlk:boss/raiden/line/show {t:"뇌광이",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 4 if score #rdLineT rd matches 4 run function rlk:boss/raiden/line/show {t:"뇌광이 영원",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 4 if score #rdLineT rd matches 6 run function rlk:boss/raiden/line/show {t:"뇌광이 영원의",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 4 if score #rdLineT rd matches 8 run function rlk:boss/raiden/line/show {t:"뇌광이 영원의 땅을",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 4 if score #rdLineT rd matches 10 run function rlk:boss/raiden/line/show {t:"뇌광이 영원의 땅을 비추",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 4 if score #rdLineT rd matches 12 run function rlk:boss/raiden/line/show {t:"뇌광이 영원의 땅을 비추는구",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 4 if score #rdLineT rd matches 14 run function rlk:boss/raiden/line/show {t:"뇌광이 영원의 땅을 비추는구나",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 4 if score #rdLineT rd matches 16 run function rlk:boss/raiden/line/show {t:"뇌광이 영원의 땅을 비추는구나.",c:"#d7b4ff",s:24,f:12,n:36,e:1,g:2}
execute if score #rdLine rd matches 5 if score #rdLineT rd matches 0 run function rlk:boss/raiden/line/show {t:"찰나",c:"#d7b4ff",s:9,f:0,n:9,e:0,g:3}
execute if score #rdLine rd matches 5 if score #rdLineT rd matches 3 run function rlk:boss/raiden/line/show {t:"찰나의...",c:"#d7b4ff",s:9,f:0,n:9,e:0,g:3}
execute if score #rdLine rd matches 5 if score #rdLineT rd matches 6 run function rlk:boss/raiden/line/show {t:"찰나의... 포영",c:"#d7b4ff",s:9,f:0,n:9,e:0,g:3}
execute if score #rdLine rd matches 5 if score #rdLineT rd matches 9 run function rlk:boss/raiden/line/show {t:"찰나의... 포영!",c:"#d7b4ff",s:22,f:12,n:34,e:1,g:3}
execute if score #rdLine rd matches 6 if score #rdLineT rd matches 0 run function rlk:boss/raiden/line/show {t:"간파",c:"#bfe4ff",s:10,f:0,n:10,e:0,g:4}
execute if score #rdLine rd matches 6 if score #rdLineT rd matches 4 run function rlk:boss/raiden/line/show {t:"간파했군",c:"#bfe4ff",s:10,f:0,n:10,e:0,g:4}
execute if score #rdLine rd matches 6 if score #rdLineT rd matches 8 run function rlk:boss/raiden/line/show {t:"간파했군.",c:"#bfe4ff",s:34,f:12,n:46,e:1,g:4}
execute if score #rdLine rd matches 7 if score #rdLineT rd matches 0 run function rlk:boss/raiden/line/show {t:"뇌명",c:"#d7b4ff",s:10,f:0,n:10,e:0,g:4}
execute if score #rdLine rd matches 7 if score #rdLineT rd matches 4 run function rlk:boss/raiden/line/show {t:"뇌명.",c:"#d7b4ff",s:20,f:12,n:32,e:1,g:4}
execute if score #rdLine rd matches 8 if score #rdLineT rd matches 0 run function rlk:boss/raiden/line/show {t:"뇌전",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 8 if score #rdLineT rd matches 2 run function rlk:boss/raiden/line/show {t:"뇌전은",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 8 if score #rdLineT rd matches 4 run function rlk:boss/raiden/line/show {t:"뇌전은 인간",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 8 if score #rdLineT rd matches 6 run function rlk:boss/raiden/line/show {t:"뇌전은 인간의",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 8 if score #rdLineT rd matches 8 run function rlk:boss/raiden/line/show {t:"뇌전은 인간의 의지",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 8 if score #rdLineT rd matches 10 run function rlk:boss/raiden/line/show {t:"뇌전은 인간의 의지 따위",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 8 if score #rdLineT rd matches 12 run function rlk:boss/raiden/line/show {t:"뇌전은 인간의 의지 따위로",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 8 if score #rdLineT rd matches 14 run function rlk:boss/raiden/line/show {t:"뇌전은 인간의 의지 따위로 변하",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 8 if score #rdLineT rd matches 16 run function rlk:boss/raiden/line/show {t:"뇌전은 인간의 의지 따위로 변하지",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 8 if score #rdLineT rd matches 18 run function rlk:boss/raiden/line/show {t:"뇌전은 인간의 의지 따위로 변하지 않아",c:"#d7b4ff",s:22,f:12,n:34,e:1,g:2}
execute if score #rdLine rd matches 9 if score #rdLineT rd matches 0 run function rlk:boss/raiden/line/show {t:"번개",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 9 if score #rdLineT rd matches 2 run function rlk:boss/raiden/line/show {t:"번개여,",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 9 if score #rdLineT rd matches 4 run function rlk:boss/raiden/line/show {t:"번개여, 나의",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 9 if score #rdLineT rd matches 6 run function rlk:boss/raiden/line/show {t:"번개여, 나의 호령",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 9 if score #rdLineT rd matches 8 run function rlk:boss/raiden/line/show {t:"번개여, 나의 호령을",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 9 if score #rdLineT rd matches 10 run function rlk:boss/raiden/line/show {t:"번개여, 나의 호령을 따르",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 9 if score #rdLineT rd matches 12 run function rlk:boss/raiden/line/show {t:"번개여, 나의 호령을 따르라",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 9 if score #rdLineT rd matches 14 run function rlk:boss/raiden/line/show {t:"번개여, 나의 호령을 따르라.",c:"#d7b4ff",s:22,f:12,n:34,e:1,g:2}
execute if score #rdLine rd matches 10 if score #rdLineT rd matches 0 run function rlk:boss/raiden/line/show {t:"무념",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 10 if score #rdLineT rd matches 2 run function rlk:boss/raiden/line/show {t:"무념 무상,",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 10 if score #rdLineT rd matches 4 run function rlk:boss/raiden/line/show {t:"무념 무상, 천하",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 10 if score #rdLineT rd matches 6 run function rlk:boss/raiden/line/show {t:"무념 무상, 천하가",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 10 if score #rdLineT rd matches 8 run function rlk:boss/raiden/line/show {t:"무념 무상, 천하가 고요",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 10 if score #rdLineT rd matches 10 run function rlk:boss/raiden/line/show {t:"무념 무상, 천하가 고요하리",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 10 if score #rdLineT rd matches 12 run function rlk:boss/raiden/line/show {t:"무념 무상, 천하가 고요하리.",c:"#d7b4ff",s:12,f:12,n:24,e:1,g:2}
execute if score #rdLine rd matches 11 if score #rdLineT rd matches 0 run function rlk:boss/raiden/line/show {t:"무념",c:"#e6a3ff",s:7,f:0,n:7,e:0,g:1}
execute if score #rdLine rd matches 11 if score #rdLineT rd matches 1 run function rlk:boss/raiden/line/show {t:"무념 무상,",c:"#e6a3ff",s:7,f:0,n:7,e:0,g:1}
execute if score #rdLine rd matches 11 if score #rdLineT rd matches 2 run function rlk:boss/raiden/line/show {t:"무념 무상, 일도",c:"#e6a3ff",s:7,f:0,n:7,e:0,g:1}
execute if score #rdLine rd matches 11 if score #rdLineT rd matches 3 run function rlk:boss/raiden/line/show {t:"무념 무상, 일도 단절",c:"#e6a3ff",s:7,f:0,n:7,e:0,g:1}
execute if score #rdLine rd matches 11 if score #rdLineT rd matches 4 run function rlk:boss/raiden/line/show {t:"무념 무상, 일도 단절.",c:"#e6a3ff",s:16,f:12,n:28,e:1,g:1}
execute if score #rdLine rd matches 12 if score #rdLineT rd matches 0 run function rlk:boss/raiden/line/show {t:"방해",c:"#e6a3ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 12 if score #rdLineT rd matches 2 run function rlk:boss/raiden/line/show {t:"방해는",c:"#e6a3ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 12 if score #rdLineT rd matches 4 run function rlk:boss/raiden/line/show {t:"방해는 모두",c:"#e6a3ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 12 if score #rdLineT rd matches 6 run function rlk:boss/raiden/line/show {t:"방해는 모두 베겠",c:"#e6a3ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 12 if score #rdLineT rd matches 8 run function rlk:boss/raiden/line/show {t:"방해는 모두 베겠노라",c:"#e6a3ff",s:22,f:12,n:34,e:1,g:2}
execute if score #rdLine rd matches 13 if score #rdLineT rd matches 0 run function rlk:boss/raiden/line/show {t:"감옥",c:"#e6a3ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 13 if score #rdLineT rd matches 2 run function rlk:boss/raiden/line/show {t:"감옥으로",c:"#e6a3ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 13 if score #rdLineT rd matches 4 run function rlk:boss/raiden/line/show {t:"감옥으로 만들",c:"#e6a3ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 13 if score #rdLineT rd matches 6 run function rlk:boss/raiden/line/show {t:"감옥으로 만들어",c:"#e6a3ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 13 if score #rdLineT rd matches 8 run function rlk:boss/raiden/line/show {t:"감옥으로 만들어 주지",c:"#e6a3ff",s:22,f:12,n:34,e:1,g:2}
execute if score #rdLine rd matches 14 if score #rdLineT rd matches 0 run function rlk:boss/raiden/line/show {t:"천수",c:"#e6a3ff",s:9,f:0,n:9,e:0,g:3}
execute if score #rdLine rd matches 14 if score #rdLineT rd matches 3 run function rlk:boss/raiden/line/show {t:"천수의",c:"#e6a3ff",s:9,f:0,n:9,e:0,g:3}
execute if score #rdLine rd matches 14 if score #rdLineT rd matches 6 run function rlk:boss/raiden/line/show {t:"천수의 속박",c:"#e6a3ff",s:9,f:0,n:9,e:0,g:3}
execute if score #rdLine rd matches 14 if score #rdLineT rd matches 9 run function rlk:boss/raiden/line/show {t:"천수의 속박!",c:"#e6a3ff",s:30,f:12,n:42,e:1,g:3}
execute if score #rdLine rd matches 15 if score #rdLineT rd matches 0 run function rlk:boss/raiden/line/show {t:"단절",c:"#e6a3ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 15 if score #rdLineT rd matches 2 run function rlk:boss/raiden/line/show {t:"단절!",c:"#e6a3ff",s:20,f:12,n:32,e:1,g:2}
execute if score #rdLine rd matches 16 if score #rdLineT rd matches 0 run function rlk:boss/raiden/line/show {t:"궤멸",c:"#e6a3ff",s:9,f:0,n:9,e:0,g:3}
execute if score #rdLine rd matches 16 if score #rdLineT rd matches 3 run function rlk:boss/raiden/line/show {t:"궤멸하라",c:"#e6a3ff",s:9,f:0,n:9,e:0,g:3}
execute if score #rdLine rd matches 16 if score #rdLineT rd matches 6 run function rlk:boss/raiden/line/show {t:"궤멸하라!",c:"#e6a3ff",s:24,f:12,n:36,e:1,g:3}
execute if score #rdLine rd matches 17 if score #rdLineT rd matches 0 run function rlk:boss/raiden/line/show {t:"뚫려",c:"#e6a3ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 17 if score #rdLineT rd matches 2 run function rlk:boss/raiden/line/show {t:"뚫려라",c:"#e6a3ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 17 if score #rdLineT rd matches 4 run function rlk:boss/raiden/line/show {t:"뚫려라!",c:"#e6a3ff",s:20,f:12,n:32,e:1,g:2}
execute if score #rdLine rd matches 18 if score #rdLineT rd matches 0 run function rlk:boss/raiden/line/show {t:"너무",c:"#d7b4ff",s:9,f:0,n:9,e:0,g:3}
execute if score #rdLine rd matches 18 if score #rdLineT rd matches 3 run function rlk:boss/raiden/line/show {t:"너무 느리",c:"#d7b4ff",s:9,f:0,n:9,e:0,g:3}
execute if score #rdLine rd matches 18 if score #rdLineT rd matches 6 run function rlk:boss/raiden/line/show {t:"너무 느리군",c:"#d7b4ff",s:9,f:0,n:9,e:0,g:3}
execute if score #rdLine rd matches 18 if score #rdLineT rd matches 9 run function rlk:boss/raiden/line/show {t:"너무 느리군.",c:"#d7b4ff",s:20,f:12,n:32,e:1,g:3}
execute if score #rdLine rd matches 19 if score #rdLineT rd matches 0 run function rlk:boss/raiden/line/show {t:"판결",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 19 if score #rdLineT rd matches 2 run function rlk:boss/raiden/line/show {t:"판결은",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 19 if score #rdLineT rd matches 4 run function rlk:boss/raiden/line/show {t:"판결은 내려",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 19 if score #rdLineT rd matches 6 run function rlk:boss/raiden/line/show {t:"판결은 내려졌다",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 19 if score #rdLineT rd matches 8 run function rlk:boss/raiden/line/show {t:"판결은 내려졌다.",c:"#d7b4ff",s:22,f:12,n:34,e:1,g:2}
execute if score #rdLine rd matches 20 if score #rdLineT rd matches 0 run function rlk:boss/raiden/line/show {t:"번개",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 20 if score #rdLineT rd matches 2 run function rlk:boss/raiden/line/show {t:"번개와",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 20 if score #rdLineT rd matches 4 run function rlk:boss/raiden/line/show {t:"번개와 함께",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 20 if score #rdLineT rd matches 6 run function rlk:boss/raiden/line/show {t:"번개와 함께 흙으",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 20 if score #rdLineT rd matches 8 run function rlk:boss/raiden/line/show {t:"번개와 함께 흙으로",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 20 if score #rdLineT rd matches 10 run function rlk:boss/raiden/line/show {t:"번개와 함께 흙으로 돌아",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 20 if score #rdLineT rd matches 12 run function rlk:boss/raiden/line/show {t:"번개와 함께 흙으로 돌아가라",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 20 if score #rdLineT rd matches 14 run function rlk:boss/raiden/line/show {t:"번개와 함께 흙으로 돌아가라.",c:"#d7b4ff",s:22,f:12,n:34,e:1,g:2}
execute if score #rdLine rd matches 21 if score #rdLineT rd matches 0 run function rlk:boss/raiden/line/show {t:"속세",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 21 if score #rdLineT rd matches 2 run function rlk:boss/raiden/line/show {t:"속세는",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 21 if score #rdLineT rd matches 4 run function rlk:boss/raiden/line/show {t:"속세는 그림",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 21 if score #rdLineT rd matches 6 run function rlk:boss/raiden/line/show {t:"속세는 그림자와",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 21 if score #rdLineT rd matches 8 run function rlk:boss/raiden/line/show {t:"속세는 그림자와 같지",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 21 if score #rdLineT rd matches 10 run function rlk:boss/raiden/line/show {t:"속세는 그림자와 같지.",c:"#d7b4ff",s:22,f:12,n:34,e:1,g:2}
execute if score #rdLine rd matches 22 if score #rdLineT rd matches 0 run function rlk:boss/raiden/line/show {t:"가소",c:"#d7b4ff",s:9,f:0,n:9,e:0,g:3}
execute if score #rdLine rd matches 22 if score #rdLineT rd matches 3 run function rlk:boss/raiden/line/show {t:"가소롭군",c:"#d7b4ff",s:9,f:0,n:9,e:0,g:3}
execute if score #rdLine rd matches 22 if score #rdLineT rd matches 6 run function rlk:boss/raiden/line/show {t:"가소롭군.",c:"#d7b4ff",s:22,f:12,n:34,e:1,g:3}
execute if score #rdLine rd matches 23 if score #rdLineT rd matches 0 run function rlk:boss/raiden/line/show {t:"슬슬",c:"#d7b4ff",s:9,f:0,n:9,e:0,g:3}
execute if score #rdLine rd matches 23 if score #rdLineT rd matches 3 run function rlk:boss/raiden/line/show {t:"슬슬 끝내",c:"#d7b4ff",s:9,f:0,n:9,e:0,g:3}
execute if score #rdLine rd matches 23 if score #rdLineT rd matches 6 run function rlk:boss/raiden/line/show {t:"슬슬 끝내지",c:"#d7b4ff",s:9,f:0,n:9,e:0,g:3}
execute if score #rdLine rd matches 23 if score #rdLineT rd matches 9 run function rlk:boss/raiden/line/show {t:"슬슬 끝내지.",c:"#d7b4ff",s:22,f:12,n:34,e:1,g:3}
execute if score #rdLine rd matches 24 if score #rdLineT rd matches 0 run function rlk:boss/raiden/line/show {t:"터무",c:"#d7b4ff",s:9,f:0,n:9,e:0,g:3}
execute if score #rdLine rd matches 24 if score #rdLineT rd matches 3 run function rlk:boss/raiden/line/show {t:"터무니",c:"#d7b4ff",s:9,f:0,n:9,e:0,g:3}
execute if score #rdLine rd matches 24 if score #rdLineT rd matches 6 run function rlk:boss/raiden/line/show {t:"터무니 없군",c:"#d7b4ff",s:9,f:0,n:9,e:0,g:3}
execute if score #rdLine rd matches 24 if score #rdLineT rd matches 9 run function rlk:boss/raiden/line/show {t:"터무니 없군.",c:"#d7b4ff",s:22,f:12,n:34,e:1,g:3}
execute if score #rdLine rd matches 25 if score #rdLineT rd matches 0 run function rlk:boss/raiden/line/show {t:"무상",c:"#d7b4ff",s:9,f:0,n:9,e:0,g:3}
execute if score #rdLine rd matches 25 if score #rdLineT rd matches 3 run function rlk:boss/raiden/line/show {t:"무상의",c:"#d7b4ff",s:9,f:0,n:9,e:0,g:3}
execute if score #rdLine rd matches 25 if score #rdLineT rd matches 6 run function rlk:boss/raiden/line/show {t:"무상의 진",c:"#d7b4ff",s:9,f:0,n:9,e:0,g:3}
execute if score #rdLine rd matches 25 if score #rdLineT rd matches 9 run function rlk:boss/raiden/line/show {t:"무상의 진!",c:"#d7b4ff",s:22,f:12,n:34,e:1,g:3}
execute if score #rdLine rd matches 26 if score #rdLineT rd matches 0 run function rlk:boss/raiden/line/show {t:"이",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 26 if score #rdLineT rd matches 2 run function rlk:boss/raiden/line/show {t:"이 눈으",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 26 if score #rdLineT rd matches 4 run function rlk:boss/raiden/line/show {t:"이 눈으로",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 26 if score #rdLineT rd matches 6 run function rlk:boss/raiden/line/show {t:"이 눈으로 속세",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 26 if score #rdLineT rd matches 8 run function rlk:boss/raiden/line/show {t:"이 눈으로 속세를",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 26 if score #rdLineT rd matches 10 run function rlk:boss/raiden/line/show {t:"이 눈으로 속세를 꿰뚫",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 26 if score #rdLineT rd matches 12 run function rlk:boss/raiden/line/show {t:"이 눈으로 속세를 꿰뚫어",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 26 if score #rdLineT rd matches 14 run function rlk:boss/raiden/line/show {t:"이 눈으로 속세를 꿰뚫어 보리",c:"#d7b4ff",s:8,f:0,n:8,e:0,g:2}
execute if score #rdLine rd matches 26 if score #rdLineT rd matches 16 run function rlk:boss/raiden/line/show {t:"이 눈으로 속세를 꿰뚫어 보리.",c:"#d7b4ff",s:24,f:12,n:36,e:1,g:2}
execute if score #rdLine rd matches 27 if score #rdLineT rd matches 0 run function rlk:boss/raiden/line/show {t:"어리",c:"#e6a3ff",s:9,f:0,n:9,e:0,g:3}
execute if score #rdLine rd matches 27 if score #rdLineT rd matches 3 run function rlk:boss/raiden/line/show {t:"어리석군",c:"#e6a3ff",s:9,f:0,n:9,e:0,g:3}
execute if score #rdLine rd matches 27 if score #rdLineT rd matches 6 run function rlk:boss/raiden/line/show {t:"어리석군.",c:"#e6a3ff",s:22,f:12,n:34,e:1,g:3}
