"""
Set-up matplotlib environment.

BSD 3-Clause License

Copyright (c) 2019, Daniel Nagel
All rights reserved.

Author: Daniel Nagel
Version: v0.1

Changelog:
    v0.1:
        - intial release

TODO:
    - use palettable (https://jiffyclub.github.io/palettable/#)
    - setup widths and scaling factors for beamer and poster mode
    - implement tufte style
    - add https://matplotlib.org/3.1.1/tutorials/toolkits/axes_grid.html
      examples
    - move colors in submodule

      fig.subplots_adjust(hspace=0) doesn't work
      use
      fig, axs = plt.subplots(..., gridspec_kw={'hspace': 0.000})

"""
# ~~~ IMPORT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import numpy as np  # np = dm.tryImport('numpy')
import matplotlib as mpl  # mpl = dm.tryImport('matplotlib')
import matplotlib.colors as clr
import matplotlib.pyplot as plt
import mpl_toolkits.axes_grid1


# ~~~ CONSTANTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
MODE = 'default'  # default mode
STYLE = 'default'


# ~~~ FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def setup_pyplot(ssh=False,
                 colors='pastel5',
                 cmap='parula',
                 ncs=10,
                 figsize=(3,),
                 figratio='golden',
                 mode=MODE,
                 style=STYLE):
    """
    Define default matplotlib style.

    Parameters
    ----------
    ssh: disables interactive display for ssh usage
    colors: set the default color cycler from continuous or discrete maps
        Use any of matplotlibs default or
    cmap: sets default cmap
    ncs: Number of colors if continuous cmap is selected
    figsize: give size of default figure in inches, either as tuple (x,y) or
        a single float for the x-axis. The y-axis will be determined by
        figratio.
    figratio: set ratio of figsize x:y to 1:1/'option', where 'option' is one
        of ['1', 'sqrt(2)', 'golden', 'sqrt(3)', '2'] and golden stands for the
        golden ratio (1.618). This option is ignored if figsize is used with
        tuple.
    mode:
        - default: use matplotlib defaults
        - beamer: extra large fontsize
        - print: default sizes
        - poster: for Din A0 posters
    style:
        - default: enables grid and upper and right spines
        - minimal: removes all unneeded lines
        - none: no changes to style

    """
    # set selected mode and style
    global MODE
    MODE = mode
    global STYLE
    STYLE = style

    if ssh:
        mpl.use('Agg')
        plt.ioff()

    # setup LaTeX font
    plt.rc('text', usetex=True)  # use latex with raw string: r'string...'
    plt.rc('font', family='serif')
    plt.rc('pdf', fonttype=42)  # embbed font in pdf

    # include advanced math functions and modern encoding
    plt.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}',
                                           r'\usepackage{lmodern}']

    # register own continuous and discrete cmaps
    for colormap in [__parula(), __parula().reversed(),
                     __turbo(), __turbo().reversed(),
                     __rainforest(), __rainforest().reversed(),
                     clr.ListedColormap(cbf10_array, name='own6'),
                     clr.ListedColormap(pastel5_array, name='pastel5'),
                     clr.ListedColormap(pastel6_array, name='pastel6'),
                     clr.ListedColormap(cbf4_array, name='cbf4'),
                     clr.ListedColormap(cbf5_array, name='cbf5'),
                     clr.ListedColormap(cbf8_array, name='cbf8'),
                     clr.ListedColormap(cbf10_array, name='cbf10'),
                     clr.ListedColormap(ufcd_array, name='ufcd')]:
        plt.register_cmap(cmap=colormap)

    # convert figratio to value
    if figratio == '1':
        figratio = 1.
    elif figratio == 'sqrt(2)':
        figratio = 1.414213562
    elif figratio == 'golden':
        figratio = 1.618033989
    elif figratio == 'sqrt(3)':
        figratio = 1.732050808
    elif figratio == '2':
        figratio = 2.

    # setup figsize
    if isinstance(figsize, (list, tuple, np.ndarray)):
        if len(figsize) == 1:
            figsize = (float(figsize[0]), float(figsize[0])/figratio)
        elif len(figsize) == 2:
            pass
    else:
        figsize = (float(figsize), float(figsize)/figratio)

    # setup figure
    # plt.rcParams['savefig.transparent'] = True
    # plt.rcParams["savefig.facecolor"] = '#ffffff'
    # plt.rcParams["savefig.edgecolor"] = '#ffffff'
    plt.rcParams['savefig.format'] = 'pdf'
    # set manually in savefig for consistent padding
    plt.rcParams['savefig.bbox'] = 'tight'  # 'standard'
    # pad_inches is only used for bbox='tight'
    plt.rcParams['savefig.pad_inches'] = 0.1  # 0.1
    plt.rcParams['path.simplify_threshold'] = 0.02  # 0.1
    plt.rcParams['pdf.compression'] = 9

    # set color cycle and cmap
    # try if discrete cmap was selected
    if style != 'none':
        try:
            color_cycler = plt.cycler(color=plt.get_cmap(colors).colors)
        except AttributeError:
            color_cycler = plt.cycler(
                color=plt.get_cmap(colors)(np.linspace(0, 1, ncs)))

        plt.rcParams['axes.prop_cycle'] = color_cycler
        plt.rcParams['image.cmap'] = cmap

        # change default colors
        if colors == 'ufcd' or cmap == 'ufcd':
            gray_black = '#4d4f53'  # Anthrazit of UFCD
            gray_light = '#b2b4b3'
        else:
            gray_black = '#4d4f55'  # '#4f4f4f'
            gray_light = '#dddfe5'  # '#b0b0b0'
        plt.rcParams['axes.edgecolor'] = gray_black
        plt.rcParams['axes.labelcolor'] = gray_black
        plt.rcParams['text.color'] = gray_black
        plt.rcParams['patch.edgecolor'] = gray_black
        plt.rcParams['xtick.color'] = gray_black
        plt.rcParams['ytick.color'] = gray_black
        plt.rcParams['patch.edgecolor'] = gray_black
        # grid color
        plt.rcParams['grid.color'] = gray_light

        # grid
        plt.rcParams['grid.linestyle'] = '--'
        plt.rcParams['axes.axisbelow'] = True
        plt.rcParams['image.origin'] = 'lower'
        plt.rcParams['hist.bins'] = 50
        plt.rcParams['agg.path.chunksize'] = 20000

        # set legend
        plt.rcParams['legend.fontsize'] = 'small'
        plt.rcParams['legend.title_fontsize'] = 'small'
        plt.rcParams['legend.edgecolor'] = 'inherit'  # from axes.edgecolor
        plt.rcParams['legend.framealpha'] = 1
        plt.rcParams['legend.fancybox'] = False
        # border whitespace
        plt.rcParams['legend.borderpad'] = 0.5
        # the vertical space between the legend entries
        plt.rcParams['legend.labelspacing'] = 0.4
        # the length of the legend lines
        plt.rcParams['legend.handlelength'] = 1.4
        # the height of the legend lines
        plt.rcParams['legend.handleheight'] = 0.7
        # the space between the legend line and legend text
        plt.rcParams['legend.handletextpad'] = 0.5
        # the border between the axes and legend edge
        plt.rcParams['legend.borderaxespad'] = 0.
        # column separation
        plt.rcParams['legend.columnspacing'] = 1.0

        # set figure
        plt.rcParams['figure.figsize'] = figsize  # (8./2.54, 5./2.54)
        plt.rcParams['figure.subplot.left'] = 0.125
        plt.rcParams['figure.subplot.right'] = 0.9
        plt.rcParams['figure.subplot.bottom'] = 0.2  # 0.11
        plt.rcParams['figure.subplot.top'] = 0.9  # 0.8

        # change widths depending on MODE
        plt.rcParams['lines.linewidth'] = __get_scale()['large_scale']*1.5
        plt.rcParams['patch.linewidth'] = __get_scale()['medium_scale']*1.0
        plt.rcParams['hatch.linewidth'] = __get_scale()['medium_scale']*1.0
        plt.rcParams['axes.linewidth'] = __get_scale()['small_scale']*0.8
        plt.rcParams['grid.linewidth'] = __get_scale()['small_scale']*0.8
        # ticks
        plt.rcParams['xtick.major.size'] = __get_scale()['tick_scale']*3.5
        plt.rcParams['ytick.major.size'] = __get_scale()['tick_scale']*3.5
        plt.rcParams['xtick.minor.size'] = __get_scale()['tick_scale']*2.0
        plt.rcParams['ytick.minor.size'] = __get_scale()['tick_scale']*2.0
        plt.rcParams['xtick.major.width'] = __get_scale()['small_scale']*0.8
        plt.rcParams['ytick.major.width'] = __get_scale()['small_scale']*0.8
        plt.rcParams['xtick.minor.width'] = __get_scale()['small_scale']*0.6
        plt.rcParams['ytick.minor.width'] = __get_scale()['small_scale']*0.6
        plt.rcParams['xtick.major.pad'] = __get_scale()['tick_scale']*3.5
        plt.rcParams['ytick.major.pad'] = __get_scale()['tick_scale']*3.5
        plt.rcParams['xtick.minor.pad'] = __get_scale()['tick_scale']*3.4
        plt.rcParams['ytick.minor.pad'] = __get_scale()['tick_scale']*3.4
        plt.rcParams['xtick.labelsize'] = 'small'  # 'normal'
        plt.rcParams['ytick.labelsize'] = 'small'  # 'normal'

        plt.rcParams['font.size'] = __get_scale()['fontsize']
        plt.rcParams['figure.dpi'] = 384

    if style == 'minimal':
        plt.rcParams['axes.grid'] = False
        plt.rcParams['axes.spines.top'] = False
        plt.rcParams['axes.spines.right'] = False
        plt.rcParams['axes.autolimit_mode'] = 'data'  # 'round_numbers'
        plt.rcParams['axes.xmargin'] = 0.1  # 0.05
        plt.rcParams['axes.ymargin'] = 0.1  # 0.05
    elif style == 'default':
        plt.rcParams['axes.grid'] = True
        plt.rcParams['axes.spines.top'] = True
        plt.rcParams['axes.spines.right'] = True
        plt.rcParams['axes.autolimit_mode'] = 'data'  # 'round_numbers'
        plt.rcParams['axes.xmargin'] = 0.05  # 0.05
        plt.rcParams['axes.ymargin'] = 0.05  # 0.05


