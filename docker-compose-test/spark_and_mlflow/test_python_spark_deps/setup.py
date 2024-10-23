from setuptools import setup, find_packages

setup(
    name='my_project',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'boto3',
        'mlflow',
        'pyspark',
        'numpy'
    ],
    zip_safe=True,
)

# python setup.py sdist --formats=zip
# python setup.py bdist_egg

"""However, it does not allow to add packages built as Wheels and 
therefore does not allow to include dependencies with native code."""
"""so user code can be shipped but python libraries will have to be installed on the workers.
Probs have to integrated into the image"""

# call inside the cluster, not from host pls, scripts are transfered to the spark worker nodes, dns/ip resolution is different
# spark-submit --master spark://spark-master:7077 --py-files dist/my_project-0.1.zip testsparksubmit.py
# spark-submit --master spark://spark-master:7077 --py-files dist/my_project-0.1-py3.12.egg testsparksubmit.py