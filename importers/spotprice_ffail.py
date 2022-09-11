import requests, json, postgresql, sys, getopt, os
from datetime import datetime as dt
from datetime import date as d
from datetime import timedelta



def add_ffail_parser(parent, subparsers):
    # ffail_import
    import = subparsers.add_parser('import',
                                    help='Deploy updated applicat',
                                    description='Deploy new application image without updating repo config',
                                    parents=[parent])
    common_args(deployp)
    deployp.add_argument("version", help="Application version to deploy (image tag)")
    deployp.add_argument("-u", "--update", action="store_true", help="Only update config")
    deployp.add_argument("--sidecar", type=str, help="Sidecar image version to deploy (name:version)")
    deployp.set_defaults(func=do_deploy)


def do_import(args):
    """ deploy new image """


#    application, environment, namespace = get_common_args(args)
#    if args.update:
#        print('[INFO] Updating deploy configuration only. Commit and create PR manually.')
#        cwd = script_utils.require_k8sobjects(args.k8sobjects)
#        kustomize_path = script_utils.get_kustomize_path(cwd)
#
#        env_patch = os.path.join(script_utils.get_env_path(kustomize_path, application, environment),
#                                 'deployment-patch.yaml')
#        if not os.path.exists(env_patch):
#            print('[ERROR] Environment patch not found:', env_patch)
#            return
#
#        if args.sidecar:
#            parts = args.sidecar.split(':')
#            if not parts or len(parts) < 2:
#                print('[ERROR] Sidecar update format: name:version')
#                return
#            sidecar_name = parts[0]
#            sidecar_version = parts[1]
#            image, _, _ = verify_image(application, environment, namespace, sidecar_version, args.verbose,
#                                       containername=sidecar_name)
#
#        image, _, _ = verify_image(application, environment, namespace, args.version, args.verbose)
#        if not image:
#            print(f'[ERROR] Unable to deploy {application}/{environment}')
#            return
#
#        # NOTE: there is an assumption here that the patch includes at least the 'containers' item and app metadata
#        script_utils.update_path_in_file(f'spec/template/spec/containers:name={application}/image', image, env_patch)
#    else:
#        deploy_util.deploy(app=application, env=environment, namespace=namespace,
#                           version=args.version,
#                           sidecar=args.sidecar,
#                           dryrun=args.dryrun, verbose=args.verbose)



#!/usr/bin/env python3


PG = os.getenv('PG_CONNECTION_STRING')
FFAILTOKEN = os.getenv('FFAILTOKEN')

request_date = d.today() + timedelta(days=1)
try:
   opts, args = getopt.getopt(sys.argv[1:],"d:")

   for opt, arg in opts:
      if opt == '-d':
         request_date = arg
except getopt.GetoptError:
    #We don't care
    print("")

r =requests.get('https://norway-power.ffail.win/?key=' + FFAILTOKEN + '&zone=NO1&date=' + str(request_date))

if r.status_code != 200:
    print("HTTP Response: " + str(r.status_code))
    print("Requested: " + r.url)
    print(r.text[:200])
    sys.exit(2)

json_data = r.json()
db = postgresql.open(PG)

save_price = db.prepare("INSERT INTO spotprice VALUES ($1, $2, $3, $4)")
for key in json_data:
    save_price(dt.fromisoformat(key), json_data[key]['NOK_per_kWh'], dt.fromisoformat(json_data[key]['valid_from']), dt.fromisoformat(json_data[key]['valid_to']))
