import os, tarfile, datetime

# 排除掉 vision 目录下的图片以节省空间，只保留核心代码与日志
def filter_func(tarinfo):
    if tarinfo.name.endswith('.png') or tarinfo.name.endswith('.jpg') or tarinfo.name.endswith('.wav') or tarinfo.name.endswith('.gif'):
        return None
    return tarinfo

backup_name = f"/data/universe_seed_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.tar.gz"
def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir), filter=filter_func)

make_tarfile(backup_name, "/data")
print(f"🌌 Universe compressed into a singularity seed at {backup_name}")
print(f"Seed Mass (Thermodynamic Weight): {os.path.getsize(backup_name) / 1024:.2f} KB")
