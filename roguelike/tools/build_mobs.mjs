// Rebuild the original shield, mage, archer and cannon rigs and their sprite aliases.
// Run: node tools/build_mobs.mjs --datapack <pack> --resourcepack <unpacked resource pack>
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';
const base=path.dirname(fileURLToPath(import.meta.url));
const arg=name=>{const i=process.argv.indexOf(name);return i<0?undefined:process.argv[i+1];};
const dp=path.resolve(arg('--datapack')||path.join(base,'..'));
const rpArg=arg('--resourcepack');
if(!rpArg)throw new Error('Provide --resourcepack pointing to an unpacked resource pack.');
const rp=path.resolve(rpArg);
for(const tool of ['build_shield.mjs','build_casters_archer.mjs','build_cannon.mjs']){
 const result=spawnSync(process.execPath,[path.join(base,tool),'--datapack',dp,'--resourcepack',rp],{stdio:'inherit'});
 if(result.error)throw result.error;
 if(result.status!==0)process.exit(result.status||1);
}
const read=name=>JSON.parse(fs.readFileSync(path.join(base,name),'utf8'));
const sources=[...read('casters_archer_poses.json').atlasSources,...read('cannon_poses.json').atlas,{type:'minecraft:single',resource:'rlk:skin/mob_sh'}];
for(const block of ['iron_block','polished_deepslate','dark_oak_planks'])sources.push({type:'minecraft:single',resource:'minecraft:block/'+block,sprite:'rlk:cm/sh/'+block});
const atlasPath=path.join(rp,'assets/minecraft/atlases/items.json');
const atlas=fs.existsSync(atlasPath)?JSON.parse(fs.readFileSync(atlasPath,'utf8')):{sources:[]};
for(const raw of sources){
 const source={type:'minecraft:single',...raw};
 const id=source.sprite||source.resource;
 atlas.sources=atlas.sources.filter(s=>(s.sprite||s.resource)!==id);
 atlas.sources.push(source);
}
fs.mkdirSync(path.dirname(atlasPath),{recursive:true});
fs.writeFileSync(atlasPath,JSON.stringify(atlas,null,2)+'\n');
