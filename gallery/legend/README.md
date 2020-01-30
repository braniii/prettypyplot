## Legend

This is an example of using `prettypyplot.plot.legend`.

.. warning::
    This is not yet correctly implemented for `STYLE='minimal'`.

```python
# ~~~ IMPORT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import matplotlib.pyplot as plt
import numpy as np

import prettypyplot as pplt

# ~~~ DEFINE DATA ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
np.random.seed(1337)
N = 500
t = np.linspace(0, 3 * np.pi, N)
x1, x2, x3 = [np.sin(t + np.pi * np.random.rand()) + 0.1 * np.random.rand(N)
              for _ in range(3)]

for style in ['default', 'minimal']:
    pplt.setup_pyplot(style=style)

    # legend
    for outside in ['top', 'bottom', 'left', 'right', False]:
        fig, ax = plt.subplots()
        pplt.plot(t, x1, label='$x_1$')
        pplt.plot(t, x2, label='$x_2$')
        pplt.plot(t, x3, label='$x_3$')

        pplt.legend(title='function:', outside=outside)
        pplt.savefig(f'gallery/legend/{style}_plot_legend_{outside}.png')
        plt.close()
```

![default](../gallery/legend/default_plot_legend_False.png)
![right](../gallery/legend/default_plot_legend_right.png)
![top](../gallery/legend/default_plot_legend_top.png)
