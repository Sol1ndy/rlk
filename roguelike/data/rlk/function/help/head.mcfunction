# 도움말 첫 줄 (macro: cmd = 명령 모양, what = 목록 설명). 생성기 쪽 같은 모양: tools/help_lib.py head()
$tellraw @s ["",{text:"[도움말] ",color:"#7FD4C1",bold:true},{text:"$(cmd)",color:"white"},{text:"  $(what) — 줄을 누르면 명령이 채워집니다",color:"gray"}]
