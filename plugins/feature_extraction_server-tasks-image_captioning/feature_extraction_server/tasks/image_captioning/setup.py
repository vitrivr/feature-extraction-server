from setuptools import setup, find_namespace_packages


setup(
    name='feature_extraction_server-tasks-image_captioning',

    version='1',

    description='',
    long_description='',

    author='Fynn Faber',
    author_email='fynn.f.faber@proton.me',

    license='Apache Software License',

    packages=find_namespace_packages(include=['feature_extraction_server.tasks.*']),
    zip_safe=False,
)