
def fitting(params, x, y_sex, fit,data=[]):
    amp = params['amp']
    decay = params['decay']
    shift = params['shift']
    sex_param = params['sex']
    
    if len(y_sex)>0:
        if fit == 'poisson':
            model = amp * np.array(x) * np.exp( -decay *np.array(x)) + shift + sex_param*np.array(y_sex)
        elif fit=='exponential':
            model = decay *pow(2,amp*np.array(x)) +shift +  sex_param*np.array(y_sex)
        elif fit=='quadratic':
            model = amp * np.array(x) + decay *pow(np.array(x),2)  + shift + sex_param*np.array(y_sex)
        else:
            model = amp * np.array(x) + shift + sex_param*np.array(y_sex)
    else:
        if fit == 'poisson':
            model = amp * np.array(x) * np.exp( -decay *np.array(x)) + shift 
        elif fit=='exponential':
            model = decay *pow(2,amp*np.array(x))  +shift
        elif fit=='quadratic':
            model = amp * np.array(x) + decay *pow(np.array(x),2)  + shift 
        else:
            model = amp * np.array(x) + shift 


    if data==[]:
        return model
    return model - data
