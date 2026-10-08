# abilities = 설명 줄 목록(텍스트 컴포넌트). 형식: 효과 서술 → 빈 줄 → "항목: 수치"
data modify storage rlk:items registry.coin_pouch set value {item:"minecraft:leather",model:"minecraft:bundle",name:"동전 주머니",type:"accessory",rarity:"common",stats:{},abilities:[{text:"",extra:[{text:"적을 처치할 때 떨어지는 골드가 늘어난다."}]},{text:""},{text:"",extra:[{text:"추가 골드: "},{text:"+1",color:"#FFE08A"}]}],desc:["짤랑거리는 소리가 발걸음을 가볍게 한다."],engravings:["treasure","dash"]}
data modify storage rlk:items ids append value "coin_pouch"