def imshow(X, ax=None, cmap=None, norm=None, aspect=None,
           interpolation=None, alpha=None, vmin=None, vmax=None,
           origin=None, extent=None, shape=None, filternorm=1,
           filterrad=4.0, imlim=None, resample=None, url=None, **kwargs):
    """
    Display an image, i.e. data on a 2D regular raster.

    This is a wrapper of pyplot.imshow().

    """
    if isinstance(ax, mpl.axes.Axes):
        pass
    else:
        ax = plt.gca()

    if 'zorder' not in kwargs:
        kwargs['zorder'] = 1

    # plot
    im = ax.imshow(X, cmap, norm, aspect, interpolation, alpha, vmin, vmax,
                   origin, extent, shape, filternorm, filterrad, imlim,
                   resample, url, **kwargs)
    return im


def plot(*args, ax=None, scalex=True, scaley=True, data=None, **kwargs):
    """
    Plot simple lineplot.

    Wrapping pyplot.plot() to adjust to style. For more information on the
    arguments see in matplotlib documentation.
    If STYLE='minimal', spines will be limited to plotting range.

    TODO:
        - should ticks be limited to spines width?

    """
    if isinstance(ax, mpl.axes.Axes):
        # print("ax is instance")
        pass
    elif len(args) == 0:
        # print("len(args) == 0")
        # fig = plt.gcf()
        ax = plt.gca()
    elif any([isinstance(arg, mpl.axes.Axes) for arg in args]):
        # print("in args is axes")
        ax = [arg for arg in args if isinstance(arg, mpl.axes.Axes)][0]
        args = tuple(arg for arg in args if not isinstance(arg, mpl.axes.Axes))
    else:
        # print("fallback")
        ax = plt.gca()
    # ax, args, dict(kwargs)

    # plot
    axes = ax.plot(*args, **kwargs)

    if STYLE == 'minimal':
        # TODO: change this to function
        xminmax = __xminmax(ax)
        xticks = ax.get_xticks()
        if xticks.size:
            ax.spines['bottom'].set_bounds(xminmax[0], xminmax[1])
            ax.spines['top'].set_bounds(xminmax[0], xminmax[1])
            # firsttick = np.compress(xticks >= min(ax.get_xlim()), xticks)[0]
            # lasttick = np.compress(xticks <= max(ax.get_xlim()), xticks)[-1]
            # ax.spines['bottom'].set_bounds(firsttick, lasttick)
            # ax.spines['top'].set_bounds(firsttick, lasttick)
            # newticks = xticks.compress(xticks <= lasttick)
            # newticks = newticks.compress(newticks >= firsttick)
            # ax.set_xticks(newticks)

        yminmax = __yminmax(ax)
        yticks = ax.get_yticks()
        if yticks.size:
            ax.spines['left'].set_bounds(yminmax[0], yminmax[1])
            ax.spines['right'].set_bounds(yminmax[0], yminmax[1])
            # firsttick = np.compress(yticks >= min(ax.get_ylim()), yticks)[0]
            # lasttick = np.compress(yticks <= max(ax.get_ylim()), yticks)[-1]
            # ax_i.spines['left'].set_bounds(firsttick, lasttick)
            # ax_i.spines['right'].set_bounds(firsttick, lasttick)
            # newticks = yticks.compress(yticks <= lasttick)
            # newticks = newticks.compress(newticks >= firsttick)
            # ax.set_yticks(newticks)

    return axes


def savefig(fname, use_canvas_size=True, **kwargs):
    """
    Save figure as png and pdf.

    This methods corrects figsize for poster/beamer mode.
    - use_canvas_size: This option uses the figsize as canvas size.
    """
    fig, ax = plt.gcf(), plt.gcf().get_axes()[0]  # plt.gca()
    figsize = fig.get_size_inches()

    set_figsize = figsize

    if STYLE == 'minimal':
        # reduce number of ticks by factor 1.5 if more than 4
        for axes in plt.gcf().get_axes():
            if len(axes.get_xticks()) > 4:
                axes.locator_params(tight=False, axis='x',
                                    nbins=len(axes.get_xticks())/1.5)
            if len(axes.get_yticks()) > 4:
                axes.locator_params(tight=False, axis='y',
                                    nbins=len(axes.get_yticks())/1.5)

    if MODE == 'poster':
        fig.set_size_inches((3*figsize[0], 3*figsize[1]))
    elif MODE == 'beamer':
        fig.set_size_inches((3*figsize[0], 3*figsize[1]))

    # convert figsize to canvas size
    if use_canvas_size:
        fig.tight_layout(pad=0.20, h_pad=0.00, w_pad=0.00)
        x0, y0, width, height = ax.get_position().bounds
        # print((width*figsize[0], height*figsize[1]))
        figsize = (figsize[0]/width, figsize[1]/height)
        fig.set_size_inches(figsize)

        # fig.subplots_adjust(hspace=0)
        # debug message
        x0, y0, width, height = ax.get_position().bounds
        # print((width*figsize[0], height*figsize[1]))

    plt.savefig('{}.pdf'.format(fname), format='pdf', **kwargs)
    plt.savefig('{}.png'.format(fname), format='png', **kwargs)

    # reset figsize, if user calls this function multiple times on same figure
    fig.set_size_inches(set_figsize)


