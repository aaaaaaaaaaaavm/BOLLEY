"""Package my A5h masters using the existing deterministic Gen3 archive format."""
import argparse
import json
import package_gen3_cad as package
package.BUILD=package.ROOT/'cad/BUILD_GEN3_12TURN.json'
package.OUTPUT=package.ROOT/'cad/exports/gen3_12turn'
package.MANIFEST=package.OUTPUT/'PACKAGE.json'
COMMANDS=['python cad/build_gen3_12turn.py --build','python tools/package_gen3_12turn.py --write']
def main():
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--write',action='store_true');g.add_argument('--check',action='store_true');a=p.parse_args()
    if a.write:
        package.write();data=json.loads(package.MANIFEST.read_text());data['generation']='Gen3 A5h detailed 12-turn';data['regeneration']=COMMANDS;package.MANIFEST.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    else:
        package.check();data=json.loads(package.MANIFEST.read_text())
        if data['regeneration']!=COMMANDS or data['generation']!='Gen3 A5h detailed 12-turn':raise SystemExit('A5h package regeneration instructions are stale')
if __name__=='__main__':main()
