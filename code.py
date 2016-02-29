####################################################################### #
###
### TkDemo()
###
### KCA_plot_inTk ##################################################### # Tk() GUI ###################################################################################################### _plot_inTk TkDemo() #################
from matplotlib.backends.backend_tkagg  import  FigureCanvasTkAgg
from matplotlib.figure                  import  Figure
import matplotlib
matplotlib.use('TkAgg')

def supershape_radius( phi, a, b, m, n1, n2, n3 ):                      # define the function for the SuperShape curve using the following code:
    theta   = .25 * m * phi
    cos     = np.fabs( np.cos( theta ) / a ) ** n2
    sin     = np.fabs( np.sin( theta ) / b ) ** n3
    r       = ( cos + sin ) ** ( -1. / n1 )
    r      /= np.max( r )
    return r

class LinearScaling( object ):                                          # define a utility object to linearly scale a range into another as follows:
    def __init__( self, src_range, dst_range ):

        self.src_start, src_diff = src_range[0], src_range[1] - src_range[0]
        self.dst_start, dst_diff = dst_range[0], dst_range[1] - dst_range[0]

        self.src_to_dst_coeff = dst_diff / src_diff
        self.dst_to_src_coeff = src_diff / dst_diff

    def src_to_dst( self, X ):
        return ( X - self.src_start ) * self.src_to_dst_coeff + self.dst_start

    def dst_to_src( self, X ):
        return ( X - self.dst_start) * self.dst_to_src_coeff + self.src_start

class SuperShapeFrame( Frame ):

    def __init__( self, master = None ):

        Frame.__init__( self, master )
        self.grid()
        self.m          = 3
        self.n1         = 2
        self.n1_scaling = LinearScaling( ( .1, 20 ), ( 0, 200 ) )
        self.n2         = 18
        self.n2_scaling = LinearScaling( ( .1, 20 ), ( 0, 200 ) )
        self.n3         = 18
        self.n3_scaling = LinearScaling( ( .1, 20 ), ( 0, 200 ) )

        self.fig        = Figure( ( 6, 6 ), dpi = 100 )

        canvas          = FigureCanvasTkAgg( self.fig, master = self )

        canvas.get_tk_widget().grid(                                    row = 0, column = 0, columnspan = 4 )

        label           = Label(    self,  text = 'M' )
        label.grid(                                                     row = 1, column = 1 )

        self.m_slider   = Scale(    self,   from_ = 1, to =  20,        \
                                            orient = HORIZONTAL,        command = lambda i : self.update_m() \
                                            )
        self.m_slider.grid(                                             row = 1, column = 2 )
        label           = Label(    self,   text = 'N1' )
        label.grid(                                                     row = 2, column = 1 )
        self.n1_slider = Scale(     self,   from_ = 0, to = 200,        \
                                            orient = HORIZONTAL,        command = lambda i : self.update_n1() \
                                            )
        self.n1_slider.grid(                                            row = 2, column = 2 )
        label = Label(              self,   text = 'N2' )
        label.grid(                                                     row = 3, column = 1 )
        self.n2_slider = Scale(     self,   from_ = 0, to = 200,        \
                                            orient = HORIZONTAL,        command = lambda i : self.update_n2() \
                                            )
        self.n2_slider.grid(                                            row = 3, column = 2 )
        label = Label(              self,   text = 'N3' )
        label.grid(                                                     row = 4, column = 1 )
        self.n3_slider = Scale(     self,   from_ = 0, to = 200,
                                            orient = HORIZONTAL,        command = lambda i : self.update_n3() \
                                            )
        self.n3_slider.grid(                                            row = 4, column = 2 )

        self.draw_figure()                                              # >>> ================================================================ DRAW FIRST APPEARANCE OF THE INSTANCE

    def update_m( self ):
        self.m = self.m_slider.get()
        self.refresh_figure()                                           # >>> .-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-. UPDATE

    def update_n1( self ):
        self.n1 = self.n1_scaling.dst_to_src( self.n1_slider.get() )
        self.refresh_figure()                                           # >>> .-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-. UPDATE

    def update_n2( self ):
        self.n2 = self.n2_scaling.dst_to_src( self.n2_slider.get() )
        self.refresh_figure()                                           # >>> .-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-. UPDATE

    def update_n3(self):
        self.n3 = self.n3_scaling.dst_to_src( self.n3_slider.get() )
        self.refresh_figure()                                           # >>> .-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-. UPDATE

    def refresh_figure( self ):                                         # <<< .-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-. UPDATE ACTUAL APPEARANCE OF THE INSTANCE
        r = supershape_radius( self.phi, 1, 1, self.m, self.n1, self.n2, self.n3 )  # .CALC new polar values in radius dimension
        self.lines.set_ydata( r )                                                   # .MOD <lines>, selectively just their <lines>.set_ydata() coordinates
        self.fig.canvas.draw_idle()                                                 # .GUI MVC-Visual part UPDATE via <self>.<fig>.<canvas>.draw_idle()

    def draw_figure( self ):                                            # <<< =============================================================== DRAW FIRST APPEARANCE OF THE INSTANCE
        self.phi    = np.linspace( 0, 2 * np.pi, 1024 )                             # .STO <phi> a np.array with static fi-coordinates
        r           = supershape_radius( self.phi, 1, 1, self.m, self.n1, self.n2, self.n3 )
        ax          = self.fig.add_subplot( 111, polar = True )                     #
        self.lines, = ax.plot( self.phi, r, lw = 3. )                               # .STO <lines> aListOfLINEs from .plot() function
        self.fig.canvas.draw()                                                      # .GUI MVC-Visual part, enforce first visual output via <self>.<fig>.<canvas>.draw()

def TkDemo():                                                           # Finally, set up and start our user interface:
    """ HELP:       CookBook: Tk-GUI-MVC via SuperShape example
        TESTS:      TkDemo()
        """
    root = Tk()
    root.lift()
    root.protocol( 'WM_DELETE_WINDOW', root.quit() )                    # [X]-overide ---------------------------

    app = SuperShapeFrame( root )                                       # <<<--- pass <root>

    app.master.title( 'CookBook: Tk-GUI-MVC via SuperShape' )

    app.mainloop()
    pass

### ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^