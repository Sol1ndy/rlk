# 도움말 한 줄 "  <id> — <이름>" (macro: pre · id · post = 채울 명령 pre+id+post, st · np · ns = 이름이 있는 저장소와 경로 np+id+ns).
# 줄 전체를 누르면 명령이 채워진다. 맨 앞의 빈 텍스트에는 꾸밈이 없어 색 · 굵기 · 글꼴을 물려받지 않는다 (tools/help_lib.py row()).
$tellraw @s [{text:"",click_event:{action:"suggest_command",command:'$(pre)$(id)$(post)'},hover_event:{action:"show_text",value:'$(pre)$(id)$(post)'}},{text:"  $(id)",color:"yellow"},{text:" — ",color:"dark_gray"},{storage:"$(st)",nbt:"$(np)$(id)$(ns)",color:"white"}]