def legend(outside=False, *args, **kwargs):
    """
    Generate a nice legend.

    This is a wrapper of pyplot.legend(). Take a look there for the default
    arguments and options.
    Parameters
    ----------
    outside : False, 'top', 'right'. Remember to set the number of columns with
        ncol= to get a nice output.

    """
    if outside in ['False', 'false']:
        outside = False
    if outside not in [False, 'top', 'right']:
        # TODO: print error message
        print('Use for outside one of [False, "top", "right"].')
        outside = False
    if outside in ['top']:
        if 'bbox_to_anchor' not in kwargs:
            kwargs['bbox_to_anchor'] = (0., 1.0, 1., .01)
        if 'mode' not in kwargs:
            kwargs['mode'] = 'expand'
        if 'loc' not in kwargs:
            kwargs['loc'] = 'lower left'
    elif outside in ['right']:
        if 'bbox_to_anchor' not in kwargs:
            kwargs['bbox_to_anchor'] = (1.03, .5)
        if 'loc' not in kwargs:
            kwargs['loc'] = 'center left'

    # generate legend
    leg = plt.legend(*args, **kwargs)
    if STYLE == 'minimal':
        leg.get_frame().set_linewidth(0.)
    elif STYLE == 'default':
        leg.get_frame().set_linewidth(__get_scale()['small_scale']*0.8)

    if outside in ['top']:
        # shift title to the left
        # https://stackoverflow.com/a/53329898
        c = leg.get_children()[0]
        title = c.get_children()[0]
        hpack = c.get_children()[1]
        c._children = [hpack]
        hpack._children = [title] + hpack.get_children()

    return leg


def __get_scale():
    """Get the scaling factors."""
    if MODE == 'default':
        return {'large_scale': 1.,
                'medium_scale': 1.,
                'small_scale': 1.,
                'tick_scale': 1.,
                'fontsize': 10.}
    elif MODE == 'print':
        return {'large_scale': 1.5,
                'medium_scale': 1.7,
                'small_scale': 1.7,
                'tick_scale': 1.7,
                'fontsize': 12.}
    elif MODE == 'poster':
        return {'large_scale': 4.,
                'medium_scale': 4.,
                'small_scale': 4.,
                'tick_scale': 4.,
                'fontsize': 28.}
    elif MODE == 'beamer':
        return {'large_scale': 4.,
                'medium_scale': 4.,
                'small_scale': 4.,
                'tick_scale': 4.,
                'fontsize': 28.}


def colorbar(imshow=None, width='5%', pad='3%', position='right'):
    """
    Generate colorbar.

    width: can be stated relative as string or absolute in inches
    pad: can be stated relative as string or absolute in inches
    """
    orientation = 'vertical'
    if position in ['top', 'bottom']:
        orientation = 'horizontal'

    # generate divider
    divider = mpl_toolkits.axes_grid1.make_axes_locatable(plt.gca())
    cax = divider.append_axes(position, width, pad=pad)

    # get imshow if not stated
    if not imshow:
        # TODO: find correct instance
        imshow = plt.gca().get_images()

    cbar = plt.colorbar(imshow, cax=cax, orientation=orientation)
    cbar.set_label(r'$\Delta G$ [$k_\textsc{b}T$]')

    # set ticks on top if cb on top
    if position in ['top', 'bottom']:
        cax.xaxis.set_ticks_position(position)
        cax.xaxis.set_label_position(position)

    # invert width and pad
    pad_inv, width_inv = __invert_number(pad), __invert_number(width)
    cax_reset = divider.append_axes(position, width_inv, pad=pad_inv)
    cax_reset.set_visible(False)


def grid(ax=None, *args, **kwargs):
    """
    Generate grid.

    This function will add a grid in case of STYLE='default' and otherwise do
    nothing.

    Parameters
    ----------
    ax: axes to plot grid

    """
    if isinstance(ax, mpl.axes.Axes):
        # print("ax is instance")
        pass
    elif len(args) == 0:
        # print("len(args) == 0")
        # fig = plt.gcf()
        ax = plt.gca()
    elif any([isinstance(arg, mpl.axes.Axes) for arg in args]):
        # print("in args is axes")
        ax = [arg for arg in args if isinstance(arg, mpl.axes.Axes)][0]
        args = tuple(arg for arg in args if not isinstance(arg, mpl.axes.Axes))
    else:
        # print("fallback")
        ax = plt.gca()

    if STYLE == 'default':
        gr_maj = ax.grid(which='major', linestyle='--', **kwargs)
        gr_min = ax.grid(which='minor', linestyle='dotted', **kwargs)
        ax.set_axisbelow(True)

        return (gr_maj, gr_min)
    else:
        return


def __invert_number(num):
    try:  # check if Number
        float(num)
        return -1*num
    except ValueError:  # it is a string
        if num[0] == '-':
            return num[1:]
        else:
            return '-' + num


def __xminmax(ax):
    return __minmax(lim=ax.get_xlim(), rcparam='axes.xmargin')


def __yminmax(ax):
    return __minmax(lim=ax.get_ylim(), rcparam='axes.ymargin')


def __minmax(lim, rcparam):
    """Get range of plotted data."""
    range = lim[1] - lim[0]
    margin = plt.rcParams[rcparam]
    minmax = [lim[0] + (margin+i)/(1+2*margin)*range for i in [0, 1]]
    return minmax


def categorical_cmap(nc,
                     nsc,
                     cmap='tab10',
                     continuous=False,
                     return_colors=False):
    """
    Generate categorical colors of given cmap.

    options:
        - nc: number of colors
        - nsc: number of shades per colors

    https://stackoverflow.com/a/47232942

    """
    if nc > plt.get_cmap(cmap).N:
        raise ValueError("Too many categories for colormap.")
    if continuous:
        ccolors = plt.get_cmap(cmap)(np.linspace(0, 1, nc))
    else:
        ccolors = plt.get_cmap(cmap)(np.arange(nc, dtype=int))
    cols = np.zeros((nc*nsc, 3))
    for i, c in enumerate(ccolors):
        chsv = clr.rgb_to_hsv(c[:3])
        arhsv = np.tile(chsv, nsc).reshape(nsc, 3)
        arhsv[:, 1] = np.linspace(chsv[1], 0.25, nsc)
        arhsv[:, 2] = np.linspace(chsv[2], 1, nsc)
        rgb = clr.hsv_to_rgb(arhsv)
        cols[i*nsc:(i+1)*nsc, :] = rgb
    if return_colors:
        return cols
    else:
        cmap = clr.ListedColormap(cols)
        return cmap


# ~~~ COLORS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# the following colors are generated with  https://medialab.github.io/iwanthue/
cbf10_array = ["#b8434e", "#6dbc5f", "#5b378a", "#bda23a", "#6d80d8",
               "#71893b", "#c873c6", "#46c19a", "#b2457c", "#bc6739"]
cbf5_array = ["#b94663", "#6fac5d", "#697ed5", "#bc7d39", "#9350a1"]
# the following colormaps were created with
# https://colorcyclepicker.mpetroff.net/
cbf4_array = ["#1878b1", "#dd6688", "#2dd9cc", "#feeaae"]
cbf8_array = ["#0c4daa", "#b70226", "#238494", "#d2651e", "#88a8ba",
              "#2ad5ad", "#fbb5fe", "#faf018"]
