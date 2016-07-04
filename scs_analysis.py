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

def print_analysis(param_d,param_l,instance,file_prefix):
    """ Performs print analysis
        
        param_d: substitutions for symbols, should evaluate to numeric values
        
        param_l: expresions to print

        filename: filename for output of print analysis

        TODO: the structure of output is not yet finished        
    """
    filename = "%s.results" % file_prefix
    subst = []
    for symbol,value in param_d.iteritems():
        tokens = scs_parser.parse_param_expresion(value)
        try:    
            value =  float(sympy.sympify(scs_parser.params2values(tokens,instance.paramsd)))
        except ValueError:
            logging.error("Passed subsitution for %s is not a number, aborting analysis")
            return
        subst.append((symbol,value))
        
    for expresion in param_l:
        tokens = scs_parser.parse_analysis_expresion(expresion)
        value =  sympy.factor(sympy.sympify(scs_parser.results2values(tokens,instance)))
        value = value.subs(subst)
        with open(filename,'a') as file:
            file.write("%s \n\n" %expresion)            
            file.write(sympy.pretty(value, use_unicode=False))
            file.write("\n=====================\n")
        

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
    config = {'fstart':1,
              'fstop':1e6,
              'npoints':100}
    for config_name,config_value in param_d.iteritems():
        if config_name in config:
            config.update({config_name:config_value})
            
    for config_name in config.keys():
        if config_name in param_d:
            config_value = param_d[config_name]
            tokens = scs_parser.parse_param_expresion(config_value)
            try:    
                config_value =  float(sympy.sympify(scs_parser.params2values(tokens,instance.paramsd)))
            except ValueError:
                logging.error("Passed subsitution for %s is not a number, aborting analysis")
                return
            config.update({config_name:config_value})
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

    F = np.logspace(np.log10(config['fstart']),np.log10(config['fstop']),config['npoints'])
    for expresion in param_l:
        tokens = scs_parser.parse_analysis_expresion(expresion)
        value = sympy.factor(sympy.sympify(scs_parser.results2values(tokens,instance)))
        value = value.subs(subst)
        value = value.subs('s',sympy.sympify('2*pi*I*f')).evalf()
        T = sympy.lambdify('f',sympy.sqrt(value*sympy.conjugate(value)))
        PH = sympy.lambdify('f',sympy.arg(value).evalf())
        t,ph = [],[]
        for f in F:            
            try:
                t.append(float(T(f)))
                ph.append(float(PH(f)))
            except ValueError:
                logging.error("Numeric error while evaluating expresions: %s. Not all values where subsituted?" % value)
                return
        
        fig = plt.figure()
                    
        ax1 = fig.add_subplot(2,1,1)
        ax1.loglog(F,t)    
        ax1.set_xlabel("f [Hz]")
        ax1.set_ylabel("|%s|" % expresion)    
        
        ax2 = fig.add_subplot(2,1,2)        
        ax2.plot(F,ph)
        ax2.set_xscale('log')
        ax2.set_xlabel("f [Hz]")
        ax2.set_ylabel("ph(%s)" % expresion)
        fig.savefig('%s_%d.png' %(file_sufix,PlotNumber.plot_num))
        PlotNumber.plot_num += 1        

#Dictionary of analysis name with appropriate functions
analysis_dict = {'print':print_analysis,
                 'plot':plot_analysis}



    