import shutil, errno

def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise
        
def deploy():
    shutil.rmtree('/job/silly_seasons/common/maya/scripts/fs_asset_toolkit/')
    copyanything('/home/dswanepoel/maya/scripts/fs_asset_toolkit/', '/job/silly_seasons/common/maya/scripts/fs_asset_toolkit/')

deploy()