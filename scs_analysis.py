"""
    Module holding functions for performing analysis on solved instances of circuits.
"""

__author__ = "Tomasz Kniola"
__credits__ = ["Tomasz Kniola"]

__license__ = "LGPL"
__version__ = "0.0.1"
__email__ = "kniola.tomasz@gmail.com"
__status__ = "development"

import sympy
import logging
import warnings
import numpy as np
import matplotlib.pyplot as plt

import scs_parser

def print_analysis(param_d,param_l,instance,file_sufix):
    """ Performs print analysis
        
        param_d: substitutions for symbols, should evaluate to numeric values
        
        param_l: expresions to print

        filename: filename for output of print analysis

        TODO: the structure of output is not yet finished        
    """
    filename = "%s.results" % file_sufix
    subst = []
    for symbol,value in param_d.iteritems():
        #tokens = scs_parser.parse_param_expresion(value)
        #try:    
        #    value =  float(sympy.sympify(scs_parser.params2values(tokens,instance.paramsd)))
        #except ValueError:
        #    logging.error("Passed subsitution for %s is not a number, aborting analysis")
        #    return
        subst.append((symbol,value))
        
    print_name = param_l[0]
    
    for expresion in param_l[1:]:
        tokens = scs_parser.parse_analysis_expresion(expresion)
        value =  sympy.factor(sympy.sympify(scs_parser.results2values(tokens,instance)),sympy.symbols('s'))
        #value =  sympy.sympify(scs_parser.results2values(tokens,instance)).simplify()
        value = value.subs(subst).simplify()        
        instance.paramsd.update({print_name:value})
        with open(filename,'a') as file:
            file.write("%s: %s \n---------------------\n" %(print_name,expresion))        
            file.write(str(value))
            file.write("\n\n")
        

class PlotNumber:
    """ Just to keep track of how many files were saved to a file not to overwrite them
    """
    plot_num = 0

