
# coding: utf-8

# In[1]:

import numpy as np
import pymc3 as pm
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import beta
plt.style.use('seaborn-darkgrid')
print('Running on PyMC3 v{}'.format(pm.__version__))

# uncomment me to run on cpu
# device = 'cpu'

# uncomment me to run on gpu
device = 'cuda0'

from theano import gpuarray as gpu
gpu.use(device=device)
print('gpu.pygpu_activated:', gpu.pygpu_activated)   # True


# ## Load Data

# In[5]:


df = pd.read_csv('orig_ALL.txt', sep='|')

print('data loaded...')


# In[9]:


non_default = df[df.DFLT == 0]['riskPoints'].astype(np.float32).values
default = df[df.DFLT == 1]['riskPoints'].astype(np.float32).values

del df


# # Bayesian t test
# 
# Tests two distributions for differences in means and standard deviations.
# 
# reference: https://docs.pymc.io/notebooks/BEST.html

# In[11]:


y = pd.DataFrame(dict(value=np.r_[non_default, default], group=np.r_[['non-default']*len(non_default), ['default']*len(default)]))


# In[12]:


mu_m = y.value.mean()
mu_s = y.value.std() * 2

with pm.Model() as model:
    group1_mean = pm.Normal('group1_mean', mu_m, sd=mu_s)
    group2_mean = pm.Normal('group2_mean', mu_m, sd=mu_s)


# In[13]:


sigma_low = 1
sigma_high = 10

with model:
    group1_std = pm.Uniform('group1_std', lower=sigma_low, upper=sigma_high)
    group2_std = pm.Uniform('group2_std', lower=sigma_low, upper=sigma_high)


# In[14]:


with model:
    nu = pm.Exponential('ν_minus_one', 1/29.) + 1

pm.kdeplot(np.random.exponential(30, size=10000), shade=0.5)
plt.savefig('exponential_parameter_estimate.png')


# In[16]:


with model:
    lambda1 = group1_std**-2
    lambda2 = group2_std**-2

    group1 = pm.StudentT('non_default', nu=nu, mu=group1_mean, lam=lambda1, observed=non_default)
    group2 = pm.StudentT('default', nu=nu, mu=group2_mean, lam=lambda2, observed=default)


# In[17]:


with model:
    diff_of_means = pm.Deterministic('difference of means', group1_mean - group2_mean)
    diff_of_stds = pm.Deterministic('difference of stds', group1_std - group2_std)
    effect_size = pm.Deterministic('effect size',
                                   diff_of_means / np.sqrt((group1_std**2 + group2_std**2) / 2))


# In[22]:


# In[28]:

print('beginning trace...')

with model:
    trace = pm.sample(50)


# In[29]:


pm.plot_posterior(trace, varnames=['group1_mean','group2_mean', 'group1_std', 'group2_std', 'ν_minus_one'],
                  color='#87ceeb')


plt.show()
plt.savefig('group_means_and_stds.png')


pm.plot_posterior(trace, varnames=['difference of means','difference of stds', 'effect size'],
                  ref_val=0,
                  color='#87ceeb')


plt.show()
plt.savefig('difference_of_means_and_stds.png')
# In[30]:


pm.forestplot(trace, varnames=['group1_mean',
                               'group2_mean'])


plt.show()
plt.savefig('forestplot_group_means.png')


pm.forestplot(trace, varnames=['group1_std',
                               'group2_std',
                               'ν_minus_one'])


plt.show()
plt.savefig('forestplot_group_stds.png')


print(pm.summary(trace,varnames=['difference of means', 'difference of stds', 'effect size']))