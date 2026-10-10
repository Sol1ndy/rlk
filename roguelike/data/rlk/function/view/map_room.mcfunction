# 북향 투명 액자의 실제 지도면: z=1000007.992109375, x=1000004..1000005, y=300..301.
# 제목/안내/위치 표시는 같은 평면에 둔다. transformation은 네 필드를 모두 작성한다.
fill 1000000 297 1000000 1000008 303 1000008 minecraft:black_concrete hollow
kill @e[tag=rlk_mapv]
summon minecraft:glow_item_frame 1000004 300 1000007 {Tags:["rlk_mapv","rlk_mapframe"],block_pos:[I;1000004,300,1000007],Facing:2b,Fixed:1b,Invisible:1b,Invulnerable:1b,Silent:1b,ItemRotation:0b}
# 위치 표식은 글꼴의 여백/기준선에 의존하지 않는 가운데 정렬 다이아몬드다.
summon minecraft:block_display 1000004.5 300.5 1000007.9901875 {Tags:["rlk_mapv","rlk_mapdot","rlk_mappin"],block_state:{id:"minecraft:black_concrete"},brightness:{sky:15,block:15},transformation:{translation:[0f,-0.01767767f,0f],scale:[0.025f,0.025f,0.0005f],left_rotation:[0f,0f,0.38268343f,0.92387953f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:block_display 1000004.5 300.5 1000007.9901875 {Tags:["rlk_mapv","rlk_mapdot"],block_state:{id:"minecraft:yellow_concrete"},brightness:{sky:15,block:15},transformation:{translation:[0f,-0.01272792f,-0.0007f],scale:[0.018f,0.018f,0.0005f],left_rotation:[0f,0f,0.38268343f,0.92387953f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:text_display 1000004.5 301.045 1000007.9901875 {Tags:["rlk_mapv"],Rotation:[180f,0f],billboard:"fixed",text:{text:"던전 지도",color:"gold",bold:true},alignment:"center",background:0,shadow:true,brightness:{sky:15,block:15},transformation:{translation:[0f,0f,0f],scale:[0.3f,0.3f,0.3f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:text_display 1000004.5 299.915 1000007.9901875 {Tags:["rlk_mapv"],Rotation:[180f,0f],billboard:"fixed",text:{text:"◆ 현재 위치  ·  좌/우클릭 닫기",color:"#FFDB55"},alignment:"center",background:0,shadow:true,brightness:{sky:15,block:15},transformation:{translation:[0f,0f,0f],scale:[0.17f,0.17f,0.17f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
data modify storage rlk:map version set value 3
