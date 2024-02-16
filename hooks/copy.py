import os
import shutil

def on_post_build(config, **kwargs):
    site_dir = config['site_dir']
    artifactsDir = os.path.join(site_dir, 'artifacts')

    # make sure the artifacts folder exists in the webroot
    if not os.path.exists(artifactsDir):
        os.makedirs(artifactsDir)

    ### Basic Usage
    basic_usage_dir = os.path.join(artifactsDir,"basic-usage")
    os.makedirs(basic_usage_dir)

    # clab file
    shutil.copy('docs/getting-started/artifacts/basic-usage.clab.yaml', os.path.join(basic_usage_dir, 'basic-usage.clab.yaml'))
        
    # copy the kform generated artifacts.yaml
    shutil.copy('config-server-repo/artifacts/out/artifacts.yaml', os.path.join(basic_usage_dir, 'colocated.yaml'))

    # connection profile
    shutil.copy('config-server-repo/example/connection-profiles/target-conn-profile-gnmi.yaml', os.path.join(basic_usage_dir, 'target-conn-profile-gnmi.yaml'))
    
    # sync profile
    shutil.copy('config-server-repo/example/sync-profiles/target-sync-profile-gnmi.yaml', os.path.join(basic_usage_dir, 'target-sync-profile-gnmi.yaml'))

    # schema
    shutil.copy('config-server-repo/example/schemas/schema-nokia-srl-23.10.1.yaml', os.path.join(basic_usage_dir, 'schema-nokia-srl-23.10.1.yaml'))

    # discovery rule
    shutil.copy('docs/getting-started/artifacts/discovery_address.yaml', os.path.join(basic_usage_dir, 'discovery_address.yaml'))

    #secret srl
    shutil.copy('docs/getting-started/artifacts/secret-srl.yaml', os.path.join(basic_usage_dir, 'secret-srl.yaml'))
