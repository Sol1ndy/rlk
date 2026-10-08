# abilities = 설명 줄 목록(텍스트 컴포넌트). 형식: 효과 서술 → 빈 줄 → "항목: 수치"
data modify storage rlk:items registry.cavalry_coin set value {item:"minecraft:raw_iron",name:"기병대장의 동전",type:"accessory",rarity:"common",stats:{critChance:3},abilities:[{text:"",extra:[{text:"적을 처치하면 원소 에너지를 얻는다."}]},{text:""},{text:"",extra:[{text:"원소 에너지: "},{text:"처치당 1pt",color:"#FFE08A"}]}],desc:["앞면이 나오면 한 잔 더."],engravings:["emblem","execute"]}
data modify storage rlk:items ids append value "cavalry_coin"
