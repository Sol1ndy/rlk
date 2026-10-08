# macro: dy(높이), color. 글은 rlk:io lab.t (줄바꿈 포함)
$summon minecraft:text_display ~ ~$(dy) ~ {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{nbt:"lab.t",storage:"rlk:io",interpret:true,color:"$(color)"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.65f,0.65f,0.65f]}}
