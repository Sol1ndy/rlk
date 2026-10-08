# abilities = 설명 줄 목록(텍스트 컴포넌트). 형식: 효과 서술 → 빈 줄 → "항목: 수치"
data modify storage rlk:items registry.witch_thimble set value {item:"minecraft:purple_dye",name:"마녀의 골무",type:"accessory",rarity:"common",stats:{elemMastery:30},abilities:[{text:"",extra:[{text:"원소전투 스킬과 원소폭발의 피해가 증가한다."}]},{text:""},{text:"",extra:[{text:"피해 증가: "},{text:"8%",color:"#FFE08A"}]}],desc:["책을 연체하면 벼락을 맞는다."],engravings:["thunder","chain"]}
data modify storage rlk:items ids append value "witch_thimble"
