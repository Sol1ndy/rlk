# abilities = 설명 줄 목록(텍스트 컴포넌트). 형식: 효과 서술 → 빈 줄 → "항목: 수치"
data modify storage rlk:items registry.moonlit_loom set value {item:"minecraft:loom",name:"달빛 베틀",type:"accessory",rarity:"legendary",stats:{elemMastery:120},abilities:[{text:"",extra:[{text:"원소 반응을 일으키면 한동안"}]},{text:"",extra:[{text:"원소 마스터리가 크게 증가한다."}]},{text:""},{text:"",extra:[{text:"원소 마스터리 증가: "},{text:"150",color:"#FFE08A"}]},{text:"",extra:[{text:"지속 시간: "},{text:"8초",color:"#FFE08A"}]}],desc:["달빛으로 짠 천은 숲의 노래를 기억한다."],engravings:["fullmoon","lunar"]}
data modify storage rlk:items ids append value "moonlit_loom"
