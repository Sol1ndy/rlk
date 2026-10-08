# abilities = 설명 줄 목록(텍스트 컴포넌트). 형식: 효과 서술 → 빈 줄 → "항목: 수치"
data modify storage rlk:items registry.thief_gloves set value {item:"minecraft:rabbit_hide",name:"도둑의 장갑",type:"accessory",rarity:"rare",stats:{critChance:5},abilities:[{text:"",extra:[{text:"치명타로 피해를 주면 골드를 얻는다."}]},{text:""},{text:"",extra:[{text:"획득량: "},{text:"1골드",color:"#FFE08A"}]},{text:"",extra:[{text:"쿨타임: "},{text:"1초",color:"#FFE08A"}]}],desc:["손버릇은 고치기 어렵다."],engravings:["treasure","keen"]}
data modify storage rlk:items ids append value "thief_gloves"
