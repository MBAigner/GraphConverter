from distutils.core import setup

with open('README.rst') as f:
    long_description = f.read()
print(long_description)
setup(
  name='GraphConverter',
  packages=['GraphConverter', 'GraphConverter.util', 'GraphConverter.document', 'GraphConverter.merging',
            'GraphConverter.models'],
  version='0.3',
  license='MIT',
  description='A tool for creating a graph representation out of the content of PDF documents.',
  long_description=long_description,
  author='Michael Aigner, Florian Preis',
  # author_email='your.email@domain.com',
  url='https://github.com/MBAigner/Graph-Converter',
  download_url='https://github.com/MBAigner/GraphConverter/archive/v0.1.tar.gz',
  keywords=['python', 'pdf', 'pdf-converter', 'graph', 'graph-algorithms', 'graph-representation', 'visibility-graph',
            'document-analysis'],
  install_requires=[
      'numpy',
      'pandas==1.0.3',
      'networkx==2.2',
      'scikit-learn==0.20.0',
      'PDFContentConverter==0.7'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7'
  ],
)
