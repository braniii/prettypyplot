## Subplots

This is an example of using `prettypyplot.subplots` module.

```python
# ~~~ IMPORT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import matplotlib.pyplot as plt
import numpy as np

import prettypyplot as pplt

# ~~~ DEFINE DATA ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
np.random.seed(1337)
N, t = 500, np.linspace(0, 3 * np.pi, N)

pplt.use_style(figsize=.8)

xs = [
    np.sin(t + np.pi * np.random.rand()) + 0.1 * np.random.rand(N)
    for _ in range(8)
]

fig, axs = plt.subplots(
    3,
    3,
    sharex=True,
    sharey=True,
    gridspec_kw={'hspace': 0, 'wspace': 0},
)

for idx, (ax, x) in enumerate(zip(axs.flatten(), xs)):
    pplt.plot(t, xs[0], ax=ax)
    ax.grid(False)

# functions of subplots submodule
pplt.hide_empty_axes()
pplt.label_outer()
pplt.subplot_labels(xlabel=r'$x$', ylabel=r'sinus $f(x)$')

pplt.savefig(f'gallery/subplots/subplots.png')
plt.close()
```

![subplots](gallery/subplots/subplots_8figs.png)
