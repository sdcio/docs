import os
import shutil

def on_post_build(config, **kwargs):
    site_dir = config['site_dir']
    artifactsDir = os.path.join(site_dir, 'artifacts')

    # make sure the artifacts folder exists in the webroot
    if not os.path.exists(artifactsDir):
        os.makedirs(artifactsDir)



    ### Basic Usage
    # clab file
    shutil.copy('docs/getting-started/artifacts/basic-usage.clab.yaml', os.path.join(artifactsDir,"basic-usage", 'basic-usage.clab.yaml'))
        
    # copy the kform generated artifacts.yaml
    shutil.copy('config-server-repo/artifacts/out/artifacts.yaml', os.path.join(artifactsDir,"basic-usage", 'colocated.yaml'))

    # connection profile
    shutil.copy('config-server/example/connection-profiles/target-conn-profile-gnmi.yaml', os.path.join(artifactsDir,"basic-usage", 'target-conn-profile-gnmi.yaml'))
    
    # sync profile
    shutil.copy('config-server-repo/example/sync-profiles/target-sync-profile-gnmi.yaml', os.path.join(artifactsDir,"basic-usage", 'target-sync-profile-gnmi.yaml'))

    # schema
    shutil.copy('config-server-repo/example/schemas/schema-nokia-srl-23.10.1.yaml', os.path.join(artifactsDir,"basic-usage", 'schema-nokia-srl-23.10.1.yaml'))

    # discovery rule
    shutil.copy('docs/getting-started/artifacts/discovery_address.yaml', os.path.join(artifactsDir,"basic-usage", 'discovery_address.yaml'))

    #secret srl
    shutil.copy('docs/getting-started/artifacts/secret-srl.yaml', os.path.join(artifactsDir,"basic-usage", 'secret-srl.yaml'))
