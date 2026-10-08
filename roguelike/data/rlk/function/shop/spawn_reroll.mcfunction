# macro: rcost. at = 블록 코너. (x, y+0.5, z)에 리롤 인터랙션 + 라벨
summon minecraft:interaction ~0.5 ~0.5 ~0.5 {Tags:["rlk_shop_reroll"],width:1.2f,height:0.6f,response:true}
$summon minecraft:text_display ~0.5 ~0.75 ~0.5 {Tags:["rlk_shop_rlbl"],billboard:"center",see_through:true,background:1073741824,text:{text:"[ 리롤: $(rcost)G ]",color:"aqua",bold:true},transformation:{scale:[0.85f,0.85f,0.85f],translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
