# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import pandas as pd
import numpy as np
import matplotlib as plt
%pylab inline

# <codecell>

df = pd.read_csv('all.tsv',sep='\t')

# <codecell>

df.head()

# <codecell>

df.describe()

# <codecell>


