'''
Created on Mar 14, 2012

@author: mudassar
'''
import os
import sys

try:
    import etl
except ImportError:
    
    
    # Get the absolute file path
    p = os.path.abspath(__file__)
    
    # Move 4 steps above. FIXME: This would change in case of relocation.
    for i in range(0, 3):
        p = os.path.split(p)[0]
    # Append to PYTHONPATH
    sys.path.append(p)
    

from etl.cron.core import single_seller_job


if __name__ == '__main__':
    single_seller_job()
