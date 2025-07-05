import os

def create_init_files(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if '__pycache__' in dirpath:
            continue
        init_path = os.path.join(dirpath, '__init__.py')
        if not os.path.exists(init_path):
            with open(init_path, 'w') as f:
                f.write('# auto-generated __init__.py\n')
            print(f'✅ Created: {init_path}')

if __name__ == '__main__':
    create_init_files('app')  # hanya app/ saja, karena prisma generate ke situ