# view/mode {m:"help"}: 시점 번호 (view/mode_do · view/tick 의 #vmode view)
function rlk:help/head {cmd:"/function rlk:view/mode {m:…}",what:"시점 번호"}
tellraw @s [{text:"",click_event:{action:"suggest_command",command:'/function rlk:view/mode {m:1}'},hover_event:{action:"show_text",value:'/function rlk:view/mode {m:1}'}},{text:"  1",color:"yellow"},{text:" — ",color:"dark_gray"},{text:"숄더뷰",color:"white"}]
tellraw @s [{text:"",click_event:{action:"suggest_command",command:'/function rlk:view/mode {m:2}'},hover_event:{action:"show_text",value:'/function rlk:view/mode {m:2}'}},{text:"  2",color:"yellow"},{text:" — ",color:"dark_gray"},{text:"F5 위쪽 시점 (기본)",color:"white"}]
tellraw @s [{text:"",click_event:{action:"suggest_command",command:'/function rlk:view/off'},hover_event:{action:"show_text",value:'/function rlk:view/off'}},{text:"  view/off",color:"yellow"},{text:" — ",color:"dark_gray"},{text:"1인칭",color:"white"}]
