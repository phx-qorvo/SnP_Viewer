import skrf as rf
import pylab
from pylab import *
import numpy as np
import matplotlib.pylab as plt
import matplotlib.gridspec as gridspec
from Tkinter import *
import sys 

from Utils import*
from get_user_file_constraints import UserLimits
# pylab.ion()   #makes it so plots print out on screen (if you want that)

def plot_and_format(data,pdf_pages,start,stop,spec,filetype):      
    #if dataset is empty skip this module
    if len(data)!=0:
        
        networks=[]
        labels  =[]
        
        root=Tk()
        user_constrainsts=UserLimits(filetype,master=root)      
        user_constrainsts.mainloop()   
        root.destroy()    
        
        for i in range (0,len(data)):
            networks.append(rf.Network(data[i]))
        
        # for i in range (0,len(networks)):
            # if start!=0:
                # networks[i]=networks[i].cropped(start,stop)
                
        for i in range (0,len(data)): 
            name=data[i].split("/")
            labels.append(name[len(name)-1])

       
       
        # start = int(user_constrainsts.start.get()) #gets start/stop
        # for q in range (0,len(user_constrainsts.start)):
            # print user_constrainsts.start[q].get()    
 
        # -------Formatting setup                             
        font = {'family' : 'Bitstream Vera Sans','weight' : 'bold','size'   : 45}#enlargens the font (its too small without this)            
        matplotlib.rc('font', **font)
        colors=cm.rainbow(np.linspace(0,1,len(networks)))        

        counter=0
        plot_number=1
        fig=plt.figure(1)    
        for j in range (0,filetype):                                         #first integer of snp
            for i in range (0,filetype):                                     #second integer of snp
            
                                                         
                
                if user_constrainsts.plot[counter].get()==1:           #port checked
                    ax=fig.add_subplot(filetype,filetype,plot_number)                                        
                    
                    start= user_constrainsts.start[counter].get()*1e6
                    stop = user_constrainsts.stop[counter].get()*1e6                    
                    
                    for k in range (0,len(networks)):                                                                                                                                                               
                        current_net=networks[k]
                        if user_constrainsts.start[counter].get() !=0.0:  #apply frequency cropping                            
                            current_net=networks[k].cropped(start,stop)
                    
                        if plot_number==1: lab=labels[k];  dt=True
                        else:              lab='';         dt=False
                            
                            
                        if user_constrainsts.graphtype[counter].get()==1:     #dB checked
                            current_net.plot_s_db(m=j,n=i,label=lab,color=colors[k])                                                                                    
                            ax.grid(True)
                        else:                            
                            current_net.plot_s_smith(m=j,n=i,show_legend=dt,chart_type='z',draw_labels=True,label_axes=True,color=colors[k])    

                            
                        #-------------plot markers
                        frequeny_points=user_constrainsts.markers_out[counter]
                        for frequeny_point in frequeny_points:
                            new_freq=rf.Frequency(frequeny_point,frequeny_point,1,'mhz')
                            new_network= current_net.interpolate(new_freq)         
    
                            if user_constrainsts.graphtype[counter].get()==1:     #dB checked    
                                ax=pylab.gca()                                                        
                                ax.plot(frequeny_point*1e6,new_network.s_db[0][j][i],'green',marker='^',markersize=25)
                                ax.text(frequeny_point*1e6,new_network.s_db[0][j][i],str(frequeny_point)+"MHz "+str(round(new_network.s_db[0][j][i],2))+"dB",fontsize=9) 
                            else:
                                new_network.plot_s_smith(m=j,n=i,chart_type='z',marker='^',markersize=25,label=' ',draw_labels=False,label_axes=False,show_legend=False,color='green') 
                                ax.text(new_network.s_re[0][j][i],new_network.s_im[0][j][i],str(round(frequeny_point,2))+"MHz",fontsize=9)
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                    if plot_number ==1:   
                        leg=ax.legend(bbox_to_anchor=(.15, 1.25))
                        for color,text in zip(colors,leg.get_texts()):
                            text.set_color(color)
                      
                        
                        
                    plot_number=plot_number+1
                    pylab.title(str(j+1)+str(i+1))#puts a title on each graph
                    
                counter=counter+1
                
 
 
        # sys.exit("stop")
 
        
        
        # saves figure to pdf  
        fig = matplotlib.pyplot.gcf()
        fig.suptitle('Charts',fontsize=70) #puts a page Title
        fig.set_size_inches(90,60)
        pdf_pages.savefig(dpi=100,orientation='landscape')
        pylab.clf()        
        plt.close('all')

        

    ##TO DO: incorporate moving average into available functions
    # def movingaverage (values, window):
        # weights = np.repeat(1.0, window)/window    
        # sma = np.convolve(values, weights,'same')
    # return sma  
 
                