pastel5_array = ["#3362b0", "#cc3164", "#1ea69c", "#f78746", "#9dd2e7"]
pastel6_array = ["#2452c7", "#c42f22", "#2aa069", "#67b2cf", "#f8a7ae",
                 "#a6f89c"]
own6_array = ["#1f77b4", "#ff7f0e", "#19a16f", "#b70409", "#cb1186", "#57544c"]

# Uni Corporate Design
ufcd_array = ["#2b6ebc", "#dd3931", "#739501", "#e96301", "#a8c3e1"]

# ~~~ PARULA CMAP ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# https://stackoverflow.com/a/43264077
cm_parula_data = [
    [0.2081, 0.1663, 0.5292],
    [0.2116238095, 0.1897809524, 0.5776761905],
    [0.212252381, 0.2137714286, 0.6269714286],
    [0.2081, 0.2386, 0.6770857143],
    [0.1959047619, 0.2644571429, 0.7279],
    [0.1707285714, 0.2919380952, 0.779247619],
    [0.1252714286, 0.3242428571, 0.8302714286],
    [0.0591333333, 0.3598333333, 0.8683333333],
    [0.0116952381, 0.3875095238, 0.8819571429],
    [0.0059571429, 0.4086142857, 0.8828428571],
    [0.0165142857, 0.4266, 0.8786333333],
    [0.032852381, 0.4430428571, 0.8719571429],
    [0.0498142857, 0.4585714286, 0.8640571429],
    [0.0629333333, 0.4736904762, 0.8554380952],
    [0.0722666667, 0.4886666667, 0.8467],
    [0.0779428571, 0.5039857143, 0.8383714286],
    [0.079347619, 0.5200238095, 0.8311809524],
    [0.0749428571, 0.5375428571, 0.8262714286],
    [0.0640571429, 0.5569857143, 0.8239571429],
    [0.0487714286, 0.5772238095, 0.8228285714],
    [0.0343428571, 0.5965809524, 0.819852381],
    [0.0265, 0.6137, 0.8135],
    [0.0238904762, 0.6286619048, 0.8037619048],
    [0.0230904762, 0.6417857143, 0.7912666667],
    [0.0227714286, 0.6534857143, 0.7767571429],
    [0.0266619048, 0.6641952381, 0.7607190476],
    [0.0383714286, 0.6742714286, 0.743552381],
    [0.0589714286, 0.6837571429, 0.7253857143],
    [0.0843, 0.6928333333, 0.7061666667],
    [0.1132952381, 0.7015, 0.6858571429],
    [0.1452714286, 0.7097571429, 0.6646285714],
    [0.1801333333, 0.7176571429, 0.6424333333],
    [0.2178285714, 0.7250428571, 0.6192619048],
    [0.2586428571, 0.7317142857, 0.5954285714],
    [0.3021714286, 0.7376047619, 0.5711857143],
    [0.3481666667, 0.7424333333, 0.5472666667],
    [0.3952571429, 0.7459, 0.5244428571],
    [0.4420095238, 0.7480809524, 0.5033142857],
    [0.4871238095, 0.7490619048, 0.4839761905],
    [0.5300285714, 0.7491142857, 0.4661142857],
    [0.5708571429, 0.7485190476, 0.4493904762],
    [0.609852381, 0.7473142857, 0.4336857143],
    [0.6473, 0.7456, 0.4188],
    [0.6834190476, 0.7434761905, 0.4044333333],
    [0.7184095238, 0.7411333333, 0.3904761905],
    [0.7524857143, 0.7384, 0.3768142857],
    [0.7858428571, 0.7355666667, 0.3632714286],
    [0.8185047619, 0.7327333333, 0.3497904762],
    [0.8506571429, 0.7299, 0.3360285714],
    [0.8824333333, 0.7274333333, 0.3217],
    [0.9139333333, 0.7257857143, 0.3062761905],
    [0.9449571429, 0.7261142857, 0.2886428571],
    [0.9738952381, 0.7313952381, 0.266647619],
    [0.9937714286, 0.7454571429, 0.240347619],
    [0.9990428571, 0.7653142857, 0.2164142857],
    [0.9955333333, 0.7860571429, 0.196652381],
    [0.988, 0.8066, 0.1793666667],
    [0.9788571429, 0.8271428571, 0.1633142857],
    [0.9697, 0.8481380952, 0.147452381],
    [0.9625857143, 0.8705142857, 0.1309],
    [0.9588714286, 0.8949, 0.1132428571],
    [0.9598238095, 0.9218333333, 0.0948380952],
    [0.9661, 0.9514428571, 0.0755333333],
    [0.9763, 0.9831, 0.0538]]


def __parula():
    cmap = clr.LinearSegmentedColormap.from_list('parula',
                                                 cm_parula_data)
    return cmap


