import os
import shutil

def on_post_build(config, **kwargs):
    site_dir = config['site_dir']
    artifactsDir = os.path.join(site_dir, 'artifacts')

    # make sure the artifacts folder exists in the webroot
    if not os.path.exists(artifactsDir):
        os.makedirs(artifactsDir)

    # copy the kform generated artifacts.yaml
    shutil.copy('config-server-repo/artifacts/out/artifacts.yaml', os.path.join(artifactsDir, 'colocated.yaml'))

    shutil.copy('docs/getting-started/basic-usage.clab.yaml', os.path.join(artifactsDir, 'basic-usage.clab.yaml'))