def plot_analysis(param_d,param_l,instance,file_sufix):
    """ Performs plot analysis

        param_d: substitutions for symbols, or named parameters for plot
        
        param_l: expresions to plot

        TODO: needs to write full description of config options and how they work and what do we
              get
    """
    warnings.filterwarnings('ignore') #Just getting rid of those fake casting from complex warnings
    #TODO: add description to those files
    s,w = sympy.symbols(('s','w'))
    I = sympy.sympify('I')
    config = {'fstart':1,
              'fstop':1e6,
              'fscale':'log',  
              'npoints':100,
              'yscale':'log',
              'type':'amp',
              'show_zp_on_plot':'yes',
              'show_zp_form':'yes',
              'hold':'no',
              'show_poles':'yes',
              'show_zeros':'yes',
              'title':'',
              'show_legend':'no'}
            
    for config_name in config.keys():
        if config_name in param_d:
            config.update({config_name:param_d[config_name]})
            param_d.pop(config_name)

    subst = []
    for symbol,value in param_d.iteritems():
        tokens = scs_parser.parse_param_expresion(value)
        try:    
            value =  float(sympy.sympify(scs_parser.params2values(tokens,instance.paramsd)))
        except ValueError:
            logging.error("Passed subsitution for %s is not a number, aborting analysis")
            return
        subst.append((symbol,value))

    if config['fscale'] == 'log':
        F = np.logspace(np.log10(float(config['fstart'])),np.log10(float(config['fstop'])),int(config['npoints']))
    elif config['fscale'] == 'linear':
        F = np.linspace(float(config['fstart']),float(config['fstop']),int(config['npoints']))
    else:
        logging.error("Option %s for yscale invalid!" % config['yscale'])
        return
    
    if config['fscale'] != 'log' and config['fscale'] != 'linear':
        logging.error("Option %s for fscale invalid!" % config['fscale'])
        return
    filename = "%s.results" % file_sufix
        
    with open(filename,'a') as file:
        for expresion in param_l:
            file.write("%s: %s \n---------------------\n" %('AC analysis of',expresion))     
            tokens = scs_parser.parse_analysis_expresion(expresion)
            value0 = sympy.factor(sympy.sympify(scs_parser.results2values(tokens,instance)),s).simplify()
            file.write("%s = %s \n\n" % (expresion,str(value0)))
            w = sympy.symbols('w',real=True)   
            denominator = sympy.denom(value0)
            numerator = sympy.numer(value0)
            poles = sympy.solve(denominator,s)
            zeros = sympy.solve(numerator,s)
            poles_r = sympy.roots(denominator,s)
            zeros_r = sympy.roots(numerator,s)
            gdc = str(value0.subs(s,0).simplify())
            file.write('G_DC = %s\n\n' %(gdc))  
            
            p = 0
            titled = 1
            for pole,degree in poles_r.iteritems():
                if pole == 0:
                    titled *= s**degree
                else:   
                    titled *= (s/sympy.symbols("\\omega_p%d" %p)+1)
                p += 1
            z = 0
            titlen = 1
            for zero,degree in zeros_r.iteritems():
                if zero == 0:
                    titlen *= s**degree
                else:   
                    titlen *= (s/sympy.symbols("\\omega_z%d" %z)+1)
                z += 1
            title = sympy.symbols("G_DC")*(titlen/titled)
            value = value0.subs(subst)
            f = sympy.symbols('f',real=True)
            value = value.subs(s,sympy.sympify('2*pi*I').evalf()*f)
            T = sympy.lambdify(f,abs(sympy.numer(value))/abs(sympy.denom(value)))
            PH = sympy.lambdify(f,sympy.arg(value))
            t,ph = [],[]
        
            if config['type']=='amp':
                Z = T
                ylabel = '|T(f)|'
            elif config['type']=='phase':
                Z = PH
                ylabel = 'ph(T(f))'
            else:
                logging.error("Option %s for type invalid!" % config['type'])
                return 

            try: 
                Y = [float(Z(f)) for f in F]   
            except ValueError:
                logging.error("Numeric error while evaluating expresions: %s. Not all values where subsituted?" % value0)
                continue
            
            plt.plot(F,Y)
            plt.hold(True)
            plt.title(r'$%s$' % sympy.latex(title,mul_symbol="dot") , y=1.05)            
            plt.xscale(config['fscale'])
            plt.yscale(config['yscale'])
            plt.xlabel('f [Hz]')
            plt.ylabel(ylabel)
            
            if len(poles): file.write('Poles: \n')
            
            p = 0
            for pole in poles: 
                 
                try:                    
                    pole_value = pole.subs(subst)
                    pole_value_f = abs(np.float64(-abs(pole_value)/sympy.sympify('2*pi').evalf() )  )
                    pole_s =  (-pole).simplify()               
                    polestr = str(pole_s)
                    file.write('wp_%d = %s\n\n' %(p,polestr))    
                    
                    p = p + 1               
                    if pole_value_f > float(config['fstop']) or pole_value_f < float(config['fstart'])  or np.isnan(Z(pole_value_f)): continue
                    if config['show_poles'] == 'yes':
                        plt.plot(pole_value_f,Z(pole_value_f),'o')            
                        plt.text(pole_value_f,Z(pole_value_f),r'$\omega_{p%d} $' %(p-1))
                        plt.axvline(pole_value_f, linestyle='dashed')
                except: None
            
            z = 0 
            for zero in zeros:  
                try:
                    zero_value = zero.subs(subst)
                    zero_value_f = abs(np.float64(-abs(zero_value)/sympy.sympify('2*pi').evalf()))
                    zero_s  =  (-zero).simplify()
                    zerostr = str(zero_s)
                    file.write('wz_%d = %s\n\n' %(z,zerostr))  
                    z = z + 1
                    if zero_value_f > float(config['fstop']) or zero_value_f < float(config['fstart'])  or np.isnan(Z(zero_value_f)): continue
                    if config['show_zeros'] == 'yes':
                        plt.plot(zero_value_f,Z(zero_value_f),'*')
                        plt.axvline(zero_value_f, linestyle='dashed')
                        plt.text(zero_value_f, Z(zero_value_f),r'$\omega_{z%d} $' %(z-1))
                except: None
            if config['hold'] == 'no':
                plt.savefig('%s_%d.png' % (file_sufix,PlotNumber.plot_num))
                PlotNumber.plot_num += 1      
                plt.hold(False)
            

#Dictionary of analysis name with appropriate functions
analysis_dict = {'print':print_analysis,
                 'plot':plot_analysis}



    