# ~~~ TRUBO CMAP ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# https://gist.github.com/FedeMiorelli/640bbc66b2038a14802729e609abfe89
cm_turbo_data = [
    [0.18995, 0.07176, 0.23217],
    [0.19483, 0.08339, 0.26149],
    [0.19956, 0.09498, 0.29024],
    [0.20415, 0.10652, 0.31844],
    [0.20860, 0.11802, 0.34607],
    [0.21291, 0.12947, 0.37314],
    [0.21708, 0.14087, 0.39964],
    [0.22111, 0.15223, 0.42558],
    [0.22500, 0.16354, 0.45096],
    [0.22875, 0.17481, 0.47578],
    [0.23236, 0.18603, 0.50004],
    [0.23582, 0.19720, 0.52373],
    [0.23915, 0.20833, 0.54686],
    [0.24234, 0.21941, 0.56942],
    [0.24539, 0.23044, 0.59142],
    [0.24830, 0.24143, 0.61286],
    [0.25107, 0.25237, 0.63374],
    [0.25369, 0.26327, 0.65406],
    [0.25618, 0.27412, 0.67381],
    [0.25853, 0.28492, 0.69300],
    [0.26074, 0.29568, 0.71162],
    [0.26280, 0.30639, 0.72968],
    [0.26473, 0.31706, 0.74718],
    [0.26652, 0.32768, 0.76412],
    [0.26816, 0.33825, 0.78050],
    [0.26967, 0.34878, 0.79631],
    [0.27103, 0.35926, 0.81156],
    [0.27226, 0.36970, 0.82624],
    [0.27334, 0.38008, 0.84037],
    [0.27429, 0.39043, 0.85393],
    [0.27509, 0.40072, 0.86692],
    [0.27576, 0.41097, 0.87936],
    [0.27628, 0.42118, 0.89123],
    [0.27667, 0.43134, 0.90254],
    [0.27691, 0.44145, 0.91328],
    [0.27701, 0.45152, 0.92347],
    [0.27698, 0.46153, 0.93309],
    [0.27680, 0.47151, 0.94214],
    [0.27648, 0.48144, 0.95064],
    [0.27603, 0.49132, 0.95857],
    [0.27543, 0.50115, 0.96594],
    [0.27469, 0.51094, 0.97275],
    [0.27381, 0.52069, 0.97899],
    [0.27273, 0.53040, 0.98461],
    [0.27106, 0.54015, 0.98930],
    [0.26878, 0.54995, 0.99303],
    [0.26592, 0.55979, 0.99583],
    [0.26252, 0.56967, 0.99773],
    [0.25862, 0.57958, 0.99876],
    [0.25425, 0.58950, 0.99896],
    [0.24946, 0.59943, 0.99835],
    [0.24427, 0.60937, 0.99697],
    [0.23874, 0.61931, 0.99485],
    [0.23288, 0.62923, 0.99202],
    [0.22676, 0.63913, 0.98851],
    [0.22039, 0.64901, 0.98436],
    [0.21382, 0.65886, 0.97959],
    [0.20708, 0.66866, 0.97423],
    [0.20021, 0.67842, 0.96833],
    [0.19326, 0.68812, 0.96190],
    [0.18625, 0.69775, 0.95498],
    [0.17923, 0.70732, 0.94761],
    [0.17223, 0.71680, 0.93981],
    [0.16529, 0.72620, 0.93161],
    [0.15844, 0.73551, 0.92305],
    [0.15173, 0.74472, 0.91416],
    [0.14519, 0.75381, 0.90496],
    [0.13886, 0.76279, 0.89550],
    [0.13278, 0.77165, 0.88580],
    [0.12698, 0.78037, 0.87590],
    [0.12151, 0.78896, 0.86581],
    [0.11639, 0.79740, 0.85559],
    [0.11167, 0.80569, 0.84525],
    [0.10738, 0.81381, 0.83484],
    [0.10357, 0.82177, 0.82437],
    [0.10026, 0.82955, 0.81389],
    [0.09750, 0.83714, 0.80342],
    [0.09532, 0.84455, 0.79299],
    [0.09377, 0.85175, 0.78264],
    [0.09287, 0.85875, 0.77240],
    [0.09267, 0.86554, 0.76230],
    [0.09320, 0.87211, 0.75237],
    [0.09451, 0.87844, 0.74265],
    [0.09662, 0.88454, 0.73316],
    [0.09958, 0.89040, 0.72393],
    [0.10342, 0.89600, 0.71500],
    [0.10815, 0.90142, 0.70599],
    [0.11374, 0.90673, 0.69651],
    [0.12014, 0.91193, 0.68660],
    [0.12733, 0.91701, 0.67627],
    [0.13526, 0.92197, 0.66556],
    [0.14391, 0.92680, 0.65448],
    [0.15323, 0.93151, 0.64308],
    [0.16319, 0.93609, 0.63137],
    [0.17377, 0.94053, 0.61938],
    [0.18491, 0.94484, 0.60713],
    [0.19659, 0.94901, 0.59466],
    [0.20877, 0.95304, 0.58199],
    [0.22142, 0.95692, 0.56914],
    [0.23449, 0.96065, 0.55614],
    [0.24797, 0.96423, 0.54303],
    [0.26180, 0.96765, 0.52981],
    [0.27597, 0.97092, 0.51653],
    [0.29042, 0.97403, 0.50321],
    [0.30513, 0.97697, 0.48987],
    [0.32006, 0.97974, 0.47654],
    [0.33517, 0.98234, 0.46325],
    [0.35043, 0.98477, 0.45002],
    [0.36581, 0.98702, 0.43688],
    [0.38127, 0.98909, 0.42386],
    [0.39678, 0.99098, 0.41098],
    [0.41229, 0.99268, 0.39826],
    [0.42778, 0.99419, 0.38575],
    [0.44321, 0.99551, 0.37345],
    [0.45854, 0.99663, 0.36140],
    [0.47375, 0.99755, 0.34963],
    [0.48879, 0.99828, 0.33816],
    [0.50362, 0.99879, 0.32701],
    [0.51822, 0.99910, 0.31622],
    [0.53255, 0.99919, 0.30581],
    [0.54658, 0.99907, 0.29581],
    [0.56026, 0.99873, 0.28623],
    [0.57357, 0.99817, 0.27712],
    [0.58646, 0.99739, 0.26849],
    [0.59891, 0.99638, 0.26038],
    [0.61088, 0.99514, 0.25280],
    [0.62233, 0.99366, 0.24579],
    [0.63323, 0.99195, 0.23937],
    [0.64362, 0.98999, 0.23356],
    [0.65394, 0.98775, 0.22835],
    [0.66428, 0.98524, 0.22370],
    [0.67462, 0.98246, 0.21960],
    [0.68494, 0.97941, 0.21602],
    [0.69525, 0.97610, 0.21294],
    [0.70553, 0.97255, 0.21032],
    [0.71577, 0.96875, 0.20815],
    [0.72596, 0.96470, 0.20640],
    [0.73610, 0.96043, 0.20504],
    [0.74617, 0.95593, 0.20406],
    [0.75617, 0.95121, 0.20343],
    [0.76608, 0.94627, 0.20311],
    [0.77591, 0.94113, 0.20310],
    [0.78563, 0.93579, 0.20336],
    [0.79524, 0.93025, 0.20386],
    [0.80473, 0.92452, 0.20459],
    [0.81410, 0.91861, 0.20552],
    [0.82333, 0.91253, 0.20663],
    [0.83241, 0.90627, 0.20788],
    [0.84133, 0.89986, 0.20926],
    [0.85010, 0.89328, 0.21074],
    [0.85868, 0.88655, 0.21230],
    [0.86709, 0.87968, 0.21391],
    [0.87530, 0.87267, 0.21555],
    [0.88331, 0.86553, 0.21719],
    [0.89112, 0.85826, 0.21880],
    [0.89870, 0.85087, 0.22038],
    [0.90605, 0.84337, 0.22188],
    [0.91317, 0.83576, 0.22328],
    [0.92004, 0.82806, 0.22456],
    [0.92666, 0.82025, 0.22570],
    [0.93301, 0.81236, 0.22667],
    [0.93909, 0.80439, 0.22744],
    [0.94489, 0.79634, 0.22800],
    [0.95039, 0.78823, 0.22831],
    [0.95560, 0.78005, 0.22836],
    [0.96049, 0.77181, 0.22811],
    [0.96507, 0.76352, 0.22754],
    [0.96931, 0.75519, 0.22663],
    [0.97323, 0.74682, 0.22536],
    [0.97679, 0.73842, 0.22369],
    [0.98000, 0.73000, 0.22161],
    [0.98289, 0.72140, 0.21918],
    [0.98549, 0.71250, 0.21650],
    [0.98781, 0.70330, 0.21358],
    [0.98986, 0.69382, 0.21043],
    [0.99163, 0.68408, 0.20706],
    [0.99314, 0.67408, 0.20348],
    [0.99438, 0.66386, 0.19971],
    [0.99535, 0.65341, 0.19577],
    [0.99607, 0.64277, 0.19165],
    [0.99654, 0.63193, 0.18738],
    [0.99675, 0.62093, 0.18297],
    [0.99672, 0.60977, 0.17842],
    [0.99644, 0.59846, 0.17376],
    [0.99593, 0.58703, 0.16899],
    [0.99517, 0.57549, 0.16412],
    [0.99419, 0.56386, 0.15918],
    [0.99297, 0.55214, 0.15417],
    [0.99153, 0.54036, 0.14910],
    [0.98987, 0.52854, 0.14398],
    [0.98799, 0.51667, 0.13883],
    [0.98590, 0.50479, 0.13367],
    [0.98360, 0.49291, 0.12849],
    [0.98108, 0.48104, 0.12332],
    [0.97837, 0.46920, 0.11817],
    [0.97545, 0.45740, 0.11305],
    [0.97234, 0.44565, 0.10797],
    [0.96904, 0.43399, 0.10294],
    [0.96555, 0.42241, 0.09798],
    [0.96187, 0.41093, 0.09310],
    [0.95801, 0.39958, 0.08831],
    [0.95398, 0.38836, 0.08362],
    [0.94977, 0.37729, 0.07905],
    [0.94538, 0.36638, 0.07461],
    [0.94084, 0.35566, 0.07031],
    [0.93612, 0.34513, 0.06616],
    [0.93125, 0.33482, 0.06218],
    [0.92623, 0.32473, 0.05837],
    [0.92105, 0.31489, 0.05475],
    [0.91572, 0.30530, 0.05134],
    [0.91024, 0.29599, 0.04814],
    [0.90463, 0.28696, 0.04516],
    [0.89888, 0.27824, 0.04243],
    [0.89298, 0.26981, 0.03993],
    [0.88691, 0.26152, 0.03753],
    [0.88066, 0.25334, 0.03521],
    [0.87422, 0.24526, 0.03297],
    [0.86760, 0.23730, 0.03082],
    [0.86079, 0.22945, 0.02875],
    [0.85380, 0.22170, 0.02677],
    [0.84662, 0.21407, 0.02487],
    [0.83926, 0.20654, 0.02305],
    [0.83172, 0.19912, 0.02131],
    [0.82399, 0.19182, 0.01966],
    [0.81608, 0.18462, 0.01809],
    [0.80799, 0.17753, 0.01660],
    [0.79971, 0.17055, 0.01520],
    [0.79125, 0.16368, 0.01387],
    [0.78260, 0.15693, 0.01264],
    [0.77377, 0.15028, 0.01148],
    [0.76476, 0.14374, 0.01041],
    [0.75556, 0.13731, 0.00942],
    [0.74617, 0.13098, 0.00851],
    [0.73661, 0.12477, 0.00769],
    [0.72686, 0.11867, 0.00695],
    [0.71692, 0.11268, 0.00629],
    [0.70680, 0.10680, 0.00571],
    [0.69650, 0.10102, 0.00522],
    [0.68602, 0.09536, 0.00481],
    [0.67535, 0.08980, 0.00449],
    [0.66449, 0.08436, 0.00424],
    [0.65345, 0.07902, 0.00408],
    [0.64223, 0.07380, 0.00401],
    [0.63082, 0.06868, 0.00401],
    [0.61923, 0.06367, 0.00410],
    [0.60746, 0.05878, 0.00427],
    [0.59550, 0.05399, 0.00453],
    [0.58336, 0.04931, 0.00486],
    [0.57103, 0.04474, 0.00529],
    [0.55852, 0.04028, 0.00579],
    [0.54583, 0.03593, 0.00638],
    [0.53295, 0.03169, 0.00705],
    [0.51989, 0.02756, 0.00780],
    [0.50664, 0.02354, 0.00863],
    [0.49321, 0.01963, 0.00955],
    [0.47960, 0.01583, 0.01055]]


