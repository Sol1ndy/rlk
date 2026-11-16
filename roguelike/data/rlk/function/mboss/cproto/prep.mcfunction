# Hook prep (@s = the kind-9 entrance zone marker, at it; cb/pp/cproto cleared cprep.cproto first): the gate texts, a per-map
# roll (kept by retries: the gate returns with the same cprep), the glyph prop on the stele and its glow chain.
data modify storage rlk:mboss cprep.cproto.gate set value {item:"minecraft:lodestone",model:"minecraft:lodestone",item2:"minecraft:compass",model2:"minecraft:compass",l1:{text:"시험용 수호자",color:"#9FC6E8",bold:true},l2:{text:"챕터 보스 틀 점검 · 내성: 물리 30% · 바위 30% · 그 외 10%",color:"#D0D0D0",bold:false},l3:{text:"좌클릭으로 도전",color:"#A8A8A8",bold:false},n:98}
data modify storage rlk:mboss cprep.cproto.title set value {text:"시험용 수호자",color:"#9FC6E8",bold:true}
data modify storage rlk:mboss cprep.cproto.sub set value {text:"챕터 보스 틀 점검용",color:"#E8E2D0"}
execute store result storage rlk:mboss cprep.cproto.roll int 1 run random value 1..4
kill @e[tag=rlk_mb_cproto_glyph]
summon minecraft:text_display -3.45 203.2 14 {Tags:["rlk_room","rlk_mb_cproto_glyph"],billboard:"vertical",brightness:{sky:15,block:15},background:0,text:{text:"◇",color:"#9FC6E8"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.5f,1.5f,1.5f]}}
schedule function rlk:mboss/cproto/glow 10t replace