def __turbo():
    cmap = clr.LinearSegmentedColormap.from_list('turbo', cm_turbo_data)
    return cmap


# https://github.com/1313e/e13Tools/blob/master/e13tools/colormaps/rainforest/rainforest.py
cm_rainforest_data = [
    [0.00000000e+00, 0.00000000e+00, 0.00000000e+00],
    [3.53476194e-04, 1.82128532e-04, 2.85292393e-04],
    [1.28648133e-03, 6.04952487e-04, 1.02841500e-03],
    [2.78017166e-03, 1.20244959e-03, 2.21135028e-03],
    [4.84079934e-03, 1.93869612e-03, 3.84560550e-03],
    [7.47951036e-03, 2.78742000e-03, 5.95280407e-03],
    [1.07094470e-02, 3.72704018e-03, 8.56159000e-03],
    [1.45426691e-02, 4.73958882e-03, 1.17051323e-02],
    [1.89926028e-02, 5.80831889e-03, 1.54230567e-02],
    [2.40709391e-02, 6.91841293e-03, 1.97593286e-02],
    [2.97895546e-02, 8.05560408e-03, 2.47642589e-02],
    [3.61579283e-02, 9.20708406e-03, 3.04925529e-02],
    [4.30901453e-02, 1.03591405e-02, 3.70083865e-02],
    [5.00276406e-02, 1.15003649e-02, 4.42085031e-02],
    [5.69088885e-02, 1.26187517e-02, 5.15557985e-02],
    [6.37372189e-02, 1.37026074e-02, 5.90359398e-02],
    [7.05146531e-02, 1.47405403e-02, 6.66638341e-02],
    [7.72420892e-02, 1.57214724e-02, 7.44535380e-02],
    [8.39194424e-02, 1.66346663e-02, 8.24183084e-02],
    [9.05457534e-02, 1.74697689e-02, 9.05706046e-02],
    [9.71192764e-02, 1.82168672e-02, 9.89220532e-02],
    [1.03637553e-01, 1.88665580e-02, 1.07483385e-01],
    [1.10097962e-01, 1.94093546e-02, 1.16265536e-01],
    [1.16497299e-01, 1.98361963e-02, 1.25278722e-01],
    [1.22830667e-01, 2.01404192e-02, 1.34529130e-01],
    [1.29094391e-01, 2.03134986e-02, 1.44026364e-01],
    [1.35282731e-01, 2.03504127e-02, 1.53774345e-01],
    [1.41390108e-01, 2.02463701e-02, 1.63777072e-01],
    [1.47410864e-01, 1.99971405e-02, 1.74038136e-01],
    [1.53338507e-01, 1.96008892e-02, 1.84557944e-01],
    [1.59166081e-01, 1.90579310e-02, 1.95334444e-01],
    [1.64886466e-01, 1.83702645e-02, 2.06364167e-01],
    [1.70492181e-01, 1.75423736e-02, 2.17641329e-01],
    [1.75975498e-01, 1.65811960e-02, 2.29158286e-01],
    [1.81328338e-01, 1.54967910e-02, 2.40904992e-01],
    [1.86542119e-01, 1.43035017e-02, 2.52867824e-01],
    [1.91608074e-01, 1.30190896e-02, 2.65031454e-01],
    [1.96517330e-01, 1.16640974e-02, 2.77380326e-01],
    [2.01260183e-01, 1.02664317e-02, 2.89892706e-01],
    [2.05826901e-01, 8.85675152e-03, 3.02547974e-01],
    [2.10207067e-01, 7.47321542e-03, 3.15320539e-01],
    [2.14389971e-01, 6.15792912e-03, 3.28185512e-01],
    [2.18364203e-01, 4.96177901e-03, 3.41112577e-01],
    [2.22117899e-01, 3.94128125e-03, 3.54071000e-01],
    [2.25638565e-01, 3.15967025e-03, 3.67028637e-01],
    [2.28913107e-01, 2.68921460e-03, 3.79949120e-01],
    [2.31927841e-01, 2.60910946e-03, 3.92795088e-01],
    [2.34668506e-01, 3.00632621e-03, 4.05527106e-01],
    [2.37120326e-01, 3.97542838e-03, 4.18103792e-01],
    [2.39268104e-01, 5.61814483e-03, 4.30481999e-01],
    [2.41096359e-01, 8.04265142e-03, 4.42617064e-01],
    [2.42589506e-01, 1.13625146e-02, 4.54463142e-01],
    [2.43732082e-01, 1.56952585e-02, 4.65973637e-01],
    [2.44509031e-01, 2.11605299e-02, 4.77101734e-01],
    [2.44906024e-01, 2.78778601e-02, 4.87801050e-01],
    [2.44909751e-01, 3.59640332e-02, 4.98026544e-01],
    [2.44508511e-01, 4.52731733e-02, 5.07734905e-01],
    [2.43692554e-01, 5.48546354e-02, 5.16885797e-01],
    [2.42454420e-01, 6.45968866e-02, 5.25442917e-01],
    [2.40789345e-01, 7.44664269e-02, 5.33374864e-01],
    [2.38695762e-01, 8.44303364e-02, 5.40655881e-01],
    [2.36175394e-01, 9.44560034e-02, 5.47266839e-01],
    [2.33233443e-01, 1.04511158e-01, 5.53195767e-01],
    [2.29878817e-01, 1.14564021e-01, 5.58438166e-01],
    [2.26123592e-01, 1.24584033e-01, 5.62997277e-01],
    [2.21983123e-01, 1.34542105e-01, 5.66883744e-01],
    [2.17475637e-01, 1.44411136e-01, 5.70115227e-01],
    [2.12622022e-01, 1.54166302e-01, 5.72715757e-01],
    [2.07444756e-01, 1.63785770e-01, 5.74714842e-01],
    [2.01967619e-01, 1.73250746e-01, 5.76146416e-01],
    [1.96215325e-01, 1.82545494e-01, 5.77047823e-01],
    [1.90212875e-01, 1.91657426e-01, 5.77458734e-01],
    [1.83985075e-01, 2.00577021e-01, 5.77420124e-01],
    [1.77556785e-01, 2.09297339e-01, 5.76973623e-01],
    [1.70951381e-01, 2.17814400e-01, 5.76160245e-01],
    [1.64190677e-01, 2.26126769e-01, 5.75019705e-01],
    [1.57295600e-01, 2.34234864e-01, 5.73590292e-01],
    [1.50287878e-01, 2.42140044e-01, 5.71909442e-01],
    [1.43183053e-01, 2.49846990e-01, 5.70009948e-01],
    [1.36001211e-01, 2.57359378e-01, 5.67925271e-01],
    [1.28755069e-01, 2.64683954e-01, 5.65683245e-01],
    [1.21460891e-01, 2.71826562e-01, 5.63311790e-01],
    [1.14131497e-01, 2.78794343e-01, 5.60835186e-01],
    [1.06778114e-01, 2.85594918e-01, 5.58275080e-01],
    [9.94120817e-02, 2.92235833e-01, 5.55651453e-01],
    [9.20438514e-02, 2.98724787e-01, 5.52982131e-01],
    [8.46831320e-02, 3.05069537e-01, 5.50282909e-01],
    [7.73390591e-02, 3.11277811e-01, 5.47567700e-01],
    [7.00203915e-02, 3.17357249e-01, 5.44848666e-01],
    [6.27357496e-02, 3.23315349e-01, 5.42136366e-01],
    [5.54939147e-02, 3.29159427e-01, 5.39439887e-01],
    [4.83042241e-02, 3.34896594e-01, 5.36766974e-01],
    [4.11771146e-02, 3.40533729e-01, 5.34124149e-01],
    [3.43130064e-02, 3.46077433e-01, 5.31516962e-01],
    [2.82315100e-02, 3.51533798e-01, 5.28950896e-01],
    [2.29113810e-02, 3.56909308e-01, 5.26428283e-01],
    [1.83169164e-02, 3.62209808e-01, 5.23951917e-01],
    [1.44136143e-02, 3.67440623e-01, 5.21524933e-01],
    [1.11600939e-02, 3.72607549e-01, 5.19146969e-01],
    [8.52042533e-03, 3.77715424e-01, 5.16819853e-01],
    [6.45349447e-03, 3.82769424e-01, 5.14542467e-01],
    [4.92165063e-03, 3.87774064e-01, 5.12314948e-01],
    [3.88400837e-03, 3.92734028e-01, 5.10135184e-01],
    [3.30343050e-03, 3.97653366e-01, 5.08002445e-01],
    [3.13921748e-03, 4.02536394e-01, 5.05913292e-01],
    [3.35533946e-03, 4.07386749e-01, 5.03866072e-01],
    [3.91350248e-03, 4.12208237e-01, 5.01856881e-01],
    [4.77762678e-03, 4.17004337e-01, 4.99881992e-01],
    [5.91468686e-03, 4.21778136e-01, 4.97938282e-01],
    [7.29035189e-03, 4.26532866e-01, 4.96020463e-01],
    [8.87382075e-03, 4.31271373e-01, 4.94123841e-01],
    [1.06372833e-02, 4.35996221e-01, 4.92243862e-01],
    [1.25538605e-02, 4.40709946e-01, 4.90374688e-01],
    [1.45999838e-02, 4.45414826e-01, 4.88510504e-01],
    [1.67553831e-02, 4.50112913e-01, 4.86645350e-01],
    [1.90037240e-02, 4.54805995e-01, 4.84773356e-01],
    [2.13311377e-02, 4.59495783e-01, 4.82887707e-01],
    [2.37282403e-02, 4.64183719e-01, 4.80981732e-01],
    [2.61899073e-02, 4.68871033e-01, 4.79048639e-01],
    [2.87155064e-02, 4.73558744e-01, 4.77081538e-01],
    [3.13091732e-02, 4.78247653e-01, 4.75073504e-01],
    [3.39793902e-02, 4.82938403e-01, 4.73017250e-01],
    [3.67399915e-02, 4.87631406e-01, 4.70905652e-01],
    [3.96099701e-02, 4.92326871e-01, 4.68731581e-01],
    [4.25449492e-02, 4.97024815e-01, 4.66487941e-01],
    [4.55024227e-02, 5.01725064e-01, 4.64167708e-01],
    [4.85169552e-02, 5.06427268e-01, 4.61763882e-01],
    [5.16145175e-02, 5.11130897e-01, 4.59269609e-01],
    [5.48210513e-02, 5.15835251e-01, 4.56678190e-01],
    [5.81619962e-02, 5.20539465e-01, 4.53983087e-01],
    [6.16618458e-02, 5.25242527e-01, 4.51177941e-01],
    [6.53435732e-02, 5.29943301e-01, 4.48256420e-01],
    [6.92286469e-02, 5.34640487e-01, 4.45212626e-01],
    [7.33364019e-02, 5.39332668e-01, 4.42040819e-01],
    [7.76838422e-02, 5.44018315e-01, 4.38735460e-01],
    [8.22855069e-02, 5.48695792e-01, 4.35291227e-01],
    [8.71532395e-02, 5.53363405e-01, 4.31702653e-01],
    [9.22966911e-02, 5.58019313e-01, 4.27964983e-01],
    [9.77230480e-02, 5.62661600e-01, 4.24073623e-01],
    [1.03437204e-01, 5.67288286e-01, 4.20024078e-01],
    [1.09441960e-01, 5.71897360e-01, 4.15811549e-01],
    [1.15738499e-01, 5.76486708e-01, 4.11431828e-01],
    [1.22326484e-01, 5.81054122e-01, 4.06881275e-01],
    [1.29204237e-01, 5.85597382e-01, 4.02155887e-01],
    [1.36369222e-01, 5.90114273e-01, 3.97250689e-01],
    [1.43817968e-01, 5.94602378e-01, 3.92163134e-01],
    [1.51546519e-01, 5.99059329e-01, 3.86889173e-01],
    [1.59550828e-01, 6.03482732e-01, 3.81423983e-01],
    [1.67825965e-01, 6.07870015e-01, 3.75765482e-01],
    [1.76367917e-01, 6.12218696e-01, 3.69907926e-01],
    [1.85171639e-01, 6.16526104e-01, 3.63849032e-01],
    [1.94233235e-01, 6.20789592e-01, 3.57583433e-01],
    [2.03548047e-01, 6.25006386e-01, 3.51108159e-01],
    [2.13112912e-01, 6.29173674e-01, 3.44417163e-01],
    [2.22923193e-01, 6.33288534e-01, 3.37508077e-01],
    [2.32977119e-01, 6.37347960e-01, 3.30372994e-01],
    [2.43270754e-01, 6.41348850e-01, 3.23008812e-01],
    [2.53801494e-01, 6.45288007e-01, 3.15410003e-01],
    [2.64568060e-01, 6.49162069e-01, 3.07568925e-01],
    [2.75568620e-01, 6.52967571e-01, 2.99479136e-01],
    [2.86801308e-01, 6.56700935e-01, 2.91134224e-01],
    [2.98265145e-01, 6.60358414e-01, 2.82526113e-01],
    [3.09959408e-01, 6.63936098e-01, 2.73646054e-01],
    [3.21883538e-01, 6.67429922e-01, 2.64484575e-01],
    [3.34037042e-01, 6.70835661e-01, 2.55031445e-01],
    [3.46419362e-01, 6.74148940e-01, 2.45275629e-01],
    [3.59030675e-01, 6.77365138e-01, 2.35203747e-01],
    [3.71870886e-01, 6.80479474e-01, 2.24801348e-01],
    [3.84936985e-01, 6.83487393e-01, 2.14056654e-01],
    [3.98229720e-01, 6.86383673e-01, 2.02949604e-01],
    [4.11743899e-01, 6.89163805e-01, 1.91466604e-01],
    [4.25478944e-01, 6.91822457e-01, 1.79583211e-01],
    [4.39426522e-01, 6.94355468e-01, 1.67283065e-01],
    [4.53579155e-01, 6.96758578e-01, 1.54543455e-01],
    [4.67926061e-01, 6.99028208e-01, 1.41341125e-01],
    [4.82452378e-01, 7.01161782e-01, 1.27652859e-01],
    [4.97138395e-01, 7.03158103e-01, 1.13456355e-01],
    [5.11958893e-01, 7.05017767e-01, 9.87316962e-02],
    [5.26884735e-01, 7.06743083e-01, 8.34601182e-02],
    [5.41876732e-01, 7.08339871e-01, 6.76412891e-02],
    [5.56892465e-01, 7.09816241e-01, 5.12958703e-02],
    [5.71881773e-01, 7.11184068e-01, 3.46760376e-02],
    [5.86792395e-01, 7.12457856e-01, 2.09649897e-02],
    [6.01568114e-01, 7.13655461e-01, 1.14450064e-02],
    [6.16154664e-01, 7.14796522e-01, 6.28441703e-03],
    [6.30500789e-01, 7.15902031e-01, 5.61289743e-03],
    [6.44561719e-01, 7.16993005e-01, 9.51989452e-03],
    [6.58301168e-01, 7.18089413e-01, 1.80592372e-02],
    [6.71690082e-01, 7.19210135e-01, 3.12558271e-02],
    [6.84711592e-01, 7.20370675e-01, 4.84904356e-02],
    [6.97354375e-01, 7.21585017e-01, 6.61114700e-02],
    [7.09615979e-01, 7.22863985e-01, 8.34727592e-02],
    [7.21499953e-01, 7.24215908e-01, 1.00549931e-01],
    [7.33013719e-01, 7.25647192e-01, 1.17351596e-01],
    [7.44168040e-01, 7.27162345e-01, 1.33899292e-01],
    [7.54975890e-01, 7.28764307e-01, 1.50219198e-01],
    [7.65450703e-01, 7.30455151e-01, 1.66336935e-01],
    [7.75606655e-01, 7.32235933e-01, 1.82277611e-01],
    [7.85459269e-01, 7.34106368e-01, 1.98067713e-01],
    [7.95020595e-01, 7.36067163e-01, 2.13725321e-01],
    [8.04305241e-01, 7.38117145e-01, 2.29273568e-01],
    [8.13325398e-01, 7.40255707e-01, 2.44730254e-01],
    [8.22091822e-01, 7.42482440e-01, 2.60109798e-01],
    [8.30615388e-01, 7.44796344e-01, 2.75427632e-01],
    [8.38905818e-01, 7.47196533e-01, 2.90697280e-01],
    [8.46971671e-01, 7.49682302e-01, 3.05930270e-01],
    [8.54820622e-01, 7.52253017e-01, 3.21136975e-01],
    [8.62459468e-01, 7.54908158e-01, 3.36326690e-01],
    [8.69893957e-01, 7.57647466e-01, 3.51506872e-01],
    [8.77129232e-01, 7.60470699e-01, 3.66684847e-01],
    [8.84169780e-01, 7.63377677e-01, 3.81867823e-01],
    [8.91019134e-01, 7.66368511e-01, 3.97061523e-01],
    [8.97679908e-01, 7.69443648e-01, 4.12269816e-01],
    [9.04154205e-01, 7.72603581e-01, 4.27496852e-01],
    [9.10443576e-01, 7.75848858e-01, 4.42747359e-01],
    [9.16548532e-01, 7.79180573e-01, 4.58022670e-01],
    [9.22469234e-01, 7.82599730e-01, 4.73325989e-01],
    [9.28205060e-01, 7.86107675e-01, 4.88658912e-01],
    [9.33754723e-01, 7.89706030e-01, 5.04021830e-01],
    [9.39116393e-01, 7.93396495e-01, 5.19416077e-01],
    [9.44287525e-01, 7.97181184e-01, 5.34840323e-01],
    [9.49265018e-01, 8.01062274e-01, 5.50294619e-01],
    [9.54045137e-01, 8.05042327e-01, 5.65776363e-01],
    [9.58623545e-01, 8.09124035e-01, 5.81283689e-01],
    [9.62995355e-01, 8.13310402e-01, 5.96812675e-01],
    [9.67155101e-01, 8.17604622e-01, 6.12359124e-01],
    [9.71096821e-01, 8.22010126e-01, 6.27917381e-01],
    [9.74814101e-01, 8.26530545e-01, 6.43480555e-01],
    [9.78300108e-01, 8.31169680e-01, 6.59040618e-01],
    [9.81547785e-01, 8.35931479e-01, 6.74587533e-01],
    [9.84549820e-01, 8.40819971e-01, 6.90110152e-01],
    [9.87299046e-01, 8.45839201e-01, 7.05594692e-01],
    [9.89788351e-01, 8.50993161e-01, 7.21026119e-01],
    [9.92011330e-01, 8.56285638e-01, 7.36386240e-01],
    [9.93962157e-01, 8.61720139e-01, 7.51655428e-01],
    [9.95636502e-01, 8.67299648e-01, 7.66810613e-01],
    [9.97031460e-01, 8.73026523e-01, 7.81827039e-01],
    [9.98146534e-01, 8.78902191e-01, 7.96676907e-01],
    [9.98983982e-01, 8.84926952e-01, 8.11330289e-01],
    [9.99549279e-01, 8.91099767e-01, 8.25755689e-01],
    [9.99852301e-01, 8.97417862e-01, 8.39919357e-01],
    [9.99906813e-01, 9.03876775e-01, 8.53788057e-01],
    [9.99732621e-01, 9.10469718e-01, 8.67326860e-01],
    [9.99353324e-01, 9.17188176e-01, 8.80504379e-01],
    [9.98800923e-01, 9.24020560e-01, 8.93287138e-01],
    [9.98109732e-01, 9.30954040e-01, 9.05649266e-01],
    [9.97323589e-01, 9.37972434e-01, 9.17563643e-01],
    [9.96492897e-01, 9.45057135e-01, 9.29007032e-01],
    [9.95676036e-01, 9.52186765e-01, 9.39959052e-01],
    [9.94948959e-01, 9.59334170e-01, 9.50394419e-01],
    [9.94422261e-01, 9.66460907e-01, 9.60272181e-01],
    [9.94324199e-01, 9.73490281e-01, 9.69478452e-01],
    [9.96026094e-01, 9.79967385e-01, 9.77162988e-01],
    [9.97755513e-01, 9.86470640e-01, 9.84703230e-01],
    [9.99047345e-01, 9.93159479e-01, 9.92341391e-01],
    [1.00000000e+00, 1.00000000e+00, 1.00000000e+00]]


def __rainforest():
    cmap = clr.LinearSegmentedColormap.from_list('rainforest',
                                                 cm_rainforest_data)
    return cmap
